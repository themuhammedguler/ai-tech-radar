"""
Pipeline Orchestrator for AI & Tech Daily Radar (v4.0).
Coordinates multi-source data acquisition (HackerNews, GitHub Trending, Hugging Face, ArXiv),
synthesizes AI Executive Briefings with Gemini Flash, and updates reports and README.
"""

from datetime import datetime
import sys
from pathlib import Path

from src.collectors.arxiv import ArxivCollector
from src.collectors.github_trending import GithubTrendingCollector
from src.collectors.hackernews import HackerNewsCollector
from src.collectors.huggingface import HuggingFaceCollector
from src.generators.readme_updater import ReadmeUpdater
from src.generators.report_generator import ReportGenerator
from src.logging_config import logger
from src.models import PipelineReportResult, SourceStatus
from src.processors.ai_summarizer import AiSummarizer


class PipelineExecutionError(Exception):
    """Raised when the pipeline fails critical validation or execution steps."""
    pass


class RadarPipeline:
    """Master orchestrator for the 25-trend AI & Tech Daily Radar pipeline."""

    def __init__(
        self,
        hn_collector: HackerNewsCollector | None = None,
        github_collector: GithubTrendingCollector | None = None,
        hf_collector: HuggingFaceCollector | None = None,
        arxiv_collector: ArxivCollector | None = None,
        ai_summarizer: AiSummarizer | None = None,
        report_generator: ReportGenerator | None = None,
        readme_updater: ReadmeUpdater | None = None
    ):
        self.hn_collector = hn_collector or HackerNewsCollector()
        self.github_collector = github_collector or GithubTrendingCollector()
        self.hf_collector = hf_collector or HuggingFaceCollector()
        self.arxiv_collector = arxiv_collector or ArxivCollector()
        self.ai_summarizer = ai_summarizer or AiSummarizer()
        self.report_generator = report_generator or ReportGenerator()
        self.readme_updater = readme_updater or ReadmeUpdater()

    def run(self, date_str: str | None = None, exit_on_critical_failure: bool = False) -> PipelineReportResult:
        """
        Executes end-to-end 25-trend radar data pipeline with AI executive synthesis.

        Args:
            date_str: Target date (defaults to today YYYY-MM-DD).
            exit_on_critical_failure: If True, calls sys.exit(1) on total pipeline failure.

        Returns:
            PipelineReportResult containing collected data, execution status, and paths.
        """
        today = date_str or datetime.now().strftime("%Y-%m-%d")
        logger.info(f"========== Starting AI & Tech Daily Radar Pipeline: {today} ==========")

        result = PipelineReportResult(date_str=today)

        # 1. Collect HackerNews
        try:
            result.hn_items = self.hn_collector.collect()
            result.hn_status = self.hn_collector.status
        except Exception as e:
            logger.error(f"HackerNews collection error: {e}")
            result.hn_status = SourceStatus.FAILED
            result.errors.append(f"HackerNews Error: {e}")

        # 2. Collect GitHub Trending
        try:
            result.github_items = self.github_collector.collect()
            result.github_status = self.github_collector.status
        except Exception as e:
            logger.error(f"GitHub collection error: {e}")
            result.github_status = SourceStatus.FAILED
            result.errors.append(f"GitHub Error: {e}")

        # 3. Collect Hugging Face Daily Papers
        try:
            result.huggingface_items = self.hf_collector.collect()
            result.huggingface_status = self.hf_collector.status
        except Exception as e:
            logger.error(f"Hugging Face collection error: {e}")
            result.huggingface_status = SourceStatus.FAILED
            result.errors.append(f"Hugging Face Error: {e}")

        # 4. Collect ArXiv
        try:
            result.arxiv_items = self.arxiv_collector.collect()
            result.arxiv_status = self.arxiv_collector.status
        except Exception as e:
            logger.error(f"ArXiv collection error: {e}")
            result.arxiv_status = SourceStatus.FAILED
            result.errors.append(f"ArXiv Error: {e}")

        # 5. Critical Data Validation: Prevent committing empty/corrupt data
        if result.total_items_count == 0:
            err_msg = (
                "CRITICAL PIPELINE FAILURE: All 4 data sources yielded 0 valid items. "
                "Aborting report generation to prevent committing empty data."
            )
            logger.critical(err_msg)
            result.errors.append(err_msg)
            if exit_on_critical_failure:
                sys.exit(1)
            raise PipelineExecutionError(err_msg)

        # 6. Generate Gemini AI Executive Briefing (3 thematic bullets)
        try:
            briefing = self.ai_summarizer.synthesize(
                hn_items=result.hn_items,
                github_items=result.github_items,
                hf_items=result.huggingface_items,
                arxiv_items=result.arxiv_items
            )
            result.executive_briefing = briefing
            result.ai_summary_status = SourceStatus.SUCCESS if briefing.generated_by_ai else SourceStatus.DEGRADED
        except Exception as e:
            logger.warning(f"AI summarization issue: {e}")
            result.executive_briefing = self.ai_summarizer._create_fallback_briefing("AI servisi geçici olarak yanıt vermedi")
            result.ai_summary_status = SourceStatus.FAILED
            result.errors.append(f"AI Summarizer Error: {e}")

        # 7. Generate Daily Report
        try:
            report_file = self.report_generator.write_report(
                date_str=today,
                hn_items=result.hn_items,
                github_items=result.github_items,
                hf_items=result.huggingface_items,
                arxiv_items=result.arxiv_items,
                briefing=result.executive_briefing,
                hn_status=result.hn_status,
                github_status=result.github_status,
                hf_status=result.huggingface_status,
                arxiv_status=result.arxiv_status
            )
            result.report_file = report_file
        except Exception as e:
            err_msg = f"Failed to write daily markdown report: {e}"
            logger.error(err_msg)
            result.errors.append(err_msg)
            if exit_on_critical_failure:
                sys.exit(1)
            raise PipelineExecutionError(err_msg) from e

        # 8. Update README.md
        try:
            readme_ok = self.readme_updater.update(
                date_str=today,
                hn_items=result.hn_items,
                github_items=result.github_items,
                hf_items=result.huggingface_items,
                arxiv_items=result.arxiv_items,
                briefing=result.executive_briefing,
                hn_status=result.hn_status,
                github_status=result.github_status,
                hf_status=result.huggingface_status,
                arxiv_status=result.arxiv_status
            )
            result.readme_updated = readme_ok
        except Exception as e:
            err_msg = f"Failed to update README.md: {e}"
            logger.error(err_msg)
            result.errors.append(err_msg)
            if exit_on_critical_failure:
                sys.exit(1)
            raise PipelineExecutionError(err_msg) from e

        logger.info(
            f"========== Pipeline Finished [{ 'SUCCESS' if result.is_healthy else 'DEGRADED' }] "
            f"(Total Trends: {result.total_items_count}) =========="
        )
        return result
