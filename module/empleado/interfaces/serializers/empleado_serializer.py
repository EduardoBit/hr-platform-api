from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer
from shared.constants import TiposDocumento, EstadosEmpleado


class RegistrarEmpleadoSerializer(BaseSerializer):
    nombres = serializers.CharField(max_length=150)
    apellidos = serializers.CharField(max_length=150)
    tipo_documento = serializers.ChoiceField(choices=TiposDocumento.CHOICES)
    numero_documento = serializers.CharField(max_length=20)
    correo = serializers.EmailField()
    cargo = serializers.CharField(max_length=100)
    area = serializers.CharField(max_length=100)
    sede_id = serializers.IntegerField()
    fecha_ingreso = serializers.DateField()


class ActualizarEmpleadoSerializer(BaseSerializer):
    nombres = serializers.CharField(max_length=150)
    apellidos = serializers.CharField(max_length=150)
    correo = serializers.EmailField()
    cargo = serializers.CharField(max_length=100)
    area = serializers.CharField(max_length=100)


class AsignarSedeSerializer(BaseSerializer):
    sede_id = serializers.IntegerField()


class EmpleadoOutputSerializer(BaseSerializer):
    id = serializers.IntegerField()
    empresa_id = serializers.IntegerField()
    codigo_unico = serializers.CharField()
    nombres = serializers.CharField()
    apellidos = serializers.CharField()
    tipo_documento = serializers.CharField()
    numero_documento = serializers.CharField()
    correo = serializers.EmailField()
    cargo = serializers.CharField()
    area = serializers.CharField()
    sede_id = serializers.IntegerField()
    sede_nombre = serializers.CharField(allow_null=True)
    estado = serializers.CharField()
    fecha_ingreso = serializers.DateField()
    fecha_creacion = serializers.DateTimeField()