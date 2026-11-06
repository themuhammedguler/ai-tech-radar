#!/usr/bin/env python3
"""
AI & Tech Daily Radar - Autonomous Data Pipeline (v2.0 Refined)
HackerNews & ArXiv trendlerini otonom olarak toplayan, akıllı gürültü filtresi,
teknoloji önceliklendirme algoritması ve gelişmiş akademik özetleme yetenekleriyle
günlük rapor üreten Python veri hattı.
"""

import os
import sys
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import requests

# Sabitler ve API Uç Noktaları
HN_API_URL = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50"
ARXIV_API_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=8"
REQUEST_TIMEOUT = 25  # saniye

# HackerNews Negatif Filtre (Vefat, İlan, Magazin, Saf Tıp ve Doğa/Kültür Konuları)
NEGATIVE_PATTERNS = [
    r"\bhas died\b", r"\bdies at\b", r"\bpassed away\b", r"\bobituary\b", r"\bdeath of\b",
    r"\bcancer\b", r"\bdentist\b", r"\bdentistry\b", r"\badhd\b", r"\bautism\b",
    r"\bdiet\b", r"\bweight loss\b", r"\bheart attack\b", r"\bdementia\b", r"\balzheimer\b",
    r"\btoddler\b", r"\bparenting\b", r"\bdivorce\b", r"\bdating\b", r"\bmarriage\b",
    r"\belection\b", r"\bsenate\b", r"\bpresident\b", r"\bcongress\b", r"\bdemocrat\b", r"\brepublican\b",
    r"\bis hiring\b", r"\bwho is hiring\b", r"\bwho wants to be hired\b", r"\bhiring:\b"
]

# İstisna: Başlıkta bu terimler varsa (örn. "CNN outperforms LLMs for skin cancer diagnosis") elenmez
STRONG_TECH_EXCEPTIONS = [
    "ai", "llm", "cnn", "model", "deep learning", "machine learning",
    "algorithm", "neural", "dataset", "biotech", "software", "robot", "compute"
]

# Pozitif Teknoloji ve AI Anahtar Kelimeleri (Kategori ve Sinyal Tespiti)
TECH_CATEGORIES = {
    "🤖 AI / ML": [
        "ai", "llm", "agent", "agents", "gpt", "model", "models", "neural", "deep learning", "machine learning",
        "weights", "transformer", "diffusion", "inference", "gpu", "cuda", "nvidia",
        "anthropic", "openai", "gemini", "mistral", "claude", "deepseek", "qwen", "llama",
        "opus", "fine-tuning", "rag", "embedding", "multimodal", "reasoning", "vision",
        "perplexity", "copilot"
    ],
    "🛡️ Güvenlik": [
        "security", "vulnerability", "cve", "exploit", "hack", "hacked", "cyber", "malware",
        "ransomware", "breach", "zero-day", "backdoor", "encryption", "auth", "phishing",
        "infected", "vm escape", "credential", "pwn"
    ],
    "💻 Yazılım & Geliştirme": [
        "software", "programming", "code", "coding", "developer", "open source", "open-source",
        "github", "rust", "python", "javascript", "typescript", "golang", "go 1.", "c++",
        "wasm", "webassembly", "database", "postgres", "sqlite", "redis", "compiler",
        "git", "api", "framework", "library", "testing", "frontend", "backend", "bare-metal",
        "uefi", "runtime", "gui", "ui framework"
    ],
    "⚙️ Sistem & Altyapı": [
        "linux", "kernel", "unix", "cpu", "chip", "semiconductor", "hardware", "server",
        "servers", "cloud", "docker", "kubernetes", "networking", "protocol", "http", "ssh",
        "microvm", "firecracker", "floppy", "storage", "quantum", "robotics", "robot",
        "architecture", "benchmark", "performance", "vm", "vms"
    ]
}


