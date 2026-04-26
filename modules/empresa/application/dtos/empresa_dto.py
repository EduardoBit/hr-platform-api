from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RegistrarEmpresaInputDTO:
    ruc: str
    correo: str
    telefono: str
    direccion: str
    contrasena: str
    plan_id: int


@dataclass
class ActualizarEmpresaInputDTO:
    empresa_id: int
    nombre_comercial: str
    telefono: str
    direccion: str
    logo_url: Optional[str]


@dataclass
class EmpresaOutputDTO:
    id: int
    ruc: str
    razon_social: str
    nombre_comercial: str
    correo: str
    telefono: str
    direccion: str
    logo_url: Optional[str]
    estado: str
    fecha_registro: datetime


@dataclass
class EmpresaListOutputDTO:
    id: int
    ruc: str
    razon_social: str
    estado: str
    plan_nombre: Optional[str]
    fecha_registro: datetime