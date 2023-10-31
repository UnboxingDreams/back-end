from django.apps import AppConfig


class PetmourningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'petmourning'

    def ready(self):
        from app import cron
        cron.start()