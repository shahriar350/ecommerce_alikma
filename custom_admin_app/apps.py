from django.apps import AppConfig


class CustomAdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_admin_app'

    def ready(self):
        from . import signals
