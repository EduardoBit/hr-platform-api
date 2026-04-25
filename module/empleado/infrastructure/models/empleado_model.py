from django.db import models
from shared.constants import EstadosEmpleado, TiposDocumento


class EmpleadoModel(models.Model):
    empresa_id = models.IntegerField()
    usuario_id = models.IntegerField(null=True, blank=True)
    sede_id = models.IntegerField()
    codigo_unico = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=20, choices=TiposDocumento.CHOICES)
    numero_documento = models.CharField(max_length=20)
    correo = models.EmailField()
    cargo = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=20,
        choices=EstadosEmpleado.CHOICES,
        default=EstadosEmpleado.ACTIVO,
    )
    fecha_ingreso = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "empleado"
        db_table = "empleados"
        unique_together = [("empresa_id", "numero_documento"), ("empresa_id", "correo")]
        indexes = [
            models.Index(fields=["empresa_id", "estado"]),
            models.Index(fields=["empresa_id", "area"]),
            models.Index(fields=["sede_id"]),
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.codigo_unico})"