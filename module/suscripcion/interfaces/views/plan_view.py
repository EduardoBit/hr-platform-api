from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from modules.suscripcion.interfaces.serializers.plan_serializer import PlanOutputSerializer
from modules.suscripcion.infrastructure.repositories.plan_repository_impl import DjangoPlanRepository
from modules.suscripcion.application.dtos.plan_dto import PlanOutputDTO


class PlanListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        planes = DjangoPlanRepository().get_all_activos()
        outputs = [
            PlanOutputDTO(
                id=p.id, nombre=p.nombre, precio_mensual=p.precio_mensual,
                limite_usuarios=p.limite_usuarios, almacenamiento_gb=p.almacenamiento_gb,
                es_activo=p.es_activo,
            )
            for p in planes
        ]
        return Response(PlanOutputSerializer(outputs, many=True).data)