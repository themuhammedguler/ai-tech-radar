"""
Processors package for content filtering, scoring, and text summarization.
"""

from .content_filter import ContentFilter
from .text_summarizer import extract_smart_summary

__all__ = ["ContentFilter", "extract_smart_summary"]
