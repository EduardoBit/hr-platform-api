from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearSedeInputDTO:
    empresa_id: int
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    radio_metros: int


@dataclass
class ActualizarSedeInputDTO:
    sede_id: int
    empresa_id: int
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    radio_metros: int


@dataclass
class SedeOutputDTO:
    id: int
    empresa_id: int
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    radio_metros: int
    es_activa: bool