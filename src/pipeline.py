"""
Pipeline Orchestrator for AI & Tech Daily Radar.
Coordinates collection, validation, error handling, report generation, and README updates.
"""

from datetime import datetime
import sys
from pathlib import Path

from src.collectors.arxiv import ArxivCollector
from src.collectors.hackernews import HackerNewsCollector
from src.generators.readme_updater import ReadmeUpdater
from src.generators.report_generator import ReportGenerator
from src.logging_config import logger
from src.models import ArxivPaper, PipelineReportResult, SourceStatus, TrendItem


class PipelineExecutionError(Exception):
    """Raised when the pipeline fails critical validation or execution steps."""
    pass


class RadarPipeline:
    """Master orchestrator for the AI & Tech Daily Radar data pipeline."""

    def __init__(
        self,
        hn_collector: HackerNewsCollector | None = None,
        arxiv_collector: ArxivCollector | None = None,
        report_generator: ReportGenerator | None = None,
        readme_updater: ReadmeUpdater | None = None
    ):
        self.hn_collector = hn_collector or HackerNewsCollector()
        self.arxiv_collector = arxiv_collector or ArxivCollector()
        self.report_generator = report_generator or ReportGenerator()
        self.readme_updater = readme_updater or ReadmeUpdater()

    def run(self, date_str: str | None = None, exit_on_critical_failure: bool = False) -> PipelineReportResult:
        """
        Executes end-to-end radar data pipeline.

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
            hn_items = self.hn_collector.collect()
            result.hn_items = hn_items
            result.hn_status = self.hn_collector.status
        except Exception as e:
            logger.critical(f"Unhandled error in HackerNewsCollector: {e}")
            result.hn_status = SourceStatus.FAILED
            result.errors.append(f"HackerNews Error: {e}")

        # 2. Collect ArXiv
        try:
            arxiv_items = self.arxiv_collector.collect()
            result.arxiv_items = arxiv_items
            result.arxiv_status = self.arxiv_collector.status
        except Exception as e:
            logger.critical(f"Unhandled error in ArxivCollector: {e}")
            result.arxiv_status = SourceStatus.FAILED
            result.errors.append(f"ArXiv Error: {e}")

        # 3. Critical Data Validation (Fixes: "API başarısızlığı başarı gibi sonuçlanabiliyor")
        if not result.hn_items and not result.arxiv_items:
            err_msg = (
                "CRITICAL PIPELINE FAILURE: Both HackerNews and ArXiv collection yielded 0 valid items. "
                "Aborting report generation to prevent committing empty/corrupted data."
            )
            logger.critical(err_msg)
            result.errors.append(err_msg)
            if exit_on_critical_failure:
                sys.exit(1)
            raise PipelineExecutionError(err_msg)

        # 4. Generate Daily Report
        try:
            report_file = self.report_generator.write_report(
                date_str=today,
                hn_items=result.hn_items,
                arxiv_items=result.arxiv_items,
                hn_status=result.hn_status,
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

        # 5. Update README.md
        try:
            readme_ok = self.readme_updater.update(
                date_str=today,
                hn_items=result.hn_items,
                arxiv_items=result.arxiv_items,
                hn_status=result.hn_status,
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
            f"========== Pipeline Finished [{ 'SUCCESS' if result.is_healthy else 'DEGRADED' }] =========="
        )
        return result
