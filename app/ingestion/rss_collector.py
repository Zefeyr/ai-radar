import feedparser
from datetime import datetime
from time import mktime
from typing import List, Optional
from app.ingestion.base import BaseCollector
from app.ingestion.html_scraper import HTMLScraper
from app.schemas.article import ArticleIngest


class RSSCollector(BaseCollector):
    def __init__(self, source_name: str, feed_url: str, scrape_full_text: bool = False):
        self.source_name = source_name
        self.feed_url = feed_url
        self.scrape_full_text = scrape_full_text
        self.scraper = HTMLScraper() if scrape_full_text else None

    def fetch(self) -> List[ArticleIngest]:
        """Parses the RSS feed and converts valid entries into ArticleIngest items."""
        feed = feedparser.parse(self.feed_url)
        items: List[ArticleIngest] = []

        for entry in feed.entries:
            url = getattr(entry, "link", None)
            title = getattr(entry, "title", None)

            if not url or not title:
                continue

            # Parse publication timestamp safely
            published_at = self._parse_published_date(entry)

            # Get content from RSS snippet first
            raw_content = getattr(entry, "summary", None) or getattr(entry, "description", None)

            # If snippet is too short or missing, and scrape_full_text is enabled, fetch webpage body
            if self.scrape_full_text and (not raw_content or len(raw_content) < 150):
                extracted = self.scraper.extract_article_text(url)
                if extracted:
                    raw_content = extracted

            items.append(
                ArticleIngest(
                    url=url,
                    title=title,
                    source=self.source_name,
                    published_at=published_at,
                    raw_content=raw_content,
                )
            )

        return items

    def _parse_published_date(self, entry) -> Optional[datetime]:
        """Extracts standard published_parsed struct from feedparser and converts to datetime."""
        time_struct = getattr(entry, "published_parsed", None) or getattr(
            entry, "updated_parsed", None
        )
        if time_struct:
            try:
                return datetime.fromtimestamp(mktime(time_struct))
            except Exception:
                return None
        return None
