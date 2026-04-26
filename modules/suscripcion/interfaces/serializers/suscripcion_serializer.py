from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer


class CambiarPlanSerializer(BaseSerializer):
    nuevo_plan_id = serializers.IntegerField()


class SuscripcionOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    empresa_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    plan_nombre = serializers.CharField()
    estado = serializers.CharField()
    fecha_inicio = serializers.DateTimeField()
    fecha_fin_trial = serializers.DateTimeField(allow_null=True)
    fecha_proxima_facturacion = serializers.DateTimeField(allow_null=True)
    usuarios_activos = serializers.IntegerField()
    limite_usuarios = serializers.IntegerField()
    dias_restantes_trial = serializers.IntegerField(allow_null=True)