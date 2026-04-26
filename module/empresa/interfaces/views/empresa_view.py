from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from modules.empresa.application.dtos.empresa_dto import RegistrarEmpresaInputDTO, ActualizarEmpresaInputDTO
from modules.empresa.interfaces.serializers.empresa_serializer import (
    RegistrarEmpresaSerializer,
    ActualizarEmpresaSerializer,
    EmpresaOutputSerializer,
)
from modules.empresa.infrastructure.repositories.empresa_repository_impl import DjangoEmpresaRepository
from modules.empresa.infrastructure.services.sunat_service import SunatService
from modules.empresa.application.use_cases.registrar_empresa import RegistrarEmpresaUseCase
from modules.empresa.application.use_cases.actualizar_empresa import ActualizarEmpresaUseCase
from modules.empresa.application.use_cases.suspender_empresa import SuspenderEmpresaUseCase
from modules.empresa.application.use_cases.validar_ruc import ValidarRucUseCase


def _build_registrar_use_case():
    from modules.usuario.infrastructure.repositories.usuario_repository_impl import DjangoUsuarioRepository
    from modules.usuario.infrastructure.repositories.rol_repository_impl import DjangoRolRepository
    from modules.usuario.infrastructure.services.jwt_service import PasswordService
    from modules.suscripcion.infrastructure.repositories.suscripcion_repository_impl import DjangoSuscripcionRepository
    from modules.suscripcion.infrastructure.repositories.plan_repository_impl import DjangoPlanRepository
    from modules.suscripcion.application.use_cases.activar_periodo_prueba import ActivarPeriodoPruebaUseCase
    from modules.auditoria.infrastructure.repositories.auditoria_repository_impl import DjangoAuditoriaRepository
    from modules.auditoria.application.use_cases.registrar_evento import RegistrarEventoUseCase
    from modules.notificacion.infrastructure.services.email_service import EmailService

    class _NotifAdapter:
        def __init__(self, svc):
            self._svc = svc

        def notificar_registro_empresa(self, correo, empresa):
            self._svc.notificar_registro_empresa(correo, empresa.razon_social)

    class _UsuarioAdapter:
        def crear_propietario(self, empresa_id, correo, contrasena):
            from modules.usuario.application.use_cases.crear_usuario import CrearUsuarioUseCase
            from modules.usuario.application.dtos.usuario_dto import CrearUsuarioInputDTO
            uc = CrearUsuarioUseCase(
                usuario_repository=DjangoUsuarioRepository(),
                rol_repository=DjangoRolRepository(),
                password_service=PasswordService(),
                auditoria_use_case=RegistrarEventoUseCase(DjangoAuditoriaRepository()),
            )
            uc.execute(CrearUsuarioInputDTO(
                empresa_id=empresa_id, rol_nombre="PROPIETARIO",
                correo=correo, contrasena=contrasena,
            ))

    class _SuscripcionAdapter:
        def activar_trial(self, empresa_id, plan_id):
            ActivarPeriodoPruebaUseCase(
                DjangoSuscripcionRepository(), DjangoPlanRepository()
            ).execute({"empresa_id": empresa_id, "plan_id": plan_id})

    return RegistrarEmpresaUseCase(
        empresa_repository=DjangoEmpresaRepository(),
        sunat_service=SunatService(),
        usuario_use_case=_UsuarioAdapter(),
        suscripcion_use_case=_SuscripcionAdapter(),
        auditoria_use_case=RegistrarEventoUseCase(DjangoAuditoriaRepository()),
        notificacion_use_case=_NotifAdapter(EmailService()),
    )


class ValidarRucView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, ruc):
        use_case = ValidarRucUseCase(DjangoEmpresaRepository(), SunatService())
        datos = use_case.execute(ruc)
        return Response({"status": "ok", "data": datos})


class RegistrarEmpresaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrarEmpresaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        use_case = _build_registrar_use_case()
        output = use_case.execute(RegistrarEmpresaInputDTO(**d))
        return Response(EmpresaOutputSerializer(output).data, status=status.HTTP_201_CREATED)


class EmpresaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, empresa_id):
        from modules.empresa.domain.exceptions import EmpresaNoEncontradaException
        empresa = DjangoEmpresaRepository().get_by_id(empresa_id)
        if not empresa:
            raise EmpresaNoEncontradaException(str(empresa_id))
        from modules.empresa.application.dtos.empresa_dto import EmpresaOutputDTO
        output = EmpresaOutputDTO(
            id=empresa.id, ruc=str(empresa.ruc), razon_social=empresa.razon_social,
            nombre_comercial=empresa.nombre_comercial, correo=str(empresa.correo),
            telefono=empresa.telefono, direccion=empresa.direccion,
            logo_url=empresa.logo_url, estado=empresa.estado,
            fecha_registro=empresa.fecha_registro,
        )
        return Response(EmpresaOutputSerializer(output).data)

    def patch(self, request, empresa_id):
        serializer = ActualizarEmpresaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        use_case = ActualizarEmpresaUseCase(DjangoEmpresaRepository())
        output = use_case.execute(ActualizarEmpresaInputDTO(empresa_id=empresa_id, **d))
        return Response(EmpresaOutputSerializer(output).data)


class SuspenderEmpresaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, empresa_id):
        from modules.auditoria.infrastructure.repositories.auditoria_repository_impl import DjangoAuditoriaRepository
        from modules.auditoria.application.use_cases.registrar_evento import RegistrarEventoUseCase
        use_case = SuspenderEmpresaUseCase(
            DjangoEmpresaRepository(),
            RegistrarEventoUseCase(DjangoAuditoriaRepository()),
        )
        use_case.execute({
            "empresa_id": empresa_id,
            "suspendido_por_id": request.usuario_id,
            "razon": request.data.get("razon", ""),
            "ip_address": request.META.get("REMOTE_ADDR"),
        })
        return Response({"status": "ok"})