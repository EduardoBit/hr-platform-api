from typing import List
from shared.application.base_use_case import BaseUseCase
from modules.auditoria.domain.repositories.auditoria_repository import AuditoriaRepository
from modules.auditoria.application.dtos.auditoria_dto import ConsultarAuditoriaInputDTO, RegistroAuditoriaOutputDTO


class ConsultarAuditoriaUseCase(BaseUseCase[ConsultarAuditoriaInputDTO, List[RegistroAuditoriaOutputDTO]]):
    def __init__(self, auditoria_repository: AuditoriaRepository):
        self._auditoria_repository = auditoria_repository

    def execute(self, input_dto: ConsultarAuditoriaInputDTO) -> List[RegistroAuditoriaOutputDTO]:
        registros = self._auditoria_repository.get_global(
            empresa_id=input_dto.empresa_id,
            usuario_id=input_dto.usuario_id,
            rol=input_dto.rol,
            tipo_evento=input_dto.tipo_evento,
            fecha_desde=input_dto.fecha_desde,
            fecha_hasta=input_dto.fecha_hasta,
            page=input_dto.page,
            page_size=input_dto.page_size,
        )
        return [
            RegistroAuditoriaOutputDTO(
                id=r.id,
                empresa_id=r.empresa_id,
                usuario_id=r.usuario_id,
                rol_usuario=r.rol_usuario,
                tipo_evento=r.tipo_evento,
                descripcion=r.descripcion,
                ip_address=r.ip_address,
                detalles=r.detalles,
                timestamp=r.timestamp,
            )
            for r in registros
        ]