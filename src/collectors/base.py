"""
Base collector class providing resilient HTTP session management,
connection pooling, exponential backoff retries, and unified timeouts.
"""

from abc import ABC, abstractmethod
from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config import DEFAULT_TIMEOUT, MAX_RETRIES, BACKOFF_FACTOR, USER_AGENT
from src.logging_config import logger
from src.models import SourceStatus


class BaseCollector(ABC):
    """Abstract base class for all remote data collectors."""

    def __init__(
        self,
        timeout: tuple[float, float] = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        backoff_factor: float = BACKOFF_FACTOR,
        user_agent: str = USER_AGENT
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.user_agent = user_agent
        self.session = self._create_resilient_session()
        self.status = SourceStatus.EMPTY

    def _create_resilient_session(self) -> requests.Session:
        """Configures a requests Session with urllib3 retry policies and connection pooling."""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"User-Agent": self.user_agent})
        return session

    def get(self, url: str, params: dict[str, Any] | None = None) -> requests.Response:
        """Executes a GET request with unified error logging and timeout."""
        logger.debug(f"HTTP GET: {url} | Params: {params}")
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response

    @abstractmethod
    def collect(self) -> list[Any]:
        """Collects, validates, and returns data items."""
        pass
