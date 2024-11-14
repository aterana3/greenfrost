from django.core.management.base import BaseCommand
from gpt4all import GPT4All
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Download model for GPT4All'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Chatbot model to download',
            default='Phi-3-mini-4k-instruct.Q4_0.gguf'
        )

    def handle(self, *args, **kwargs):
        model_name = kwargs['model']
        if not os.path.exists(settings.MODELS_ROOT):
            os.makedirs(settings.MODELS_ROOT)

        GPT4All.download_model(
            model_filename=model_name,
            model_path=settings.MODELS_ROOT,
        )