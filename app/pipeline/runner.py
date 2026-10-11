from datetime import datetime

from app.ai.summarizer import ArticleSummarizer
from app.core.database import SessionLocal
from app.db.repositories.article_repo import ArticleRepository
from app.db.repositories.digest_repo import DigestRepository
from app.ingestion.rss_collector import RSSCollector

# List of initial target feeds
FEEDS = [
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss"},
    {"name": "OpenAI Blog", "url": "https://openai.com/news/rss.xml"},
    {"name": "GitHub Trending AI", "url": "https://github-rss.alexi.sh/trending?topic=ai"},
]


class PipelineRunner:
    def __init__(self):
        self.summarizer = ArticleSummarizer()

    def run_ingestion(self) -> int:
        """Step 1: Collect from feeds and deduplicate via PostgreSQL."""
        print("[Pipeline] Starting ingestion...")
        total_new = 0

        with SessionLocal() as db:
            repo = ArticleRepository(db)
            for feed in FEEDS:
                try:
                    collector = RSSCollector(
                        source_name=feed["name"],
                        feed_url=feed["url"],
                        scrape_full_text=False,  # Keep fast; uses RSS snippets
                    )
                    items = collector.fetch()
                    print(f"[{feed['name']}] Found {len(items)} items.")

                    for item in items:
                        created = repo.create_if_not_exists(item)
                        if created:
                            total_new += 1
                except Exception as e:
                    print(f"[{feed['name']}] Ingestion error: {e}")

        print(f"[Pipeline] Ingestion completed. Inserted {total_new} new unique articles.")
        return total_new

    def run_ai_enrichment(self, batch_size: int = 5):
        """Step 2: Process pending articles with Ollama."""
        print("[Pipeline] Starting AI enrichment...")
        if not self.summarizer.ollama.is_available():
            print("[Pipeline] Ollama is not accessible. Skipping AI step.")
            return

        with SessionLocal() as db:
            repo = ArticleRepository(db)
            pending = repo.get_pending_articles(limit=batch_size)
            print(f"[Pipeline] Processing {len(pending)} pending articles.")

            for article in pending:
                print(f"-> Analyzing: {article.title[:50]}...")
                content = article.raw_content or article.title
                result = self.summarizer.analyze_article(
                    title=article.title,
                    source=article.source,
                    content=content,
                )

                if result:
                    repo.update_with_ai_results(
                        article_id=article.id,
                        summary=result.summary,
                        key_takeaways=result.key_takeaways,
                        category=result.category,
                        impact_score=result.impact_score,
                    )
                    print(f"   [DONE] Score: {result.impact_score} | Category: {result.category}")
                else:
                    repo.mark_as_failed(article.id, "Failed LLM validation or timeout")
                    print("   [FAILED] Marked as FAILED.")

    def run_digest_generation(self) -> None:
        """Step 3: Compile today's top stories into a digest."""
        print("[Pipeline] Generating Daily Digest...")
        with SessionLocal() as db:
            digest_repo = DigestRepository(db)
            top_articles = digest_repo.get_top_articles_for_digest(min_score=6.0, limit=5)

            if not top_articles:
                print("[Pipeline] No high-impact articles found for today's digest.")
                return

            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            digest = digest_repo.create_digest(
                title=f"AI Radar Daily - {date_str}",
                articles=top_articles,
                intro=f"Curated top technical updates for {date_str}.",
            )
            print(
                f"[Pipeline] Digest created successfully: '{digest.title}' with {len(digest.articles)} articles."
            )


def main():
    runner = PipelineRunner()
    runner.run_ingestion()
    runner.run_ai_enrichment(batch_size=5)
    runner.run_digest_generation()


if __name__ == "__main__":
    main()
