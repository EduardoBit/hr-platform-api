from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from modules.solicitud.application.dtos.tipo_permiso_dto import (
    CrearTipoPermisoInputDTO, ActualizarTipoPermisoInputDTO
)
from modules.solicitud.interfaces.serializers.tipo_permiso_serializer import (
    CrearTipoPermisoSerializer, TipoPermisoOutputSerializer
)
from modules.solicitud.infrastructure.repositories.tipo_permiso_repository_impl import DjangoTipoPermisoRepository
from modules.solicitud.application.use_cases.configurar_tipo_permiso import (
    CrearTipoPermisoUseCase, ActualizarTipoPermisoUseCase
)
from modules.solicitud.application.dtos.tipo_permiso_dto import TipoPermisoOutputDTO


class TipoPermisoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tipos = DjangoTipoPermisoRepository().get_by_empresa(request.empresa_id)
        outputs = [
            TipoPermisoOutputDTO(
                id=t.id, empresa_id=t.empresa_id, nombre=t.nombre,
                descripcion=t.descripcion, requiere_adjunto=t.requiere_adjunto,
                es_activo=t.es_activo,
            )
            for t in tipos
        ]
        return Response(TipoPermisoOutputSerializer(outputs, many=True).data)

    def post(self, request):
        serializer = CrearTipoPermisoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output = CrearTipoPermisoUseCase(DjangoTipoPermisoRepository()).execute(
            CrearTipoPermisoInputDTO(empresa_id=request.empresa_id, **serializer.validated_data)
        )
        return Response(TipoPermisoOutputSerializer(output).data, status=status.HTTP_201_CREATED)


class TipoPermisoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, tipo_id):
        serializer = CrearTipoPermisoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output = ActualizarTipoPermisoUseCase(DjangoTipoPermisoRepository()).execute(
            ActualizarTipoPermisoInputDTO(
                tipo_permiso_id=tipo_id,
                empresa_id=request.empresa_id,
                **serializer.validated_data,
            )
        )
        return Response(TipoPermisoOutputSerializer(output).data)