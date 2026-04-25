from datetime import datetime
from shared.application.base_use_case import BaseUseCase
from modules.suscripcion.domain.entities.suscripcion import Suscripcion
from modules.suscripcion.domain.repositories.suscripcion_repository import SuscripcionRepository
from modules.suscripcion.domain.repositories.plan_repository import PlanRepository
from modules.suscripcion.domain.exceptions import PlanNoEncontradoException


class ActivarPeriodoPruebaUseCase(BaseUseCase[dict, None]):
    def __init__(
        self,
        suscripcion_repository: SuscripcionRepository,
        plan_repository: PlanRepository,
    ):
        self._suscripcion_repository = suscripcion_repository
        self._plan_repository = plan_repository

    def execute(self, input_dto: dict) -> None:
        plan = self._plan_repository.get_by_id(input_dto["plan_id"])
        if not plan:
            raise PlanNoEncontradoException(str(input_dto["plan_id"]))

        suscripcion = Suscripcion(
            id=None,
            empresa_id=input_dto["empresa_id"],
            plan_id=plan.id,
            plan_nombre=plan.nombre,
            plan_limite_usuarios=plan.limite_usuarios,
            estado="TRIAL",
            fecha_inicio=datetime.now(),
            fecha_fin_trial=None,
            fecha_proxima_facturacion=None,
            usuarios_activos=0,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=None,
        )
        suscripcion.activar_trial()
        self._suscripcion_repository.save(suscripcion)