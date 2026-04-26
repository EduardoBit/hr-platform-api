from django.urls import path
from modules.auditoria.interfaces.views.auditoria_view import AuditoriaListView, AuditoriaExportarView

urlpatterns = [
    path("", AuditoriaListView.as_view()),
    path("exportar/", AuditoriaExportarView.as_view()),
]