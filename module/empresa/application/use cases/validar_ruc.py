from shared.application.base_use_case import BaseUseCase
from modules.empresa.domain.repositories.empresa_repository import EmpresaRepository
from modules.empresa.domain.exceptions import EmpresaYaRegistradaException


class ValidarRucUseCase(BaseUseCase[str, dict]):
    def __init__(self, empresa_repository: EmpresaRepository, sunat_service):
        self._empresa_repository = empresa_repository
        self._sunat_service = sunat_service

    def execute(self, ruc: str) -> dict:
        if self._empresa_repository.exists_by_ruc(ruc):
            raise EmpresaYaRegistradaException(ruc)
        datos_sunat = self._sunat_service.consultar_ruc(ruc)
        return datos_sunat