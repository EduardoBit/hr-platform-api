from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer


class ConfigurarPreferenciasSerializer(BaseSerializer):
    email_habilitado = serializers.BooleanField(default=True)
    push_habilitado = serializers.BooleanField(default=True)


class NotificacionOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    usuario_id = serializers.IntegerField()
    titulo = serializers.CharField()
    mensaje = serializers.CharField()
    canal = serializers.CharField()
    leida = serializers.BooleanField()
    enviada = serializers.BooleanField()
    fecha_envio = serializers.DateTimeField(allow_null=True)
    fecha_creacion = serializers.DateTimeField()