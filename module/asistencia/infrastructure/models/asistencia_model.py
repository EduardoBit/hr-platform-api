from django.db import models
from shared.constants import TiposMarcaje, MetodosMarcaje


class RegistroAsistenciaModel(models.Model):
    empresa_id = models.IntegerField()
    empleado_id = models.IntegerField()
    sede_id = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TiposMarcaje.CHOICES)
    metodo = models.CharField(max_length=10, choices=MetodosMarcaje.CHOICES)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    es_tardanza = models.BooleanField(default=False)
    es_manual = models.BooleanField(default=False)
    justificacion_manual = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "asistencia"
        db_table = "registros_asistencia"
        indexes = [
            models.Index(fields=["empleado_id", "timestamp"]),
            models.Index(fields=["empresa_id", "timestamp"]),
            models.Index(fields=["sede_id"]),
        ]

    def __str__(self):
        return f"Empleado {self.empleado_id} - {self.tipo} - {self.timestamp}"