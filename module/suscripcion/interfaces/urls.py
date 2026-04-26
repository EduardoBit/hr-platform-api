from django.urls import path
from modules.suscripcion.interfaces.views.plan_view import PlanListView
from modules.suscripcion.interfaces.views.suscripcion_view import SuscripcionDetailView, CambiarPlanView

urlpatterns = [
    path("planes/", PlanListView.as_view()),
    path("mi-suscripcion/", SuscripcionDetailView.as_view()),
    path("mi-suscripcion/cambiar-plan/", CambiarPlanView.as_view()),
]