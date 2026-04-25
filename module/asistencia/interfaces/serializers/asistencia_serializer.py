from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer
from shared.constants import TiposMarcaje


class RegistrarMarcajeSerializer(BaseSerializer):
    token_qr = serializers.CharField()
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)


class RegistrarManualSerializer(BaseSerializer):
    empleado_id = serializers.IntegerField()
    tipo = serializers.ChoiceField(choices=TiposMarcaje.CHOICES)
    fecha = serializers.DateField()
    hora = serializers.TimeField(format="%H:%M")
    justificacion = serializers.CharField(min_length=10)


class RegistroAsistenciaOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    empleado_id = serializers.IntegerField()
    empleado_nombre = serializers.CharField()
    sede_id = serializers.IntegerField()
    sede_nombre = serializers.CharField(allow_null=True)
    tipo = serializers.CharField()
    metodo = serializers.CharField()
    es_tardanza = serializers.BooleanField()
    es_manual = serializers.BooleanField()
    timestamp = serializers.DateTimeField()


class ReporteAsistenciaOutputSerializer(BaseSerializer):
    empleado_id = serializers.IntegerField()
    empleado_nombre = serializers.CharField()
    total_dias = serializers.IntegerField()
    dias_presentes = serializers.IntegerField()
    dias_ausentes = serializers.IntegerField()
    tardanzas = serializers.IntegerField()
    registros = RegistroAsistenciaOutputSerializer(many=True)