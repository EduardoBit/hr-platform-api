from django.db import models
from modules.empresa.infrastructure.models.empresa_model import EmpresaModel


class SedeModel(models.Model):
    empresa = models.ForeignKey(EmpresaModel, on_delete=models.CASCADE, related_name="sedes")
    nombre = models.CharField(max_length=150)
    direccion = models.TextField()
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)
    radio_metros = models.PositiveIntegerField(default=100)
    es_activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "empresa"
        db_table = "sedes"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.empresa.razon_social})"