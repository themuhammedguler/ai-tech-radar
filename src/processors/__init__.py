"""
Processors package for content filtering, scoring, text summarization, and AI executive synthesis.
"""

from .content_filter import ContentFilter
from .text_summarizer import extract_smart_summary
from .ai_summarizer import AiSummarizer

__all__ = ["ContentFilter", "extract_smart_summary", "AiSummarizer"]
