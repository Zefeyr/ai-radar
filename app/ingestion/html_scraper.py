import httpx
from bs4 import BeautifulSoup


class HTMLScraper:
    def __init__(self, timeout: float = 10.0):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            )
        }
        self.timeout = timeout

    def extract_article_text(self, url: str) -> str | None:
        """
        Fetches the HTML from a URL and extracts clean paragraphs,
        stripping scripts, styles, and navigational elements.
        """
        try:
            with httpx.Client(
                headers=self.headers, timeout=self.timeout, follow_redirects=True
            ) as client:
                response = client.get(url)
                if response.status_code != 200:
                    return None

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted tags that contaminate LLM context
            for unwanted_tag in soup(
                ["script", "style", "nav", "footer", "header", "noscript", "aside"]
            ):
                unwanted_tag.extract()

            # Target standard semantic article containers if present, else fallback to body
            article_container = (
                soup.find("article")
                or soup.find("main")
                or soup.find("div", class_="post-content")
                or soup.body
            )

            if not article_container:
                return None

            # Extract text from paragraphs
            paragraphs = [p.get_text(strip=True) for p in article_container.find_all("p")]
            cleaned_text = "\n\n".join([p for p in paragraphs if len(p) > 20])

            # Limit length to avoid blowing through LLM token limits (first ~4000 characters)
            return cleaned_text[:4000] if cleaned_text else None

        except Exception as e:
            # Scraping errors should fail gracefully without crashing the whole pipeline
            print(f"[HTMLScraper] Failed to scrape {url}: {e}")
            return None
