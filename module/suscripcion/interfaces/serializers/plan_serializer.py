from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer
from shared.constants import PlanesNombre


class CrearPlanSerializer(BaseSerializer):
    nombre = serializers.ChoiceField(choices=PlanesNombre.CHOICES)
    precio_mensual = serializers.FloatField(min_value=0)
    limite_usuarios = serializers.IntegerField(min_value=1)
    almacenamiento_gb = serializers.IntegerField(min_value=1)


class PlanOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    precio_mensual = serializers.FloatField()
    limite_usuarios = serializers.IntegerField()
    almacenamiento_gb = serializers.IntegerField()
    es_activo = serializers.BooleanField()