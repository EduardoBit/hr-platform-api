from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer


class ConsultarAuditoriaSerializer(BaseSerializer):
    empresa_id = serializers.IntegerField(required=False, allow_null=True)
    usuario_id = serializers.IntegerField(required=False, allow_null=True)
    rol = serializers.CharField(required=False, allow_null=True)
    tipo_evento = serializers.CharField(required=False, allow_null=True)
    fecha_desde = serializers.DateTimeField(required=False, allow_null=True)
    fecha_hasta = serializers.DateTimeField(required=False, allow_null=True)


class ExportarAuditoriaSerializer(BaseSerializer):
    fecha_desde = serializers.DateTimeField()
    fecha_hasta = serializers.DateTimeField()
    formato = serializers.ChoiceField(choices=["PDF", "CSV"])


class RegistroAuditoriaOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    empresa_id = serializers.IntegerField(allow_null=True)
    usuario_id = serializers.IntegerField(allow_null=True)
    rol_usuario = serializers.CharField(allow_null=True)
    tipo_evento = serializers.CharField()
    descripcion = serializers.CharField()
    ip_address = serializers.CharField(allow_null=True)
    detalles = serializers.DictField()
    timestamp = serializers.DateTimeField()