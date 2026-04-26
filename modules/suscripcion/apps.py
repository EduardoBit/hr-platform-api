from django.apps import AppConfig


class SuscripcionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.suscripcion"
    label = "suscripcion"

    def ready(self):
        pass