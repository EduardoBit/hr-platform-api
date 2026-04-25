from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer


class CrearTipoPermisoSerializer(BaseSerializer):
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(allow_blank=True, default="")
    requiere_adjunto = serializers.BooleanField(default=False)


class TipoPermisoOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    empresa_id = serializers.IntegerField()
    nombre = serializers.CharField()
    descripcion = serializers.CharField()
    requiere_adjunto = serializers.BooleanField()
    es_activo = serializers.BooleanField()