"""
Configuration module for AI & Tech Daily Radar (v4.0).
Centralizes paths, API endpoints, timeouts, heuristics, categories, and LLM configuration.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
README_PATH = BASE_DIR / "README.md"

# Network & HTTP Settings
CONNECT_TIMEOUT = 5.0    # Seconds to establish connection
READ_TIMEOUT = 25.0      # Seconds to wait for server response
DEFAULT_TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.5
USER_AGENT = "AITechRadar/4.0 (+https://github.com/themuhammedguler/ai-tech-radar)"

# HackerNews Settings
HN_API_URL = "https://hn.algolia.com/api/v1/search"
HN_POOL_SIZE = 50        # Number of candidates fetched from front page
HN_TARGET_COUNT = 10     # Number of curated items in the final report
HN_MIN_POINTS = 10       # Minimum points required for non-boosted entries

# GitHub Trending Settings
GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
GITHUB_TARGET_COUNT = 5
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"

# Hugging Face Settings
HUGGINGFACE_DAILY_PAPERS_URL = "https://huggingface.co/api/daily_papers"
HUGGINGFACE_TARGET_COUNT = 5

# ArXiv Settings (HTTPS enforced!)
ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_CATEGORIES = ["cat:cs.AI", "cat:cs.LG", "cat:cs.CL"]
ARXIV_FETCH_COUNT = 10   # Fetch more to allow deduplication / verification
ARXIV_TARGET_COUNT = 5   # Target papers in the final report

# Gemini AI Synthesis Settings
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
GEMINI_FALLBACK_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

# Text Summarizer Settings
SUMMARY_MAX_CHARS = 380
SUMMARY_MIN_CHARS = 80
ARCHIVE_DISPLAY_DAYS = 7

# HackerNews Negative Filter Patterns (Exclude spam, obituaries, pure medical, politics)
NEGATIVE_PATTERNS = [
    r"\bhas died\b", r"\bdies at\b", r"\bpassed away\b", r"\bobituary\b", r"\bdeath of\b",
    r"\bcancer\b", r"\bdentist\b", r"\bdentistry\b", r"\badhd\b", r"\bautism\b",
    r"\bdiet\b", r"\bweight loss\b", r"\bheart attack\b", r"\bdementia\b", r"\balzheimer\b",
    r"\btoddler\b", r"\bparenting\b", r"\bdivorce\b", r"\bdating\b", r"\bmarriage\b",
    r"\belection\b", r"\bsenate\b", r"\bpresident\b", r"\bcongress\b", r"\bdemocrat\b", r"\brepublican\b",
    r"\bis hiring\b", r"\bwho is hiring\b", r"\bwho wants to be hired\b", r"\bhiring:\b"
]

# Exceptions: If any of these exist, do NOT eliminate even if a negative word matches
STRONG_TECH_EXCEPTIONS = [
    "ai", "llm", "cnn", "model", "models", "deep learning", "machine learning",
    "algorithm", "neural", "dataset", "biotech", "software", "robot", "robotics",
    "compute", "gpu", "inference"
]

# Verified Tech Domains that grant domain credibility bonus
TECH_DOMAINS = [
    "github.com", "arxiv.org", "huggingface.co", "eff.org", "cve.org",
    "blog.cloudflare.com", "go.dev", "rust-lang.org", "python.org", "kernel.org"
]

# Categorization and positive scoring dictionary
TECH_CATEGORIES = {
    "🤖 AI / ML": [
        "ai", "llm", "llms", "cnn", "cnns", "agent", "agents", "gpt", "model", "models", "neural", "deep learning", "machine learning",
        "weights", "transformer", "diffusion", "inference", "gpu", "cuda", "nvidia",
        "anthropic", "openai", "gemini", "mistral", "claude", "deepseek", "qwen", "llama",
        "opus", "fine-tuning", "rag", "embedding", "multimodal", "reasoning", "vision",
        "perplexity", "copilot"
    ],
    "🛡️ Güvenlik": [
        "security", "vulnerability", "cve", "exploit", "hack", "hacked", "cyber", "malware",
        "ransomware", "breach", "zero-day", "backdoor", "encryption", "auth", "phishing",
        "infected", "vm escape", "credential", "pwn"
    ],
    "💻 Yazılım & Geliştirme": [
        "software", "programming", "code", "coding", "developer", "open source", "open-source",
        "github", "rust", "python", "javascript", "typescript", "golang", "go 1.", "c++",
        "wasm", "webassembly", "database", "postgres", "sqlite", "redis", "compiler",
        "git", "api", "framework", "library", "testing", "frontend", "backend", "bare-metal",
        "uefi", "runtime", "gui", "ui framework"
    ],
    "⚙️ Sistem & Altyapı": [
        "linux", "kernel", "unix", "cpu", "chip", "semiconductor", "hardware", "server",
        "servers", "cloud", "docker", "kubernetes", "networking", "protocol", "http", "ssh",
        "microvm", "firecracker", "floppy", "storage", "quantum", "robotics", "robot",
        "architecture", "benchmark", "performance", "vm", "vms"
    ]
}
