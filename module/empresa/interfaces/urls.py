from django.urls import path
from modules.empresa.interfaces.views.empresa_view import (
    ValidarRucView, RegistrarEmpresaView, EmpresaDetailView, SuspenderEmpresaView
)
from modules.empresa.interfaces.views.sede_view import SedeListView, SedeDetailView

urlpatterns = [
    path("validar-ruc/<str:ruc>/", ValidarRucView.as_view()),
    path("registro/", RegistrarEmpresaView.as_view()),
    path("<int:empresa_id>/", EmpresaDetailView.as_view()),
    path("<int:empresa_id>/suspender/", SuspenderEmpresaView.as_view()),
    path("<int:empresa_id>/sedes/", SedeListView.as_view()),
    path("<int:empresa_id>/sedes/<int:sede_id>/", SedeDetailView.as_view()),
]