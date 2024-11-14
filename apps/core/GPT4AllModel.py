from gpt4all import GPT4All
import threading
from django.conf import settings
import os


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
        if not os.path.exists(settings.MODELS_ROOT):
            os.makedirs(settings.MODELS_ROOT)

        self.model = GPT4All(
            model_name=settings.MODEL_USAGE,
            model_path=settings.MODELS_ROOT,
        )

    def generate_response(self, prompt: str) -> str:
        with self.model.chat_session() as session:
            response = self.model.generate(prompt, max_tokens=460)
        return response