def classify_and_score_story(hit: dict) -> tuple[bool, str, int]:
    """
    HackerNews gönderisini analiz eder:
    - Negatif filtreye takılıyorsa (ve güçlü tech istisnası yoksa) elenir (False).
    - İşe alım ilanlarını veya sıfır etkileşimli reklamları eler.
    - Kategori etiketini ve teknoloji ilgi skorunu döner.
    """
    title = (hit.get("title") or hit.get("story_title") or "").strip()
    url = (hit.get("url") or "").lower()
    points = hit.get("points") or 0
    comments = hit.get("num_comments") or 0
    title_lower = title.lower()

    # İşe alım veya sıfır etkileşimli gönderileri ele
    if points < 10 and comments == 0:
        return False, "Düşük Etkileşim", 0

    # 1. Güçlü teknoloji istisnası kontrolü
    has_strong_tech = any(re.search(rf"\b{re.escape(k)}\b", title_lower) for k in STRONG_TECH_EXCEPTIONS)

    # 2. Negatif filtre kontrolü (Ölüm, magazin, tıp, ilan vb.)
    if not has_strong_tech:
        for pat in NEGATIVE_PATTERNS:
            if re.search(pat, title_lower):
                return False, "Gürültü", 0

    # 3. Kategori belirleme ve ilgi puanı
    matched_category = "⚡ Teknoloji"
    tech_score = 0

    for cat_name, keywords in TECH_CATEGORIES.items():
        cat_matches = 0
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", title_lower):
                cat_matches += 1
        if cat_matches > 0:
            tech_score += cat_matches
            if matched_category == "⚡ Teknoloji":
                matched_category = cat_name

    # Domain bazlı ek sinyal
    tech_domains = ["github.com", "arxiv.org", "huggingface.co", "eff.org", "cve.org", "blog.cloudflare.com", "go.dev"]
    if any(domain in url for domain in tech_domains):
        tech_score += 1
        if matched_category == "⚡ Teknoloji":
            matched_category = "💻 Yazılım & Geliştirme"

    return True, matched_category, tech_score


