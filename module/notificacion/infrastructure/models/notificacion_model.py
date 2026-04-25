from django.db import models


class NotificacionModel(models.Model):
    CANAL_CHOICES = [
        ("EMAIL", "Email"),
        ("IN_APP", "In-App"),
        ("PUSH", "Push"),
    ]

    empresa_id = models.IntegerField(null=True, blank=True)
    usuario_id = models.IntegerField()
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    canal = models.CharField(max_length=10, choices=CANAL_CHOICES)
    leida = models.BooleanField(default=False)
    enviada = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "notificacion"
        db_table = "notificaciones"
        indexes = [
            models.Index(fields=["usuario_id", "leida"]),
            models.Index(fields=["usuario_id", "fecha_creacion"]),
        ]

    def __str__(self):
        return f"{self.canal} - {self.titulo} - {'leída' if self.leida else 'no leída'}"