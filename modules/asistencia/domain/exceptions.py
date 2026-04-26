from shared.domain.exceptions import DomainException, BusinessRuleViolationException


class RegistroAsistenciaNoEncontradoException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"El registro de asistencia con identificador '{identifier}' no fue encontrado.",
            code="registro_no_encontrado",
        )


class QrVencidoException(DomainException):
    def __init__(self):
        super().__init__(
            message="El código QR ha vencido. Solicite uno nuevo al administrador.",
            code="qr_vencido",
        )


class QrSedeIncorrectaException(BusinessRuleViolationException):
    def __init__(self):
        super().__init__(
            message="El código QR no corresponde a la sede asignada al empleado."
        )
        self.code = "qr_sede_incorrecta"


class FueraDeGeovallaException(BusinessRuleViolationException):
    def __init__(self, distancia_metros: float, radio_permitido: int):
        super().__init__(
            message=(
                f"El registro fue rechazado. La ubicación del dispositivo se encuentra a "
                f"{distancia_metros:.0f} metros del centro de la sede, "
                f"superando el radio permitido de {radio_permitido} metros."
            )
        )
        self.code = "fuera_de_geovalla"


class MarcajeDuplicadoException(BusinessRuleViolationException):
    def __init__(self, tipo: str):
        super().__init__(
            message=f"Ya existe un registro de {tipo.lower()} para el día de hoy."
        )
        self.code = "marcaje_duplicado"


class AsistenciaEnPermisoException(BusinessRuleViolationException):
    def __init__(self):
        super().__init__(
            message="No se puede registrar asistencia durante un período cubierto por un permiso aprobado."
        )
        self.code = "asistencia_en_permiso"