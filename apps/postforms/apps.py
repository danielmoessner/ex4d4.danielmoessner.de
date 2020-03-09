from django.apps import AppConfig


class PostformsConfig(AppConfig):
    name = 'apps.postforms'

    def ready(self):
        # Makes sure all signal handlers are connected
        from apps.postforms import handlers
