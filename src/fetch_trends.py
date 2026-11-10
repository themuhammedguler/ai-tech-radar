#!/usr/bin/env python3
"""
AI & Tech Daily Radar - CLI Entrypoint
Autonomous data pipeline runner invoked by GitHub Actions and local developers.
"""

import sys
from pathlib import Path

# Add project root to sys.path so it works seamlessly from any CWD
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logging_config import logger
from src.pipeline import RadarPipeline, PipelineExecutionError


def main() -> None:
    """CLI execution entrypoint."""
    try:
        pipeline = RadarPipeline()
        result = pipeline.run(exit_on_critical_failure=True)
        if not result.is_healthy:
            logger.warning(
                f"Pipeline completed with warnings/degraded sources: {result.errors}"
            )
        sys.exit(0)
    except PipelineExecutionError as e:
        logger.critical(f"Pipeline terminated due to critical error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
