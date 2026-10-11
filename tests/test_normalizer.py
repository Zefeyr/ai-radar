from app.ingestion.normalizer import generate_url_hash, normalize_url


def test_url_normalization_strips_tracking():
    dirty_url = "https://techcrunch.com/2026/10/08/ai-news/?utm_source=twitter&utm_medium=feed"
    clean_url = "https://techcrunch.com/2026/10/08/ai-news"

    assert normalize_url(dirty_url) == clean_url


def test_hash_identical_for_equivalent_urls():
    url_a = "https://news.ycombinator.com/item?id=12345"
    url_b = "https://news.ycombinator.com/item?id=12345&utm_campaign=daily"

    hash_a = generate_url_hash(url_a)
    hash_b = generate_url_hash(url_b)

    assert hash_a == hash_b
    assert len(hash_a) == 64
