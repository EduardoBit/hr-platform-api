from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from modules.suscripcion.interfaces.serializers.suscripcion_serializer import (
    CambiarPlanSerializer,
    SuscripcionOutputSerializer,
)
from modules.suscripcion.application.dtos.suscripcion_dto import CambiarPlanInputDTO
from modules.suscripcion.infrastructure.repositories.suscripcion_repository_impl import DjangoSuscripcionRepository
from modules.suscripcion.infrastructure.repositories.plan_repository_impl import DjangoPlanRepository
from modules.suscripcion.application.use_cases.obtener_estado import ObtenerEstadoSuscripcionUseCase
from modules.suscripcion.application.use_cases.cambiar_plan import CambiarPlanUseCase


class SuscripcionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        output = ObtenerEstadoSuscripcionUseCase(DjangoSuscripcionRepository()).execute(
            request.empresa_id
        )
        return Response(SuscripcionOutputSerializer(output).data)


class CambiarPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CambiarPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output = CambiarPlanUseCase(
            DjangoSuscripcionRepository(), DjangoPlanRepository()
        ).execute(CambiarPlanInputDTO(
            empresa_id=request.empresa_id,
            nuevo_plan_id=serializer.validated_data["nuevo_plan_id"],
        ))
        return Response(SuscripcionOutputSerializer(output).data)