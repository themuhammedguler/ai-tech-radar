"""
AI Summarizer processor.
Uses Google Gemini Flash REST API to synthesize the day's 25 collected trends
into a crisp 3-bullet Turkish Executive Briefing (TL;DR).
Implements resilient fallback when API key is missing or quota is exhausted.
"""

import json
import os
import re
from typing import Optional
import requests

from src.config import (
    GEMINI_API_KEY_ENV,
    GEMINI_API_URL,
    GEMINI_FALLBACK_URL,
    DEFAULT_TIMEOUT
)
from src.logging_config import logger
from src.models import (
    ArxivPaper,
    ExecutiveBriefing,
    GithubRepoItem,
    HuggingFacePaperItem,
    TrendItem
)


class AiSummarizer:
    """Generates structured daily executive briefings using Google Gemini API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        primary_url: str = GEMINI_API_URL,
        fallback_url: str = GEMINI_FALLBACK_URL,
        timeout: tuple[float, float] = DEFAULT_TIMEOUT
    ):
        self.api_key = api_key or os.getenv(GEMINI_API_KEY_ENV)
        self.primary_url = primary_url
        self.fallback_url = fallback_url
        self.timeout = timeout

    def _build_prompt(
        self,
        hn_items: list[TrendItem],
        github_items: list[GithubRepoItem],
        hf_items: list[HuggingFacePaperItem],
        arxiv_items: list[ArxivPaper]
    ) -> str:
        """Constructs a compact context prompt summarizing all 25 trends."""
        lines = [
            "Aşağıda bugün teknoloji ve yapay zeka dünyasında öne çıkan 25 gelişme bulunmaktadır:\n",
            "### HackerNews Trendleri:"
        ]
        for it in hn_items[:10]:
            lines.append(f"- {it.title} (Kategori: {it.category}, Puan: {it.points})")

        lines.append("\n### GitHub Trending Açık Kaynak Repolar:")
        for gh in github_items[:5]:
            lines.append(f"- {gh.name} ({gh.language}, ⭐{gh.stars}): {gh.description}")

        lines.append("\n### Hugging Face Popüler AI Makaleleri:")
        for hf in hf_items[:5]:
            lines.append(f"- {hf.title} (Oy: {hf.upvotes}): {hf.summary[:150]}")

        lines.append("\n### ArXiv Araştırmaları:")
        for ax in arxiv_items[:5]:
            lines.append(f"- {ax.title} ({ax.category}): {ax.summary[:150]}")

        lines.append("""
GÖREV:
Bu 25 veriyi bir teknoloji analisti gözüyle sentezle ve Türkçe olarak tam 3 tematik madde halinde günlük yönetici brifingi (Executive TL;DR) oluştur.
Her madde 1-2 akıcı ve bilgilendirici cümleden oluşmalıdır.

Format kesinlikle şu şekilde olmalıdır:
SEKTOR: [Teknoloji dünyasındaki büyük olaylar, şirketler, güvenlik veya regülasyonlar hakkında sentez]
YAZILIM: [Açık kaynak dünyası, geliştirici araçları, diller ve altyapı projeleri hakkında sentez]
ARASTIRMA: [Yapay zeka modelleri, araştırma makaleleri ve mimari yenilikler hakkında sentez]
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
        """Sends prompt to Gemini REST API and returns raw text response."""
        if not self.api_key:
            logger.info("GEMINI_API_KEY not found in environment. Using graceful fallback.")
            return None

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 600
            }
        }

        # Try primary URL then fallback URL
        urls = [self.primary_url, self.fallback_url]
        for url in urls:
            try:
                target_endpoint = f"{url}?key={self.api_key}"
                logger.info(f"Generating AI Executive Briefing via Gemini API...")
                resp = requests.post(target_endpoint, json=payload, timeout=self.timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                else:
                    logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text[:150]}")
            except Exception as e:
                logger.warning(f"Gemini API call failed on {url}: {e}")

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
            # If markers were not strictly followed, split lines
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
