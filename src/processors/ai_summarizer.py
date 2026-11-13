"""
AI Summarizer processor (v4.2 Auto-Healing).
Uses Google Gemini REST API with dynamic model discovery and automatic deprecation healing
to synthesize the day's 25 collected trends into a crisp 3-bullet Turkish Executive Briefing (TL;DR).
"""

import json
import os
import re
from typing import Optional
import requests

from src.config import (
    DEFAULT_TIMEOUT,
    GEMINI_API_KEY_ENV,
    GEMINI_TIMEOUT
)
from src.logging_config import logger
from src.models import (
    ArxivPaper,
    ExecutiveBriefing,
    GithubRepoItem,
    HuggingFacePaperItem,
    TrendItem
)

# Preferred models in priority order (Gemini 3.8 Flash generation)
PREFERRED_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.8-flash-lite",
    "gemini-3.0-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]


class AiSummarizer:
    """Generates structured daily executive briefings using Google Gemini API with auto-healing."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: tuple[float, float] = GEMINI_TIMEOUT
    ):
        self.api_key = api_key or os.getenv(GEMINI_API_KEY_ENV)
        self.timeout = timeout
        self._discovered_model: Optional[str] = None
        self._candidate_models: list[str] = []

    def _discover_active_model(self) -> Optional[str]:
        """Queries Google Gemini models API to find active models supporting generateContent."""
        if not self.api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
        try:
            resp = requests.get(url, timeout=(5.0, 15.0))
            if resp.status_code == 200:
                data = resp.json()
                models = data.get("models", [])
                supported = [
                    m.get("name", "").replace("models/", "")
                    for m in models
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ]
                # Prioritize PREFERRED_MODELS that are actually present
                ordered = [pref for pref in PREFERRED_MODELS if pref in supported]
                # Then any remaining flash models
                for m_name in supported:
                    if "flash" in m_name and m_name not in ordered:
                        ordered.append(m_name)
                # Then any remaining general models
                for m_name in supported:
                    if m_name not in ordered:
                        ordered.append(m_name)

                if ordered:
                    self._candidate_models = ordered
                    selected = ordered[0]
                    logger.info(f"Discovered active Gemini models: {ordered[:3]} (selected: {selected})")
                    return selected
            else:
                logger.warning(f"Could not discover Gemini models (status {resp.status_code})")
        except Exception as e:
            logger.warning(f"Error querying Gemini models list: {e}")

        self._candidate_models = list(PREFERRED_MODELS)
        return "gemini-3.8-flash"

    def _build_prompt(
        self,
        hn_items: list[TrendItem],
        github_items: list[GithubRepoItem],
        hf_items: list[HuggingFacePaperItem],
        arxiv_items: list[ArxivPaper]
    ) -> str:
        """Constructs a compact context prompt summarizing all 25 trends."""
        lines = [
            "Bugün teknoloji ve yapay zeka dünyasında öne çıkan gelişmeler:\n",
            "### HackerNews:"
        ]
        for it in hn_items[:10]:
            lines.append(f"- {it.title} ({it.category})")

        lines.append("\n### GitHub Trending:")
        for gh in github_items[:5]:
            desc = f": {gh.description[:90]}" if gh.description else ""
            lines.append(f"- {gh.name} ({gh.language}){desc}")

        lines.append("\n### Hugging Face Popüler AI Makaleleri:")
        for hf in hf_items[:5]:
            lines.append(f"- {hf.title}")

        lines.append("\n### ArXiv Araştırmaları:")
        for ax in arxiv_items[:5]:
            lines.append(f"- {ax.title}")

        lines.append("""
GÖREV:
Bu verileri bir teknoloji analisti gözüyle sentezle ve Türkçe olarak tam 3 tematik madde halinde günlük yönetici brifingi (Executive TL;DR) oluştur.
Her madde 1-2 akıcı ve bilgilendirici cümleden oluşmalıdır.

