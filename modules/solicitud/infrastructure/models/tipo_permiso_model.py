from django.db import models


class TipoPermisoModel(models.Model):
    empresa_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    requiere_adjunto = models.BooleanField(default=False)
    es_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "solicitud"
        db_table = "tipos_permiso"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
