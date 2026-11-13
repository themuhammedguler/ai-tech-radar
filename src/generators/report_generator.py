"""
Report generator module (v4.0).
Builds beautifully structured, professional Markdown reports with:
1. Gemini AI Executive Briefing (3 thematic bullets)
2. HackerNews Top 10 Tech News
3. GitHub Trending Top 5 Open-Source Repositories
4. Hugging Face Daily Papers Top 5 Upvoted AI Papers
5. ArXiv Top 5 Frontier AI/ML Papers
"""

from pathlib import Path
from src.config import REPORTS_DIR
from src.logging_config import logger
from src.models import (
    ArxivPaper,
    ExecutiveBriefing,
    GithubRepoItem,
    HuggingFacePaperItem,
    SourceStatus,
    TrendItem
)


class ReportGenerator:
    """Generates comprehensive daily radar markdown report files."""

    def __init__(self, reports_dir: Path = REPORTS_DIR):
        self.reports_dir = reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown(
        self,
        date_str: str,
        hn_items: list[TrendItem],
        github_items: list[GithubRepoItem],
        hf_items: list[HuggingFacePaperItem],
        arxiv_items: list[ArxivPaper],
        briefing: ExecutiveBriefing | None = None,
        hn_status: SourceStatus = SourceStatus.SUCCESS,
        github_status: SourceStatus = SourceStatus.SUCCESS,
        hf_status: SourceStatus = SourceStatus.SUCCESS,
        arxiv_status: SourceStatus = SourceStatus.SUCCESS
    ) -> str:
        """Constructs markdown content string for a 25-trend daily report."""
        lines = [
            f"# AI & Tech Daily Radar — {date_str}",
            "",
            f"> **Tarih:** {date_str} | **Kapsam:** 25 Seçkin Teknoloji Trendi + Yapay Zeka Özeti",
            "",
            "---",
            "",
            "## 🧠 Günün Yapay Zeka Özeti (Executive Briefing)",
            ""
        ]

        if briefing:
            lines.extend([
                f"> 🌐 **Sektör & Büyük Olaylar:** {briefing.sector_events}  ",
                f"> 🛠️ **Yazılım & Açık Kaynak:** {briefing.software_opensource}  ",
                f"> 🔬 **Yapay Zeka & Araştırma:** {briefing.ai_research}",
                ""
            ])
            if briefing.disclaimer:
                lines.extend([f"> {briefing.disclaimer}", ""])
        else:
            lines.extend([
                "> *Yapay zeka yönetici özeti oluşturulamadı.*",
                ""
            ])

        # HackerNews Section
        lines.extend([
            "---",
            "",
            "## 🔥 HackerNews Günün Öne Çıkan 10 Teknoloji Haberi",
            ""
        ])
        if hn_status == SourceStatus.FAILED or not hn_items:
            lines.extend(["> ⚠️ *HackerNews verilerine geçici olarak ulaşılamadı.*", ""])
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

        # GitHub Trending Section
        lines.extend([
            "---",
            "",
            "## ⭐ GitHub Trending: En Popüler 5 Açık Kaynak Proje",
            ""
        ])
        if github_status == SourceStatus.FAILED or not github_items:
            lines.extend(["> ⚠️ *GitHub trending verilerine geçici olarak ulaşılamadı.*", ""])
        else:
            lines.extend([
                "| # | Proje / Araç | Dil | Yıldız | Fork | Açıklama |",
                "|---|--------------|:---:|:------:|:----:|----------|",
            ])
            for idx, repo in enumerate(github_items, 1):
                clean_desc = repo.description[:100] + ("..." if len(repo.description) > 100 else "")
                lines.append(
                    f"| {idx} | [**{repo.name}**]({repo.url}) | `{repo.language}` | ⭐ {repo.stars:,} | 🍴 {repo.forks:,} | {clean_desc} |"
                )
            lines.append("")

        # Hugging Face Daily Papers Section
        lines.extend([
            "---",
            "",
            "## 🤗 Hugging Face Daily Papers: Topluluğun En Çok Oyladığı 5 AI Makalesi",
            ""
        ])
        if hf_status == SourceStatus.FAILED or not hf_items:
            lines.extend(["> ⚠️ *Hugging Face Daily Papers verilerine geçici olarak ulaşılamadı.*", ""])
        else:
            lines.extend([
                "| # | Makale | Oy | Yorum | Yazarlar | Detay |",
                "|---|--------|:--:|:-----:|:--------:|:-----:|",
            ])
            for idx, hf_p in enumerate(hf_items, 1):
                lines.append(
                    f"| {idx} | [{hf_p.title}]({hf_p.url}) | 🔺 {hf_p.upvotes} | 💬 {hf_p.num_comments} | {hf_p.authors} | [HF Makale Sayfası]({hf_p.url}) |"
                )
            lines.append("")

        # ArXiv Section
        lines.extend([
            "---",
            "",
            "## 🤖 ArXiv: En Güncel 5 Yapay Zeka & Makine Öğrenimi Araştırması",
            ""
        ])
        if arxiv_status == SourceStatus.FAILED or not arxiv_items:
            lines.extend(["> ⚠️ *ArXiv API hizmetine şu anda ulaşılamıyor.*", ""])
        else:
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
        github_items: list[GithubRepoItem],
        hf_items: list[HuggingFacePaperItem],
        arxiv_items: list[ArxivPaper],
        briefing: ExecutiveBriefing | None = None,
        hn_status: SourceStatus = SourceStatus.SUCCESS,
        github_status: SourceStatus = SourceStatus.SUCCESS,
        hf_status: SourceStatus = SourceStatus.SUCCESS,
        arxiv_status: SourceStatus = SourceStatus.SUCCESS
    ) -> Path:
        """Renders and writes daily report to disk, returning the Path."""
        content = self.generate_markdown(
            date_str=date_str,
            hn_items=hn_items,
            github_items=github_items,
            hf_items=hf_items,
            arxiv_items=arxiv_items,
            briefing=briefing,
            hn_status=hn_status,
            github_status=github_status,
            hf_status=hf_status,
            arxiv_status=arxiv_status
        )
        report_file = self.reports_dir / f"{date_str}.md"
        report_file.write_text(content, encoding="utf-8")
        logger.info(f"Report successfully written to {report_file}")
        return report_file
