from shared.domain.exceptions import DomainException, BusinessRuleViolationException


class UsuarioNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El usuario con identificador '{identifier}' no fue encontrado.",
            code="usuario_no_encontrado",
        )


class CredencialesInvalidasException(DomainException):
    def __init__(self):
        super().__init__(
            message="Las credenciales proporcionadas son incorrectas.",
            code="credenciales_invalidas",
        )


class UsuarioBloqueadoException(DomainException):
    def __init__(self):
        super().__init__(
            message="La cuenta ha sido bloqueada por exceder el número máximo de intentos fallidos.",
            code="usuario_bloqueado",
        )


class UsuarioInactivoException(DomainException):
    def __init__(self):
        super().__init__(
            message="La cuenta de usuario se encuentra inactiva.",
            code="usuario_inactivo",
        )


class CodigoUnicoYaExisteException(BusinessRuleViolationException):
    def __init__(self, codigo: str):
        super().__init__(message=f"El código único '{codigo}' ya está asignado a otro usuario.")
        self.code = "codigo_unico_ya_existe"


class RolNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El rol con identificador '{identifier}' no fue encontrado.",
            code="rol_no_encontrado",
        )


class TokenInvalidoException(DomainException):
    def __init__(self):
        super().__init__(
            message="El token proporcionado es inválido o ha expirado.",
            code="token_invalido",
        )


class MaximosIntentosAlcanzadosException(BusinessRuleViolationException):
    def __init__(self, max_intentos: int):
        super().__init__(
            message=f"Se ha alcanzado el límite de {max_intentos} intentos fallidos. La cuenta ha sido bloqueada."
        )
        self.code = "maximos_intentos_alcanzados"