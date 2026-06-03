from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from shared.infrastructure.permissions import IsSuperAdminOrPropietario
from modules.usuario.infrastructure.repositories.usuario_repository_impl import DjangoUsuarioRepository
from modules.usuario.infrastructure.repositories.rol_repository_impl import DjangoRolRepository
from modules.usuario.infrastructure.services.jwt_service import PasswordService
from modules.usuario.application.use_cases.crear_usuario import CrearUsuarioUseCase
from modules.usuario.application.dtos.usuario_dto import CrearUsuarioInputDTO
from modules.usuario.interfaces.serializers.usuario_serializer import UsuarioOutputSerializer
from modules.auditoria.infrastructure.repositories.auditoria_repository_impl import DjangoAuditoriaRepository
from modules.auditoria.application.use_cases.registrar_evento import RegistrarEventoUseCase
from rest_framework import serializers
from shared.interfaces.base_serializer import BaseSerializer


class CrearAdminSerializer(BaseSerializer):
    correo = serializers.EmailField()
    contrasena = serializers.CharField(min_length=8, write_only=True)


def _auditoria():
    return RegistrarEventoUseCase(DjangoAuditoriaRepository())


def _to_output_dto(usuario):
    from modules.usuario.application.dtos.usuario_dto import UsuarioOutputDTO
    return UsuarioOutputDTO(
        id=usuario.id,
        empresa_id=usuario.empresa_id,
        codigo_unico=str(usuario.codigo_unico),
        correo=str(usuario.correo),
        rol="ADMIN",
        estado=usuario.estado,
        ultimo_acceso=usuario.ultimo_acceso,
        fecha_creacion=usuario.fecha_creacion,
    )


class AdministradoresView(APIView):
    permission_classes = [IsSuperAdminOrPropietario]

    def get(self, request, empresa_id):
        repo = DjangoUsuarioRepository()
        usuarios = repo.get_by_empresa(empresa_id, rol="ADMIN")
        dtos = [_to_output_dto(u) for u in usuarios]
        return Response(UsuarioOutputSerializer(dtos, many=True).data)

    def post(self, request, empresa_id):
        serializer = CrearAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CrearUsuarioUseCase(
            usuario_repository=DjangoUsuarioRepository(),
            rol_repository=DjangoRolRepository(),
            password_service=PasswordService(),
            auditoria_use_case=_auditoria(),
        )
        output = use_case.execute(CrearUsuarioInputDTO(
            empresa_id=empresa_id,
            rol_nombre="ADMIN",
            correo=serializer.validated_data["correo"],
            contrasena=serializer.validated_data["contrasena"],
        ))

        try:
            from modules.notificacion.infrastructure.services.email_service import EmailService
            EmailService().notificar_bienvenida_empleado(output.correo, output.codigo_unico)
        except Exception:
            pass

        return Response(UsuarioOutputSerializer(output).data, status=status.HTTP_201_CREATED)