def fetch_hackernews_trends(limit: int = 10) -> list[dict]:
    """
    HackerNews Algolia API üzerinden 50 gönderi çeker;
    - Alakasız gürültüyü (ölüm, saf sağlık, politika, iş ilanları) eler.
    - Teknoloji ve AI sinyali taşıyan içerikleri en üste yerleştirir.
    - En yüksek nitelikli 10 haberi seçer.
    """
    print(f"[*] HackerNews havuzu taranıyor (50 aday çekiliyor)...")
    headers = {"User-Agent": "AITechRadar/2.0 (+https://github.com)"}

    try:
        response = requests.get(HN_API_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[!] HackerNews verisi çekilirken hata oluştu: {e}", file=sys.stderr)
        return []

    hits = data.get("hits", [])
    verified_tech_items = []
    general_tech_items = []

    for hit in hits:
        is_valid, category, tech_score = classify_and_score_story(hit)
        if not is_valid:
            continue

        title = hit.get("title") or hit.get("story_title") or "Başlıksız Gönderi"
        object_id = hit.get("objectID", "")
        hn_url = f"https://news.ycombinator.com/item?id={object_id}"
        story_url = hit.get("url") or hn_url
        points = hit.get("points") or 0
        num_comments = hit.get("num_comments") or 0

        safe_title = title.replace("|", "-").strip()

        # Sıralama skoru: Gerçek etkileşim + Teknoloji ağırlığı
        ranking_score = points + (tech_score * 120) + (num_comments * 0.4)

        item = {
            "title": safe_title,
            "url": story_url,
            "hn_url": hn_url,
            "points": points,
            "num_comments": num_comments,
            "category": category,
            "tech_score": tech_score,
            "ranking_score": ranking_score
        }

        # Doğrulanmış teknoloji terimleri içerenleri ayrı tut
        if tech_score >= 1:
            verified_tech_items.append(item)
        else:
            general_tech_items.append(item)

    # Önce doğrulanmış teknoloji haberlerini puanına göre sırala
    verified_tech_items.sort(key=lambda x: x["ranking_score"], reverse=True)
    general_tech_items.sort(key=lambda x: x["ranking_score"], reverse=True)

    # İhtiyaç halinde genel haberlerle tamamla
    final_selection = verified_tech_items[:limit]
    if len(final_selection) < limit:
        needed = limit - len(final_selection)
        final_selection.extend(general_tech_items[:needed])

    print(f"[+] Filtrelenmiş {len(final_selection)} yüksek nitelikli teknoloji trendi belirlendi.")
    return final_selection


def extract_smart_summary(raw_summary: str, max_chars: int = 380) -> str:
    """
    Özeti rastgele 200 karakterde kesmek yerine, anlam bütünlüğünü koruyan
    1 ila 3 tam cümle çıkartır.
    """
    text = re.sub(r"\s+", " ", raw_summary).strip()
    text = text.replace("|", "-")

    # Cümleleri son noktalama işaretlerinden ayır
    sentences = re.split(r"(?<=[.!?])\s+", text)
    selected_sentences = []
    current_len = 0

    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        # En az 1 tam cümle al; sonraki cümleler uzunluk limitini aşmıyorsa ekle
        if not selected_sentences or (current_len + len(s_clean) <= max_chars):
            selected_sentences.append(s_clean)
            current_len += len(s_clean) + 1
        else:
            break

    result = " ".join(selected_sentences)
    # Eğer tek bir cümle bile çok uzunsa kelime sınırından kes
    if len(result) > max_chars + 60:
        result = result[:max_chars].rsplit(" ", 1)[0] + "..."

    return result


def fetch_arxiv_papers(limit: int = 5, reports_dir: Path | None = None) -> list[dict]:
    """
    ArXiv API üzerinden en güncel cs.AI, cs.LG ve cs.CL makalelerini çeker.
    Yazarları, akıllı tam cümle özetlerini ve kategorileri ayrıştırır.
    API geçici olarak başarısız olursa önceki rapordan koruma (fallback) sağlar.
    """
    print(f"[*] ArXiv makaleleri çekiliyor (cs.AI, cs.LG, cs.CL)...")
    headers = {"User-Agent": "AITechRadar/2.0 (+https://github.com)"}

    root = None
    # 2 kez deneme (retry) döngüsü
    for attempt in range(1, 3):
        try:
            response = requests.get(ARXIV_API_URL, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            break
        except Exception as e:
            print(f"[!] ArXiv deneme {attempt} başarısız: {e}", file=sys.stderr)
            time.sleep(2)

    papers = []
    namespace = {"atom": "http://www.w3.org/2005/Atom"}

    if root is not None:
        for entry in root.findall("atom:entry", namespace)[:limit]:
            title_elem = entry.find("atom:title", namespace)
            summary_elem = entry.find("atom:summary", namespace)
            id_elem = entry.find("atom:id", namespace)

            raw_title = title_elem.text if title_elem is not None and title_elem.text else "Başlıksız Makale"
            raw_summary = summary_elem.text if summary_elem is not None and summary_elem.text else "Özet bulunamadı."
            link = id_elem.text.strip() if id_elem is not None and id_elem.text else "#"

            clean_title = re.sub(r"\s+", " ", raw_title).strip().replace("|", "-")
            smart_summary = extract_smart_summary(raw_summary)

            # Yazarların ilk 3 tanesini al
            author_elems = entry.findall("atom:author", namespace)
            authors = [a.find("atom:name", namespace).text for a in author_elems if a.find("atom:name", namespace) is not None]
            authors_str = ", ".join(authors[:3]) + (" vb." if len(authors) > 3 else "")

            # Kategori etiketi
            category_elem = entry.find("{http://arxiv.org/schemas/atom}primary_category")
            category_tag = category_elem.attrib.get("term", "cs.AI") if category_elem is not None else "cs.AI"

            papers.append({
                "title": clean_title,
                "summary": smart_summary,
                "link": link,
                "authors": authors_str or "Bilinmeyen Araştırmacılar",
                "category": category_tag
            })

    # Hafta sonu veya API kesintisi durumunda Fallback (Önceki günden kurtarma)
    if not papers and reports_dir and reports_dir.exists():
        print("[!] ArXiv boş döndü, son başarılı rapor inceleniyor (Fallback)...")
        past_reports = sorted(reports_dir.glob("*.md"), reverse=True)
        for r_path in past_reports:
            content = r_path.read_text(encoding="utf-8")
            matches = re.findall(
                r"###\s*\d+\.\s*\[(.*?)\]\((.*?)\)\s*\n-\s*👥\s*\*\*Yazarlar:\*\*\s*(.*?)\s*\n-\s*🏷️\s*\*\*Kategori:\*\*\s*(.*?)\s*\n-\s*🔗\s*\*\*Bağlantı:\*\*\s*.*?\n-\s*📝\s*\*\*Özet:\*\*\s*\*(.*?)\*",
                content
            )
            if matches:
                for m in matches[:limit]:
                    papers.append({
                        "title": m[0],
                        "link": m[1],
                        "authors": m[2],
                        "category": m[3],
                        "summary": m[4]
                    })
                print(f"[+] Fallback: {r_path.name} dosyasından {len(papers)} makale başarıyla korundu.")
                break

    print(f"[+] {len(papers)} ArXiv makalesi hazırlandı.")
    return papers


def generate_report_markdown(date_str: str, hn_items: list[dict], arxiv_items: list[dict]) -> str:
    """
    Günün verilerini zengin Markdown raporu formatında derler.
    """
    lines = [
        f"# 📡 AI & Tech Daily Radar — {date_str}",
        "",
        f"> **Tarih:** {date_str} | **Kapsam:** Yüksek Nitelikli Teknoloji & AI Trendleri",
        "",
        "---",
        "",
        "## 🔥 HackerNews Günün Öne Çıkan Teknoloji Gelişmeleri",
        "",
        "| # | Kategori | Başlık | Puan | Yorum | Bağlantılar |",
        "|---|:--------:|--------|:----:|:-----:|:-----------:|",
    ]

    for idx, item in enumerate(hn_items, 1):
        lines.append(
            f"| {idx} | `{item.get('category', '⚡ Teknoloji')}` | [{item['title']}]({item['url']}) | ⭐ {item['points']} | 💬 {item['num_comments']} | [Haber]({item['url']}) · [HN Tartışması]({item['hn_url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🤖 En Güncel Yapay Zeka & Makine Öğrenimi Araştırmaları (ArXiv)",
        "",
    ])

    for idx, paper in enumerate(arxiv_items, 1):
        lines.extend([
            f"### {idx}. [{paper['title']}]({paper['link']})",
            f"- 👥 **Yazarlar:** {paper.get('authors', 'Bilinmiyor')}",
            f"- 🏷️ **Kategori:** `{paper.get('category', 'cs.AI')}`",
            f"- 🔗 **Bağlantı:** [{paper['link']}]({paper['link']})",
            f"- 📝 **Özet:** *{paper['summary']}*",
            "",
        ])

    lines.extend([
        "---",
        "*Bu rapor GitHub Actions üzerinde çalışan otonom veri hattı tarafından otomatik olarak üretilmiştir.*",
        ""
    ])

    return "\n".join(lines)


def update_readme(date_str: str, hn_items: list[dict], arxiv_items: list[dict], base_dir: Path):
    """
    README.md dosyasındaki <!-- LATEST_REPORT_START --> ve <!-- LATEST_REPORT_END --> etiketleri arasını
    en güncel özet ve son 7 günün arşiv linkleriyle günceller.
    """
    readme_path = base_dir / "README.md"
    reports_dir = base_dir / "reports"

    if not readme_path.exists():
        print(f"[!] README.md bulunamadı: {readme_path}", file=sys.stderr)
        return

    report_files = sorted(reports_dir.glob("*.md"), reverse=True)
    recent_reports = report_files[:7]

    archive_lines = []
    if recent_reports:
        for r_file in recent_reports:
            r_date = r_file.stem
            archive_lines.append(f"- [📅 {r_date} Raporu](reports/{r_file.name})")
    else:
        archive_lines.append(f"- [📅 {date_str} Raporu](reports/{date_str}.md)")

    archive_markdown = "\n".join(archive_lines)

    # Öne çıkan HackerNews tablosu (ilk 5 tanesi)
    hn_table_rows = []
    for item in hn_items[:5]:
        cat = item.get("category", "⚡ Teknoloji")
        hn_table_rows.append(f"| `{cat}` | [{item['title']}]({item['url']}) | ⭐ {item['points']} | 💬 {item['num_comments']} | [Tartışma]({item['hn_url']}) |")
    hn_table_content = "\n".join(hn_table_rows)

    # Öne çıkan ArXiv listesi (ilk 3 tanesi)
    arxiv_rows = []
    for paper in arxiv_items[:3]:
        cat = paper.get('category', 'cs.AI')
        authors = paper.get('authors', '')
        author_info = f" *(Yazarlar: {authors})*" if authors else ""
        arxiv_rows.append(
            f"- 📄 **[{paper['title']}]({paper['link']})** `{cat}`{author_info}\n  *{paper['summary']}*"
        )
    arxiv_content = "\n\n".join(arxiv_rows)

    latest_block_content = f"""<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `{date_str}`

> 📊 **Bugünün Özeti:** 10 yüksek nitelikli teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/{date_str}.md`)](reports/{date_str}.md)

#### 🔥 HackerNews Öne Çıkanlar
| Kategori | Başlık | Puan | Yorum | HN Linki |
|:--------:|--------|:----:|:-----:|:--------:|
{hn_table_content}

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
{arxiv_content}

#### 🗄️ Son 7 Günün Rapor Arşivi
{archive_markdown}
<!-- LATEST_REPORT_END -->"""

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_text = f.read()

    pattern = re.compile(r"<!-- LATEST_REPORT_START -->[\s\S]*?<!-- LATEST_REPORT_END -->")
    if not pattern.search(readme_text):
        print("[!] README.md içinde etiketler bulunamadı!", file=sys.stderr)
        return

    updated_readme = pattern.sub(latest_block_content, readme_text)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_readme)

    print(f"[+] README.md başarıyla güncellendi ({date_str} özeti ve arşiv eklendi).")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"=== AI & Tech Daily Radar Pipeline Başlatıldı: {today_str} ===")

    # 1. Verileri Çek
    hn_trends = fetch_hackernews_trends(limit=10)
    arxiv_papers = fetch_arxiv_papers(limit=5, reports_dir=reports_dir)

    # 2. Günlük Rapor Dosyasını Oluştur
    report_md = generate_report_markdown(today_str, hn_trends, arxiv_papers)
    report_path = reports_dir / f"{today_str}.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[+] Günlük rapor dosyası oluşturuldu: {report_path.relative_to(base_dir)}")

    # 3. README.md Dosyasını Güncelle
    update_readme(today_str, hn_trends, arxiv_papers, base_dir)

    print("=== Pipeline Başarıyla Tamamlandı ===")


if __name__ == "__main__":
    main()
