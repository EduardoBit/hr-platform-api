from shared.domain.exceptions import DomainException, BusinessRuleViolationException


class SolicitudNoEncontradaException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"La solicitud con identificador '{identifier}' no fue encontrada.",
            code="solicitud_no_encontrada",
        )


class TransicionEstadoInvalidaException(BusinessRuleViolationException):
    def __init__(self, estado_actual: str, estado_nuevo: str):
        super().__init__(
            message=f"No es posible cambiar el estado de '{estado_actual}' a '{estado_nuevo}'."
        )
        self.code = "transicion_estado_invalida"


class FechasSolicitudInvalidasException(BusinessRuleViolationException):
    def __init__(self, razon: str):
        super().__init__(message=f"Las fechas de la solicitud no son válidas: {razon}")
        self.code = "fechas_solicitud_invalidas"


class TipoPermisoNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El tipo de permiso con identificador '{identifier}' no fue encontrado.",
            code="tipo_permiso_no_encontrado",
        )


class SolicitudNoPerteneceEmpleadoException(BusinessRuleViolationException):
    def __init__(self):
        super().__init__(message="La solicitud no pertenece al empleado autenticado.")
        self.code = "solicitud_no_pertenece_empleado"