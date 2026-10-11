from abc import ABC, abstractmethod
from typing import List
from app.schemas.article import ArticleIngest


class BaseCollector(ABC):
    """Abstract interface that all data collectors must implement."""

    @abstractmethod
    def fetch(self) -> List[ArticleIngest]:
        """Fetches raw items, standardizes them, and returns a list of ArticleIngest."""
        pass
