from django.urls import path
from modules.empleado.interfaces.views.empleado_view import (
    EmpleadoListView,
    EmpleadoDetailView,
    EmpleadoDesactivarView,
    EmpleadoReactivarView,
    EmpleadoSedeView,
)

urlpatterns = [
    path("", EmpleadoListView.as_view()),
    path("<int:empleado_id>/", EmpleadoDetailView.as_view()),
    path("<int:empleado_id>/desactivar/", EmpleadoDesactivarView.as_view()),
    path("<int:empleado_id>/reactivar/", EmpleadoReactivarView.as_view()),
    path("<int:empleado_id>/sede/", EmpleadoSedeView.as_view()),
]