class DomainException(Exception):
    def __init__(self, message: str, code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    def __init__(self, entity: str, identifier: str | int):
        super().__init__(
            message=f"{entity} con identificador '{identifier}' no fue encontrado.",
            code="not_found",
        )


class EntityAlreadyExistsException(DomainException):
    def __init__(self, entity: str, field: str, value: str):
        super().__init__(
            message=f"{entity} con {field} '{value}' ya existe en el sistema.",
            code="already_exists",
        )


class InvalidValueException(DomainException):
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"El valor del campo '{field}' no es válido: {reason}",
            code="invalid_value",
        )


class BusinessRuleViolationException(DomainException):
    def __init__(self, message: str):
        super().__init__(message=message, code="business_rule_violation")


class UnauthorizedOperationException(DomainException):
    def __init__(self, message: str = "No tiene permisos para realizar esta operación."):
        super().__init__(message=message, code="unauthorized")


class InactiveEntityException(DomainException):
    def __init__(self, entity: str):
        super().__init__(
            message=f"{entity} se encuentra inactivo y no puede realizar esta operación.",
            code="inactive_entity",
        )


class TenantIsolationException(DomainException):
    def __init__(self):
        super().__init__(
            message="Acceso denegado: el recurso no pertenece a su organización.",
            code="tenant_isolation_violation",
        )


class ExternalServiceException(DomainException):
    def __init__(self, service: str, reason: str):
        super().__init__(
            message=f"Error al comunicarse con el servicio externo '{service}': {reason}",
            code="external_service_error",
        )