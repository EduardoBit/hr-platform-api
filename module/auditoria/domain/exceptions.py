from shared.domain.exceptions import DomainException, BusinessRuleViolationException


class RegistroAuditoriaNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El registro de auditoría con identificador '{identifier}' no fue encontrado.",
            code="registro_auditoria_no_encontrado",
        )


class ModificacionAuditoriaException(BusinessRuleViolationException):
    def __init__(self):
        super().__init__(
            message="Los registros de auditoría son de solo lectura y no pueden ser modificados ni eliminados."
        )
        self.code = "modificacion_auditoria_no_permitida"