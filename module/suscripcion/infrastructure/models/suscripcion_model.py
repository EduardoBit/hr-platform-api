from django.db import models
from shared.constants import EstadosSuscripcion
from modules.suscripcion.infrastructure.models.plan_model import PlanModel


class SuscripcionModel(models.Model):
    empresa_id = models.IntegerField(unique=True)
    plan = models.ForeignKey(PlanModel, on_delete=models.PROTECT, related_name="suscripciones")
    estado = models.CharField(
        max_length=20,
        choices=EstadosSuscripcion.CHOICES,
        default=EstadosSuscripcion.TRIAL,
    )
    fecha_inicio = models.DateTimeField()
    fecha_fin_trial = models.DateTimeField(null=True, blank=True)
    fecha_proxima_facturacion = models.DateTimeField(null=True, blank=True)
    usuarios_activos = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "suscripcion"
        db_table = "suscripciones"
        indexes = [models.Index(fields=["empresa_id", "estado"])]

    def __str__(self):
        return f"Empresa {self.empresa_id} - {self.plan.nombre} - {self.estado}"