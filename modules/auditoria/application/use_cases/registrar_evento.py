from datetime import datetime
from shared.application.base_use_case import BaseUseCase
from modules.auditoria.domain.entities.registro_auditoria import RegistroAuditoria
from modules.auditoria.domain.repositories.auditoria_repository import AuditoriaRepository
from modules.auditoria.application.dtos.auditoria_dto import RegistrarEventoInputDTO, RegistroAuditoriaOutputDTO


class RegistrarEventoUseCase(BaseUseCase[RegistrarEventoInputDTO, RegistroAuditoriaOutputDTO]):
    def __init__(self, auditoria_repository: AuditoriaRepository):
        self._auditoria_repository = auditoria_repository

    def execute(self, input_dto: RegistrarEventoInputDTO) -> RegistroAuditoriaOutputDTO:
        registro = RegistroAuditoria(
            id=None,
            empresa_id=input_dto.empresa_id,
            usuario_id=input_dto.usuario_id,
            rol_usuario=input_dto.rol_usuario,
            tipo_evento=input_dto.tipo_evento,
            descripcion=input_dto.descripcion,
            ip_address=input_dto.ip_address,
            detalles=input_dto.detalles,
            timestamp=datetime.now(),
        )
        registro = self._auditoria_repository.save(registro)
        return RegistroAuditoriaOutputDTO(
            id=registro.id,
            empresa_id=registro.empresa_id,
            usuario_id=registro.usuario_id,
            rol_usuario=registro.rol_usuario,
            tipo_evento=registro.tipo_evento,
            descripcion=registro.descripcion,
            ip_address=registro.ip_address,
            detalles=registro.detalles,
            timestamp=registro.timestamp,
        )

    def registrar(
        self,
        empresa_id,
        usuario_id,
        tipo_evento: str,
        descripcion: str,
        ip_address,
        detalles: dict,
    ) -> None:
        self.execute(RegistrarEventoInputDTO(
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            rol_usuario=None,
            tipo_evento=tipo_evento,
            descripcion=descripcion,
            ip_address=ip_address,
            detalles=detalles,
        ))