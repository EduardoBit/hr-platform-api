from django.db import models
from shared.constants import RolesUsuario


class RolModel(models.Model):
    empresa_id = models.IntegerField(null=True, blank=True)
    nombre = models.CharField(max_length=50, choices=RolesUsuario.CHOICES)
    permisos = models.JSONField(default=list)
    es_sistema = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "usuario"
        db_table = "roles"
        unique_together = [("empresa_id", "nombre")]

    def __str__(self):
        return self.nombre