from django.apps import AppConfig


class NotificacionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.notificacion"
    label = "notificacion"

    def ready(self):
        pass 