from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer


class CrearSedeSerializer(BaseSerializer):
    nombre = serializers.CharField(max_length=150)
    direccion = serializers.CharField()
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)
    radio_metros = serializers.IntegerField(min_value=10, max_value=10000)


class ActualizarSedeSerializer(BaseSerializer):
    nombre = serializers.CharField(max_length=150)
    direccion = serializers.CharField()
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)
    radio_metros = serializers.IntegerField(min_value=10, max_value=10000)


class SedeOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    empresa_id = serializers.IntegerField()
    nombre = serializers.CharField()
    direccion = serializers.CharField()
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    radio_metros = serializers.IntegerField()
    es_activa = serializers.BooleanField()