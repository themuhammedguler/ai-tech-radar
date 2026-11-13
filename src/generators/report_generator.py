"""
Report generator module.
Builds beautifully structured, professional Markdown reports with health status,
provenance indicators, and comprehensive metadata.
"""

from pathlib import Path
from src.config import REPORTS_DIR
from src.logging_config import logger
from src.models import ArxivPaper, SourceStatus, TrendItem


class ReportGenerator:
    """Generates daily radar markdown report files."""

    def __init__(self, reports_dir: Path = REPORTS_DIR):
        self.reports_dir = reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown(
        self,
        date_str: str,
        hn_items: list[TrendItem],
        arxiv_items: list[ArxivPaper],
        hn_status: SourceStatus = SourceStatus.SUCCESS,
        arxiv_status: SourceStatus = SourceStatus.SUCCESS
    ) -> str:
        """Constructs markdown content string for a daily report."""
        lines = [
            f"# AI & Tech Daily Radar — {date_str}",
            "",
            f"> **Tarih:** {date_str} | **Kapsam:** Yüksek Nitelikli Teknoloji & AI Trendleri",
            "",
            "---",
            "",
            "## 🔥 HackerNews Günün Öne Çıkan Teknoloji Gelişmeleri",
            ""
        ]

        if hn_status == SourceStatus.FAILED or not hn_items:
            lines.extend([
                "> ⚠️ *HackerNews API verisine geçici olarak ulaşılamadı veya uygun kriterde haber bulunamadı.*",
                ""
            ])
        else:
            lines.extend([
                "| # | Kategori | Başlık | Puan | Yorum | Bağlantılar |",
                "|---|:--------:|--------|:----:|:-----:|:-----------:|",
            ])
            for idx, item in enumerate(hn_items, 1):
                lines.append(
                    f"| {idx} | `{item.category}` | [{item.title}]({item.url}) | ⭐ {item.points} | 💬 {item.comments} | [Haber]({item.url}) · [HN Tartışması]({item.hn_url}) |"
                )
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 🤖 En Güncel Yapay Zeka & Makine Öğrenimi Araştırmaları (ArXiv)",
            ""
        ])

        if arxiv_status == SourceStatus.FAILED or not arxiv_items:
            lines.extend([
                "> ⚠️ *ArXiv API hizmetine şu anda ulaşılamıyor.*",
                ""
            ])
        else:
            # Şeffaflık: Eğer makaleler fallback ise kullanıcıya açıkça bildir
            is_fallback = any(p.is_archived_fallback for p in arxiv_items)
            if is_fallback or arxiv_status == SourceStatus.DEGRADED:
                lines.extend([
                    "> ℹ️ **Bilgilendirme:** ArXiv hafta sonu/tatil takvimi veya servis bakımı nedeniyle yeni makale yayımlamadı. Aşağıda en son tescil edilen öncü araştırmalar referans amacıyla sunulmaktadır.",
                    ""
                ])

            for idx, paper in enumerate(arxiv_items, 1):
                fallback_badge = " *(Referans Arşiv)*" if paper.is_archived_fallback else ""
                lines.extend([
                    f"### {idx}. [{paper.title}]({paper.link}){fallback_badge}",
                    f"- 👥 **Yazarlar:** {paper.authors}",
                    f"- 📅 **Yayın Tarihi:** `{paper.published_date}`",
                    f"- 🏷️ **Kategori:** `{paper.category}`",
                    f"- 🔗 **Bağlantı:** [{paper.link}]({paper.link})",
                    f"- 📝 **Özet:** *{paper.summary}*",
                    ""
                ])

        lines.extend([
            "---",
            "*Bu rapor GitHub Actions üzerinde çalışan otonom veri hattı tarafından otomatik olarak üretilmiştir.*",
            ""
        ])

        return "\n".join(lines)

    def write_report(
        self,
        date_str: str,
        hn_items: list[TrendItem],
        arxiv_items: list[ArxivPaper],
        hn_status: SourceStatus = SourceStatus.SUCCESS,
        arxiv_status: SourceStatus = SourceStatus.SUCCESS
    ) -> Path:
        """Renders and writes daily report to disk, returning the Path."""
        content = self.generate_markdown(date_str, hn_items, arxiv_items, hn_status, arxiv_status)
        report_file = self.reports_dir / f"{date_str}.md"
        report_file.write_text(content, encoding="utf-8")
        logger.info(f"Report successfully written to {report_file}")
        return report_file
