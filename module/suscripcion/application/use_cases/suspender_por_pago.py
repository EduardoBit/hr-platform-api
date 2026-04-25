from shared.application.base_use_case import BaseUseCase
from modules.suscripcion.domain.repositories.suscripcion_repository import SuscripcionRepository
from modules.empresa.domain.repositories.empresa_repository import EmpresaRepository
from shared.constants import PAYMENT_GRACE_DAYS


class SuspenderPorPagoUseCase(BaseUseCase[None, None]):
    def __init__(
        self,
        suscripcion_repository: SuscripcionRepository,
        empresa_repository: EmpresaRepository,
        notificacion_use_case,
    ):
        self._suscripcion_repository = suscripcion_repository
        self._empresa_repository = empresa_repository
        self._notificacion_use_case = notificacion_use_case

    def execute(self, input_dto=None) -> None:
        suscripciones_vencidas = self._suscripcion_repository.get_vencidas_sin_pago(PAYMENT_GRACE_DAYS)

        for suscripcion in suscripciones_vencidas:
            suscripcion.suspender()
            self._suscripcion_repository.save(suscripcion)

            empresa = self._empresa_repository.get_by_id(suscripcion.empresa_id)
            if empresa:
                empresa.suspender()
                self._empresa_repository.save(empresa)
                self._notificacion_use_case.notificar_suspension_por_pago(
                    correo=str(empresa.correo),
                    empresa_nombre=empresa.razon_social,
                )