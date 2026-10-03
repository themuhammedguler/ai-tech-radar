#!/usr/bin/env python3
"""
AI & Tech Daily Radar - Autonomous Data Pipeline
HackerNews & ArXiv trendlerini otonom olarak toplayan, günlük rapor üreten
ve README.md dosyasını güncelleyen Python veri hattı betiği.
"""

import os
import sys
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
import requests

# Sabitler ve API Uç Noktaları
HN_API_URL = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10"
ARXIV_API_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=5"
REQUEST_TIMEOUT = 20  # saniye


def fetch_hackernews_trends(limit: int = 10) -> list[dict]:
    """
    HackerNews Algolia API üzerinden günün en popüler teknoloji haberlerini çeker.
    """
    print(f"[*] HackerNews trendleri çekiliyor (Limit: {limit})...")
    url = f"https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={limit}"
    headers = {"User-Agent": "AITechRadar/1.0 (+https://github.com)"}

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[!] HackerNews verisi çekilirken hata oluştu: {e}", file=sys.stderr)
        return []

    hits = data.get("hits", [])
    trends = []

    for hit in hits[:limit]:
        title = hit.get("title") or hit.get("story_title") or "Başlıksız Gönderi"
        object_id = hit.get("objectID", "")
        hn_url = f"https://news.ycombinator.com/item?id={object_id}"
        story_url = hit.get("url") or hn_url
        points = hit.get("points") or 0
        num_comments = hit.get("num_comments") or 0

        # Tablo formatını bozmaması için başlık içindeki dik çizgileri (|) temizle
        safe_title = title.replace("|", "-").strip()

        trends.append({
            "title": safe_title,
            "url": story_url,
            "hn_url": hn_url,
            "points": points,
            "num_comments": num_comments,
        })

    print(f"[+] {len(trends)} HackerNews gönderisi başarıyla alındı.")
    return trends


def fetch_arxiv_papers(limit: int = 5) -> list[dict]:
    """
    ArXiv API üzerinden en güncel cs.AI ve cs.LG makalelerini çeker ve XML olarak ayrıştırır.
    """
    print(f"[*] ArXiv güncel makaleleri çekiliyor (Limit: {limit})...")
    url = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results={limit}"
    headers = {"User-Agent": "AITechRadar/1.0 (+https://github.com)"}

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        root = ET.fromstring(response.content)
    except Exception as e:
        print(f"[!] ArXiv verisi çekilirken hata oluştu: {e}", file=sys.stderr)
        return []

    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []

    for entry in root.findall("atom:entry", namespace)[:limit]:
        title_elem = entry.find("atom:title", namespace)
        summary_elem = entry.find("atom:summary", namespace)
        id_elem = entry.find("atom:id", namespace)

        raw_title = title_elem.text if title_elem is not None and title_elem.text else "Başlıksız Makale"
        raw_summary = summary_elem.text if summary_elem is not None and summary_elem.text else "Özet bulunamadı."
        link = id_elem.text.strip() if id_elem is not None and id_elem.text else "#"

        # Boşlukları ve satır sonlarını temizle
        clean_title = re.sub(r"\s+", " ", raw_title).strip()
        clean_title = clean_title.replace("|", "-")

        clean_summary = re.sub(r"\s+", " ", raw_summary).strip()
        summary_200 = clean_summary[:200].strip() + ("..." if len(clean_summary) > 200 else "")
        summary_200 = summary_200.replace("|", "-")

        papers.append({
            "title": clean_title,
            "summary": summary_200,
            "link": link
        })

    print(f"[+] {len(papers)} ArXiv makalesi başarıyla alındı.")
    return papers


def generate_report_markdown(date_str: str, hn_items: list[dict], arxiv_items: list[dict]) -> str:
    """
    Günün verilerini Markdown raporu formatında derler.
    """
    lines = [
        f"# 📡 AI & Tech Daily Radar — {date_str}",
        "",
        f"> **Tarih:** {date_str} | **Veri Kaynakları:** HackerNews Front Page & ArXiv cs.AI/cs.LG",
        "",
        "---",
        "",
        "## 🔥 HackerNews Günün En Popüler 10 Teknoloji Haberi",
        "",
        "| # | Başlık | Puan | Yorum | Kaynak | Tartışma |",
        "|---|--------|:----:|:-----:|:------:|:--------:|",
    ]

    for idx, item in enumerate(hn_items, 1):
        lines.append(
            f"| {idx} | [{item['title']}]({item['url']}) | ⭐ {item['points']} | 💬 {item['num_comments']} | [Haber Linki]({item['url']}) | [HN Tartışması]({item['hn_url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🤖 En Güncel 5 Yapay Zeka & Makine Öğrenimi Makalesi (ArXiv)",
        "",
    ])

    for idx, paper in enumerate(arxiv_items, 1):
        lines.extend([
            f"### {idx}. [{paper['title']}]({paper['link']})",
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
    en güncel rapor özeti ve son 7 günün arşiv linkleriyle günceller.
    """
    readme_path = base_dir / "README.md"
    reports_dir = base_dir / "reports"

    if not readme_path.exists():
        print(f"[!] README.md bulunamadı: {readme_path}", file=sys.stderr)
        return

    # reports/ klasöründeki raporları alıp tarihe göre ters sırala
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
        hn_table_rows.append(f"| [{item['title']}]({item['url']}) | ⭐ {item['points']} | 💬 {item['num_comments']} | [Tartışma]({item['hn_url']}) |")
    hn_table_content = "\n".join(hn_table_rows)

    # Öne çıkan ArXiv listesi (ilk 3 tanesi)
    arxiv_rows = []
    for paper in arxiv_items[:3]:
        arxiv_rows.append(f"- 📄 **[{paper['title']}]({paper['link']})**\n  *{paper['summary']}*")
    arxiv_content = "\n\n".join(arxiv_rows)

    latest_block_content = f"""<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `{date_str}`

> 📊 **Bugünün Özeti:** 10 HackerNews teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/{date_str}.md`)](reports/{date_str}.md)

#### 🔥 HackerNews Öne Çıkanlar
| Başlık | Puan | Yorum | HN Linki |
|--------|:----:|:-----:|:--------:|
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
        print("[!] README.md içinde <!-- LATEST_REPORT_START --> ve <!-- LATEST_REPORT_END --> etiketleri bulunamadı!", file=sys.stderr)
        return

    updated_readme = pattern.sub(latest_block_content, readme_text)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_readme)

    print(f"[+] README.md başarıyla güncellendi ({date_str} özeti ve arşiv eklendi).")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Bugünün tarihi (UTC standart veya yerel tarih)
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"=== AI & Tech Daily Radar Pipeline Başlatıldı: {today_str} ===")

    # 1. Verileri Çek
    hn_trends = fetch_hackernews_trends(limit=10)
    arxiv_papers = fetch_arxiv_papers(limit=5)

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
