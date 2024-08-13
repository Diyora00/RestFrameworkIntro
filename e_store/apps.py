from django.apps import AppConfig


class EStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'e_store'

    def ready(self):
        import e_store.signals
