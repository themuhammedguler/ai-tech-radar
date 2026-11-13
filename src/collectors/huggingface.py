"""
Hugging Face Daily Papers collector.
Queries Hugging Face's Daily Papers API to track the most upvoted and discussed
AI models and research papers in the machine learning community.
"""

from typing import Any
import requests

from src.collectors.base import BaseCollector
from src.config import HUGGINGFACE_DAILY_PAPERS_URL, HUGGINGFACE_TARGET_COUNT
from src.logging_config import logger
from src.models import HuggingFacePaperItem, SourceStatus
from src.processors.text_summarizer import extract_smart_summary


class HuggingFaceCollector(BaseCollector):
    """Collects top community-curated papers from Hugging Face Daily Papers."""

    def __init__(
        self,
        api_url: str = HUGGINGFACE_DAILY_PAPERS_URL,
        target_count: int = HUGGINGFACE_TARGET_COUNT,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.api_url = api_url
        self.target_count = target_count

    def collect(self) -> list[HuggingFacePaperItem]:
        """
        Fetches daily papers, sorts by community engagement (upvotes),
        and returns validated HuggingFacePaperItem instances.
        """
        logger.info(f"Querying Hugging Face Daily Papers API...")

        try:
            response = self.get(self.api_url)
            data = response.json()
        except requests.RequestException as e:
            self.status = SourceStatus.FAILED
            logger.error(f"Hugging Face API request failed: {e}")
            return []
        except ValueError as e:
            self.status = SourceStatus.FAILED
            logger.error(f"Hugging Face API returned invalid JSON: {e}")
            return []

        if not isinstance(data, list) or len(data) == 0:
            self.status = SourceStatus.EMPTY
            logger.warning("Hugging Face API returned 0 daily papers.")
            return []

        # Sort papers by community engagement: upvotes * 2 + comments
        def engagement_score(item: dict) -> int:
            paper_dict = item.get("paper", {})
            upvotes = int(item.get("numUpvotes") or paper_dict.get("upvotes") or 0)
            comments = int(item.get("numComments") or 0)
            return (upvotes * 2) + comments

        sorted_items = sorted(data, key=engagement_score, reverse=True)

        papers: list[HuggingFacePaperItem] = []
        for item in sorted_items[:self.target_count]:
            paper = item.get("paper", {})
            paper_id = paper.get("id") or item.get("id") or ""
            raw_title = item.get("title") or paper.get("title") or "Başlıksız HF Makalesi"
            clean_title = raw_title.replace("|", "-").strip()

            url = f"https://huggingface.co/papers/{paper_id}" if paper_id else "https://huggingface.co/papers"
            raw_summary = item.get("summary") or paper.get("summary") or "Özet bulunamadı."
            smart_summary = extract_smart_summary(raw_summary)

            upvotes = max(0, int(item.get("numUpvotes") or paper.get("upvotes") or 0))
            comments = max(0, int(item.get("numComments") or 0))

            # Authors
            authors_list = paper.get("authors", [])
            author_names = [
                a.get("name") for a in authors_list if isinstance(a, dict) and a.get("name")
            ]
            authors_str = ", ".join(author_names[:2]) + (" vb." if len(author_names) > 2 else "")

            pub_date = str(item.get("publishedAt") or "").split("T")[0]

            try:
                hf_paper = HuggingFacePaperItem(
                    title=clean_title,
                    url=url,
                    authors=authors_str or "Araştırmacılar Belirtilmemiş",
                    upvotes=upvotes,
                    num_comments=comments,
                    summary=smart_summary,
                    published_date=pub_date or "Güncel"
                )
                papers.append(hf_paper)
            except ValueError as e:
                logger.warning(f"Validation error for Hugging Face paper '{clean_title}': {e}")

        if len(papers) == 0:
            self.status = SourceStatus.EMPTY
        elif len(papers) < self.target_count:
            self.status = SourceStatus.DEGRADED
        else:
            self.status = SourceStatus.SUCCESS

        logger.info(f"Successfully collected {len(papers)} Hugging Face daily papers.")
        return papers
