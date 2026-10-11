from app.ingestion.rss_collector import RSSCollector


def test_live_rss():
    # Hacker News Official "Front Page" RSS feed
    hn_feed = "https://news.ycombinator.com/rss"
    collector = RSSCollector(source_name="Hacker News", feed_url=hn_feed)

    print("Fetching articles from Hacker News...")
    articles = collector.fetch()

    print(f"Successfully collected {len(articles)} items!\n")
    if articles:
        first = articles[0]
        print("Sample Article:")
        print(f"- Title: {first.title}")
        print(f"- URL:   {first.url}")
        print(f"- Source: {first.source}")
        print(f"- Date:  {first.published_at}")


if __name__ == "__main__":
    test_live_rss()
