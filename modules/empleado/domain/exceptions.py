from shared.domain.exceptions import DomainException, BusinessRuleViolationException


class EmpleadoNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El empleado con identificador '{identifier}' no fue encontrado.",
            code="empleado_no_encontrado",
        )


class EmpleadoInactivoException(DomainException):
    def __init__(self):
        super().__init__(
            message="El empleado se encuentra inactivo y no puede realizar esta operación.",
            code="empleado_inactivo",
        )


class EmpleadoYaExisteException(BusinessRuleViolationException):
    def __init__(self, campo: str, valor: str):
        super().__init__(
            message=f"Ya existe un empleado con {campo} '{valor}' en esta empresa."
        )
        self.code = "empleado_ya_existe"


class ModificacionCodigoUnicoException(BusinessRuleViolationException):
    def __init__(self):
        super().__init__(message="El código único de identificación del empleado no puede ser modificado.")
        self.code = "modificacion_codigo_unico"