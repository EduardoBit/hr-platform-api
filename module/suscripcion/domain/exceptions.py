from shared.domain.exceptions import DomainException, BusinessRuleViolationException


class PlanNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El plan con identificador '{identifier}' no fue encontrado.",
            code="plan_no_encontrado",
        )


class SuscripcionNoEncontradaException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"La suscripción con identificador '{identifier}' no fue encontrada.",
            code="suscripcion_no_encontrada",
        )


class LimiteUsuariosAlcanzadoException(BusinessRuleViolationException):
    def __init__(self, plan: str, limite: int):
        super().__init__(
            message=f"Se ha alcanzado el límite de {limite} usuarios activos para el plan {plan}."
        )
        self.code = "limite_usuarios_alcanzado"


class SuscripcionVencidaException(DomainException):
    def __init__(self):
        super().__init__(
            message="La suscripción ha vencido. Por favor, renueve su plan para continuar.",
            code="suscripcion_vencida",
        )


class SuscripcionSuspendidaException(DomainException):
    def __init__(self):
        super().__init__(
            message="La suscripción se encuentra suspendida por falta de pago.",
            code="suscripcion_suspendida",
        )


class CambioPlanNoValidoException(BusinessRuleViolationException):
    def __init__(self, plan_actual: str, plan_nuevo: str, razon: str):
        super().__init__(
            message=f"No es posible cambiar del plan '{plan_actual}' al plan '{plan_nuevo}': {razon}"
        )
        self.code = "cambio_plan_no_valido"