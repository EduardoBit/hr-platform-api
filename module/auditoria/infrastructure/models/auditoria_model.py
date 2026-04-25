from django.db import models
from shared.constants import TiposEvento


class AuditoriaLogModel(models.Model):
    empresa_id = models.IntegerField(null=True, blank=True)
    usuario_id = models.IntegerField(null=True, blank=True)
    rol_usuario = models.CharField(max_length=50, null=True, blank=True)
    tipo_evento = models.CharField(max_length=50, choices=TiposEvento.CHOICES)
    descripcion = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    detalles = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "auditoria"
        db_table = "auditoria_log"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["empresa_id", "timestamp"]),
            models.Index(fields=["usuario_id"]),
            models.Index(fields=["tipo_evento"]),
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            raise PermissionError("Los registros de auditoría son inmutables.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionError("Los registros de auditoría no pueden ser eliminados.")

    def __str__(self):
        return f"{self.tipo_evento} - {self.timestamp}"