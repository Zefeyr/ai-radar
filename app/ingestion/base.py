from abc import ABC, abstractmethod

from app.schemas.article import ArticleIngest


class BaseCollector(ABC):
    """Abstract interface that all data collectors must implement."""

    @abstractmethod
    def fetch(self) -> list[ArticleIngest]:
        """Fetches raw items, standardizes them, and returns a list of ArticleIngest."""
        pass