Format kesinlikle şu şekilde olmalıdır:
SEKTOR: [Teknoloji sektörü, büyük şirketler, güvenlik veya regülasyonlar hakkında sentez]
YAZILIM: [Açık kaynak projeleri, geliştirici araçları ve altyapı kütüphaneleri hakkında sentez]
ARASTIRMA: [Yapay zeka modelleri ve araştırma makaleleri hakkında sentez]
""")
        return "\n".join(lines)

    def _create_fallback_briefing(self, reason: str = "") -> ExecutiveBriefing:
        """Creates an algorithmic placeholder briefing when Gemini is not available."""
        disclaimer = f"*({reason})*" if reason else ""
        return ExecutiveBriefing(
            sector_events="Teknoloji sektörü ve pazarındaki güncel gelişmeler geliştirici platformlarında yoğun tartışma konusu oldu.",
            software_opensource="Açık kaynak dünyasında modern yazılım araçları ve yeni nesil sistem kütüphaneleri öne çıktı.",
            ai_research="Yapay zeka literatüründe ve Hugging Face topluluğunda otonom ajanlar ile model optimizasyonu odak noktası oldu.",
            generated_by_ai=False,
            disclaimer=disclaimer
        )

    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Sends prompt to Gemini REST API and returns raw text response with auto-healing."""
        if not self.api_key:
            logger.info("GEMINI_API_KEY not found in environment. Using graceful fallback.")
            return None

        if not self._discovered_model:
            self._discovered_model = self._discover_active_model() or "gemini-3.8-flash"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 450
            }
        }

        candidate_models = list(self._candidate_models or [self._discovered_model] or PREFERRED_MODELS)

        i = 0
        while i < len(candidate_models):
            model_name = candidate_models[i]
            i += 1
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            try:
                logger.info(f"Generating AI Executive Briefing via Gemini API ({model_name})...")
                resp = requests.post(url, json=payload, timeout=self.timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            self._discovered_model = model_name
                            return parts[0].get("text", "")
                else:
                    logger.warning(f"Gemini API ({model_name}) returned status {resp.status_code}")
                    # Auto-heal: If Google returns a deprecation message suggesting a specific model, try it immediately!
                    m = re.search(r"Please update your code to use models/([a-zA-Z0-9\.\-]+)", resp.text)
                    if m:
                        suggested_model = m.group(1)
                        if suggested_model not in candidate_models:
                            logger.info(f"Auto-healing: dynamically injecting Google's suggested model '{suggested_model}'")
                            candidate_models.insert(i, suggested_model)
            except Exception as e:
                logger.warning(f"Gemini API call failed on {model_name}: {e}")

        return None

    def synthesize(
        self,
        hn_items: list[TrendItem],
        github_items: list[GithubRepoItem],
        hf_items: list[HuggingFacePaperItem],
        arxiv_items: list[ArxivPaper]
    ) -> ExecutiveBriefing:
        """
        Synthesizes the day's signals into a 3-bullet Executive Briefing.

        Returns:
            ExecutiveBriefing instance (either AI-generated or graceful fallback).
        """
        prompt = self._build_prompt(hn_items, github_items, hf_items, arxiv_items)
        raw_text = self._call_gemini_api(prompt)

        if not raw_text:
            return self._create_fallback_briefing("AI özeti için GEMINI_API_KEY bekleniyor veya kota aşıldı")

        # Parse SEKTOR, YAZILIM, ARASTIRMA from generated text
        sektor_m = re.search(r"SEKTOR:\s*(.*?)(?=(?:YAZILIM:|ARASTIRMA:|\Z))", raw_text, re.DOTALL | re.IGNORECASE)
        yazilim_m = re.search(r"YAZILIM:\s*(.*?)(?=(?:ARASTIRMA:|SEKTOR:|\Z))", raw_text, re.DOTALL | re.IGNORECASE)
        arastirma_m = re.search(r"ARASTIRMA:\s*(.*?)(?=(?:SEKTOR:|YAZILIM:|\Z))", raw_text, re.DOTALL | re.IGNORECASE)

        sektor = sektor_m.group(1).strip() if sektor_m else ""
        yazilim = yazilim_m.group(1).strip() if yazilim_m else ""
        arastirma = arastirma_m.group(1).strip() if arastirma_m else ""

        if not (sektor or yazilim or arastirma):
            clean_lines = [l.strip("- *#") for l in raw_text.splitlines() if len(l.strip()) > 20]
            sektor = clean_lines[0] if len(clean_lines) > 0 else "Günün teknoloji gelişmeleri analiz edildi."
            yazilim = clean_lines[1] if len(clean_lines) > 1 else "Açık kaynak projelerinde hareketlilik sürdü."
            arastirma = clean_lines[2] if len(clean_lines) > 2 else "Yapay zeka araştırmalarında yeni modeller sunuldu."

        logger.info("Successfully synthesized Gemini AI Executive Briefing.")
        return ExecutiveBriefing(
            sector_events=sektor,
            software_opensource=yazilim,
            ai_research=arastirma,
            generated_by_ai=True
        )
