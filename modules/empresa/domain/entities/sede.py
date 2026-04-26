from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from shared.domain.value_objects import Coordenadas, RadioMetros


@dataclass
class Sede:
    empresa_id: int
    nombre: str
    direccion: str
    coordenadas: Coordenadas
    radio_metros: RadioMetros
    id: Optional[int] = None
    es_activa: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
