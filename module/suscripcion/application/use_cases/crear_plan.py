from datetime import datetime
from shared.application.base_use_case import BaseUseCase
from modules.suscripcion.domain.entities.plan import Plan
from modules.suscripcion.domain.repositories.plan_repository import PlanRepository
from modules.suscripcion.application.dtos.plan_dto import CrearPlanInputDTO, PlanOutputDTO


class CrearPlanUseCase(BaseUseCase[CrearPlanInputDTO, PlanOutputDTO]):
    def __init__(self, plan_repository: PlanRepository):
        self._plan_repository = plan_repository

    def execute(self, input_dto: CrearPlanInputDTO) -> PlanOutputDTO:
        plan = Plan(
            id=None,
            nombre=input_dto.nombre,
            precio_mensual=input_dto.precio_mensual,
            limite_usuarios=input_dto.limite_usuarios,
            almacenamiento_gb=input_dto.almacenamiento_gb,
            es_activo=True,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=None,
        )
        plan = self._plan_repository.save(plan)
        return PlanOutputDTO(
            id=plan.id,
            nombre=plan.nombre,
            precio_mensual=plan.precio_mensual,
            limite_usuarios=plan.limite_usuarios,
            almacenamiento_gb=plan.almacenamiento_gb,
            es_activo=plan.es_activo,
        )