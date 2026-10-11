import json
import re

from app.ai.client import OllamaClient
from app.ai.prompts import SYSTEM_PROMPT, build_analysis_prompt
from app.schemas.digest import LLMSummaryOutput


class ArticleSummarizer:
    def __init__(self):
        self.ollama = OllamaClient()

    def analyze_article(self, title: str, source: str, content: str) -> LLMSummaryOutput | None:
        """
        Sends article text to Ollama and returns validated LLMSummaryOutput.
        Returns None if inference or JSON validation fails.
        """
        prompt = build_analysis_prompt(title=title, source=source, content=content)

        try:
            response = self.ollama.client.chat(
                model=self.ollama.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                options={"temperature": 0.2},  # Low temperature for factual, deterministic output
            )

            raw_text = response["message"]["content"].strip()
            return self._parse_and_validate(raw_text)

        except Exception as e:
            print(f"[ArticleSummarizer] Inference failed for '{title}': {e}")
            return None

    def _parse_and_validate(self, text: str) -> LLMSummaryOutput | None:
        """Cleans potential Markdown artifacts and validates JSON with Pydantic."""
        try:
            # Clean common markdown code fences if the model emitted them
            cleaned = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
            cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE).strip()

            # Attempt JSON decode
            data = json.loads(cleaned)

            # Validate against Pydantic schema
            return LLMSummaryOutput(**data)

        except Exception as e:
            print(f"[ArticleSummarizer] JSON validation failed: {e}\nRaw Output: {text[:200]}")
            return None
