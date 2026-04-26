from django.urls import path
from modules.asistencia.interfaces.views.asistencia_view import (
    MarcajeView,
    AsistenciaManualView,
    ReporteAsistenciaView,
)
from modules.asistencia.interfaces.views.qr_view import GenerarQrView

urlpatterns = [
    path("marcaje/", MarcajeView.as_view()),
    path("manual/", AsistenciaManualView.as_view()),
    path("reporte/", ReporteAsistenciaView.as_view()),
    path("qr/<int:sede_id>/", GenerarQrView.as_view()),
]