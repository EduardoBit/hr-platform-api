from django.urls import path
from modules.notificacion.interfaces.views.notificacion_view import (
    NotificacionListView,
    NotificacionMarcarLeidaView,
    PreferenciasView,
)

urlpatterns = [
    path("", NotificacionListView.as_view()),
    path("<int:notificacion_id>/leer/", NotificacionMarcarLeidaView.as_view()),
    path("preferencias/", PreferenciasView.as_view()),
]