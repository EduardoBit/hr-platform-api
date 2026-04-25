from shared.application.base_use_case import BaseUseCase
from modules.suscripcion.domain.repositories.suscripcion_repository import SuscripcionRepository
from modules.suscripcion.domain.exceptions import SuscripcionNoEncontradaException


class VerificarLimitesUseCase(BaseUseCase[int, None]):
    def __init__(self, suscripcion_repository: SuscripcionRepository):
        self._suscripcion_repository = suscripcion_repository

    def execute(self, empresa_id: int) -> None:
        suscripcion = self._suscripcion_repository.get_by_empresa(empresa_id)
        if not suscripcion:
            raise SuscripcionNoEncontradaException(str(empresa_id))
        suscripcion.verificar_puede_operar()
        suscripcion.verificar_limite_usuarios()