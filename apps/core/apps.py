from django.apps import AppConfig

from apps.core.GPT4AllModel import GPT4AllModelSingleton


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    def ready(self):
        GPT4AllModelSingleton()