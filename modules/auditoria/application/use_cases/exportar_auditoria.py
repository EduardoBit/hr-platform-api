from shared.application.base_use_case import BaseUseCase
from shared.domain.exceptions import InvalidValueException
from modules.auditoria.domain.repositories.auditoria_repository import AuditoriaRepository
from modules.auditoria.application.dtos.auditoria_dto import ExportarAuditoriaInputDTO


class ExportarAuditoriaUseCase(BaseUseCase[ExportarAuditoriaInputDTO, bytes]):
    FORMATOS_VALIDOS = {"PDF", "CSV"}

    def __init__(self, auditoria_repository: AuditoriaRepository, exportacion_service):
        self._auditoria_repository = auditoria_repository
        self._exportacion_service = exportacion_service

    def execute(self, input_dto: ExportarAuditoriaInputDTO) -> bytes:
        if input_dto.formato.upper() not in self.FORMATOS_VALIDOS:
            raise InvalidValueException("formato", f"debe ser uno de: {self.FORMATOS_VALIDOS}")

        registros = self._auditoria_repository.get_global(
            empresa_id=input_dto.empresa_id,
            fecha_desde=input_dto.fecha_desde,
            fecha_hasta=input_dto.fecha_hasta,
            page=1,
            page_size=10000,
        )

        if input_dto.formato.upper() == "PDF":
            return self._exportacion_service.generar_pdf(registros)
        return self._exportacion_service.generar_csv(registros)