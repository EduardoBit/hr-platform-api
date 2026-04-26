from shared.domain.exceptions import DomainException


class NotificacionNoEncontradaException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"La notificación con identificador '{identifier}' no fue encontrada.",
            code="notificacion_no_encontrada",
        )


class EnvioNotificacionFallidoException(DomainException):
    def __init__(self, canal: str, razon: str):
        super().__init__(
            message=f"El envío de la notificación por '{canal}' falló: {razon}",
            code="envio_notificacion_fallido",
        )