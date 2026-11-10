"""
README updater module.
Synchronizes daily highlights and 7-day rolling archive into README.md markers.
"""

from pathlib import Path
import re

from src.config import README_PATH, REPORTS_DIR, ARCHIVE_DISPLAY_DAYS
from src.logging_config import logger
from src.models import ArxivPaper, SourceStatus, TrendItem


class ReadmeUpdater:
    """Updates README.md dynamic section with the latest pipeline outputs."""

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
        arxiv_items: list[ArxivPaper],
        hn_status: SourceStatus = SourceStatus.SUCCESS,
        arxiv_status: SourceStatus = SourceStatus.SUCCESS
    ) -> str:
        """Renders the markdown content between the marker tags."""
        status_banner = ""
        if hn_status != SourceStatus.SUCCESS or arxiv_status != SourceStatus.SUCCESS:
            status_banner = "\n> ⚠️ **Sistem Durumu:** Kısmi veri akışı tespit edildi (ArXiv/HN kaynak durumu izleniyor)."

        # HackerNews rows (top 5)
        if hn_items:
            hn_rows = []
            for item in hn_items[:5]:
                hn_rows.append(
                    f"| `{item.category}` | [{item.title}]({item.url}) | ⭐ {item.points} | 💬 {item.comments} | [Tartışma]({item.hn_url}) |"
                )
            hn_content = "\n".join(hn_rows)
        else:
            hn_content = "*HackerNews verisi geçici olarak alınamadı.*"

        # ArXiv list (top 3)
        if arxiv_items:
            arxiv_rows = []
            for paper in arxiv_items[:3]:
                ref_label = " *(Referans Arşiv)*" if paper.is_archived_fallback else ""
                author_info = f" *(Yazarlar: {paper.authors})*" if paper.authors else ""
                arxiv_rows.append(
                    f"- 📄 **[{paper.title}]({paper.link})** `{paper.category}`{ref_label}{author_info}\n"
                    f"  *📅 Yayın: {paper.published_date}* — {paper.summary}"
                )
            arxiv_content = "\n\n".join(arxiv_rows)
        else:
            arxiv_content = "*ArXiv araştırma verisi geçici olarak alınamadı.*"

        archive_content = self.get_recent_archive_links(date_str)

        return f"""<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `{date_str}`

> 📊 **Bugünün Özeti:** {len(hn_items)} yüksek nitelikli teknoloji trendi ve {len(arxiv_items)} ArXiv AI/ML akademik makalesi tarandı.{status_banner}  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/{date_str}.md`)](reports/{date_str}.md)

#### 🔥 HackerNews Öne Çıkanlar
| Kategori | Başlık | Puan | Yorum | HN Linki |
|:--------:|--------|:----:|:-----:|:--------:|
{hn_content}

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
{arxiv_content}

#### 🗄️ Son 7 Günün Rapor Arşivi
{archive_content}
<!-- LATEST_REPORT_END -->"""

    def update(
        self,
        date_str: str,
        hn_items: list[TrendItem],
        arxiv_items: list[ArxivPaper],
        hn_status: SourceStatus = SourceStatus.SUCCESS,
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

        new_block = self.render_block(date_str, hn_items, arxiv_items, hn_status, arxiv_status)
        updated_text = pattern.sub(new_block, readme_text)

        self.readme_path.write_text(updated_text, encoding="utf-8")
        logger.info(f"README.md dynamic block successfully updated for {date_str}.")
        return True
