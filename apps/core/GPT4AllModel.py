from gpt4all import GPT4All
import threading
from django.conf import settings

class GPT4AllModelSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self):
        self.model = GPT4All(
            model_name="Phi-3-mini-4k-instruct.Q4_0.gguf",
            model_path=settings.MODELS_ROOT,
        )

    def generate_response(self, prompt: str) -> str:
        with self.model.chat_session() as session:
            response = self.model.generate(prompt, max_tokens=460)
        return response