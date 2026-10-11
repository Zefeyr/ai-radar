import ollama
from app.config import settings


class OllamaClient:
    def __init__(self):
        # Initializes official Ollama client pointing to configured base URL
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        self.model = settings.OLLAMA_MODEL

    def is_available(self) -> bool:
        """Verifies if the Ollama service is reachable and responsive."""
        try:
            self.client.list()
            return True
        except Exception as e:
            print(f"[OllamaClient] Ollama connection check failed: {e}")
            return False

    def check_model_exists(self) -> bool:
        """Checks if the configured model is installed locally in Ollama."""
        try:
            models_response = self.client.list()
            # Handle both object and dict structures across ollama package versions
            installed = [
                m.model if hasattr(m, "model") else m.get("name", "")
                for m in models_response.get("models", [])
            ]
            return any(self.model in name for name in installed)
        except Exception:
            return False
