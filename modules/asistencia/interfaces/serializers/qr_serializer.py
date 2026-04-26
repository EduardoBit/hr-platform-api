from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer
from shared.constants import QR_EXPIRY_MIN_MINUTES, QR_EXPIRY_MAX_MINUTES


class GenerarQrSerializer(BaseSerializer):
    minutos_vigencia = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=QR_EXPIRY_MIN_MINUTES,
        max_value=QR_EXPIRY_MAX_MINUTES,
    )


class QrOutputSerializer(BaseSerializer):
    token = serializers.CharField()
    sede_id = serializers.IntegerField()
    sede_nombre = serializers.CharField()
    expira_en = serializers.DateTimeField()
    imagen_base64 = serializers.CharField()