# chatx/apps.py

from django.apps import AppConfig

class ChatxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatx'

    # ADD THIS METHOD to import your signals
    def ready(self):
        import chatx.signals