"""
README updater module (v4.0).
Synchronizes daily AI executive briefing, 25-trend cross-platform highlights,
and rolling 7-day archive into README.md markers.
"""

from pathlib import Path
import re

from src.config import ARCHIVE_DISPLAY_DAYS, README_PATH, REPORTS_DIR
from src.logging_config import logger
from src.models import (
    ArxivPaper,
    ExecutiveBriefing,
    GithubRepoItem,
    HuggingFacePaperItem,
    SourceStatus,
    TrendItem
)


class ReadmeUpdater:
    """Updates README.md dynamic section with the latest multi-source radar outputs."""

    def __init__(self, readme_path: Path = README_PATH, reports_dir: Path = REPORTS_DIR):
        self.readme_path = readme_path
        self.reports_dir = reports_dir

    def get_recent_archive_links(self, current_date: str, days: int = ARCHIVE_DISPLAY_DAYS) -> str:
        """Collects markdown links for the last N reports."""
        if not self.reports_dir.exists():
            return f"- [📅 {current_date} Raporu](reports/{current_date}.md)"

        report_files = sorted(self.reports_dir.glob("*.md"), reverse=True)
        recent_files = report_files[:days]

        if not recent_files:
            return f"- [📅 {current_date} Raporu](reports/{current_date}.md)"

        lines = [f"- [📅 {f.stem} Raporu](reports/{f.name})" for f in recent_files]
        return "\n".join(lines)

    def render_block(
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
        """Renders the markdown content between the marker tags."""
        total_count = len(hn_items) + len(github_items) + len(hf_items) + len(arxiv_items)

        # 1. Executive Briefing
        briefing_lines = []
        if briefing:
            briefing_lines.extend([
                f"- 🌐 **Sektör & Büyük Olaylar:** {briefing.sector_events}",
                f"- 🛠️ **Yazılım & Açık Kaynak:** {briefing.software_opensource}",
                f"- 🔬 **Yapay Zeka & Araştırma:** {briefing.ai_research}"
            ])
            if briefing.disclaimer:
                briefing_lines.append(f"  {briefing.disclaimer}")
        else:
            briefing_lines.append("- *Yönetici özeti henüz oluşturulmadı.*")
        briefing_content = "\n".join(briefing_lines)

        # 2. HackerNews (Top 5)
        if hn_items:
            hn_rows = []
            for item in hn_items[:5]:
                hn_rows.append(
                    f"| `{item.category}` | [{item.title}]({item.url}) | ⭐ {item.points} | 💬 {item.comments} | [Tartışma]({item.hn_url}) |"
                )
            hn_content = "\n".join(hn_rows)
        else:
            hn_content = "*HackerNews verisi geçici olarak alınamadı.*"

        # 3. GitHub Trending (Top 3)
        if github_items:
            gh_rows = []
            for repo in github_items[:3]:
                desc = repo.description[:80] + ("..." if len(repo.description) > 80 else "")
                gh_rows.append(
                    f"| [**{repo.name}**]({repo.url}) | `{repo.language}` | ⭐ {repo.stars:,} | {desc} |"
                )
            gh_content = "\n".join(gh_rows)
        else:
            gh_content = "*GitHub trending verisi geçici olarak alınamadı.*"

        # 4. Hugging Face & ArXiv Highlights
        research_items = []
        for hf_p in hf_items[:2]:
            research_items.append(
                f"- 🤗 **[{hf_p.title}]({hf_p.url})** `HuggingFace` *(🔺 {hf_p.upvotes} oy · {hf_p.authors})*\n  {hf_p.summary}"
            )
        for ax_p in arxiv_items[:2]:
            ref_badge = " *(Referans Arşiv)*" if ax_p.is_archived_fallback else ""
            research_items.append(
                f"- 🤖 **[{ax_p.title}]({ax_p.link})** `{ax_p.category}`{ref_badge} *(Yazarlar: {ax_p.authors})*\n  *📅 Yayın: {ax_p.published_date}* — {ax_p.summary}"
            )
        research_content = "\n\n".join(research_items) if research_items else "*Araştırma verisi geçici olarak alınamadı.*"

        archive_content = self.get_recent_archive_links(date_str)

        return f"""<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `{date_str}`

> 📊 **Bugünün Özeti:** 25 teknoloji trendi ({len(hn_items)} HackerNews + {len(github_items)} GitHub + {len(hf_items)} Hugging Face + {len(arxiv_items)} ArXiv) tarandı.  
> 📑 **Tam Rapor:** [Günün 25 Maddelik Raporunu Görüntüle (`reports/{date_str}.md`)](reports/{date_str}.md)

#### 🧠 Günün Yapay Zeka Özeti (Executive Briefing)
{briefing_content}

#### 🔥 HackerNews Öne Çıkanlar
| Kategori | Başlık | Puan | Yorum | HN Linki |
|:--------:|--------|:----:|:-----:|:--------:|
{hn_content}

#### ⭐ GitHub Trending Açık Kaynak Projeler
| Proje | Dil | Yıldız | Açıklama |
|-------|:---:|:------:|----------|
{gh_content}

#### 🔬 Öne Çıkan AI & Model Araştırmaları (Hugging Face & ArXiv)
{research_content}

#### 🗄️ Son 7 Günün Rapor Arşivi
{archive_content}
<!-- LATEST_REPORT_END -->"""

    def update(
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
    ) -> bool:
        """Replaces the content between markers in README.md."""
        if not self.readme_path.exists():
            raise FileNotFoundError(f"README.md not found at {self.readme_path}")

        readme_text = self.readme_path.read_text(encoding="utf-8")
        pattern = re.compile(r"<!-- LATEST_REPORT_START -->[\s\S]*?<!-- LATEST_REPORT_END -->")

        if not pattern.search(readme_text):
            raise ValueError(
                "Marker tags <!-- LATEST_REPORT_START --> and <!-- LATEST_REPORT_END --> not found in README.md"
            )

        new_block = self.render_block(
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
        updated_text = pattern.sub(new_block, readme_text)

        self.readme_path.write_text(updated_text, encoding="utf-8")
        logger.info(f"README.md dynamic block successfully updated for {date_str}.")
        return True
