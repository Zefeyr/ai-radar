from app.ai.summarizer import ArticleSummarizer


def test_single_summary():
    summarizer = ArticleSummarizer()

    if not summarizer.ollama.is_available():
        print("Ollama is not running. Please start Ollama desktop/daemon first.")
        return

    sample_title = "PostgreSQL 17 Released with Enhanced Query Performance and Memory Management"
    sample_source = "PostgreSQL News"
    sample_content = (
        "The PostgreSQL Global Development Group today announced the release of PostgreSQL 17. "
        "This release includes significant improvements to the query execution engine, vacuum memory consumption "
        "improvements up to 2x, enhanced JSON query features using JSON_TABLE, and improved logical replication."
    )

    print("Sending article to Ollama for analysis...")
    result = summarizer.analyze_article(
        title=sample_title, source=sample_source, content=sample_content
    )

    if result:
        print("\n--- Ollama Enrichment Result ---")
        print(f"Category:     {result.category}")
        print(f"Impact Score: {result.impact_score}/10.0")
        print(f"Summary:      {result.summary}")
        print("Takeaways:")
        for t in result.key_takeaways:
            print(f"  - {t}")
    else:
        print("Analysis failed.")


if __name__ == "__main__":
    test_single_summary()
