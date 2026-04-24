import re
import uuid
from dataclasses import dataclass
from shared.domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.value):
            raise InvalidValueException("email", "formato de correo electrónico inválido.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Ruc:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{11}$", self.value):
            raise InvalidValueException("ruc", "debe contener exactamente 11 dígitos numéricos.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class CodigoUnico:
    value: str

    @classmethod
    def generate(cls) -> "CodigoUnico":
        raw = uuid.uuid4().hex[:10].upper()
        return cls(value=raw)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Coordenadas:
    latitud: float
    longitud: float

    def __post_init__(self):
        if not (-90 <= self.latitud <= 90):
            raise InvalidValueException("latitud", "debe estar entre -90 y 90.")
        if not (-180 <= self.longitud <= 180):
            raise InvalidValueException("longitud", "debe estar entre -180 y 180.")

    def __str__(self) -> str:
        return f"{self.latitud},{self.longitud}"


@dataclass(frozen=True)
class RadioMetros:
    value: int

    def __post_init__(self):
        if self.value < 10 or self.value > 10000:
            raise InvalidValueException("radio_metros", "debe estar entre 10 y 10,000 metros.")

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class NumeroDocumento:
    value: str
    tipo: str

    TIPOS_VALIDOS = {"DNI", "CE", "PASAPORTE", "RUC"}

    def __post_init__(self):
        if self.tipo not in self.TIPOS_VALIDOS:
            raise InvalidValueException("tipo_documento", f"debe ser uno de: {self.TIPOS_VALIDOS}.")
        if self.tipo == "DNI" and not re.match(r"^\d{8}$", self.value):
            raise InvalidValueException("numero_documento", "DNI debe tener exactamente 8 dígitos.")
        if not self.value.strip():
            raise InvalidValueException("numero_documento", "no puede estar vacío.")

    def __str__(self) -> str:
        return self.value