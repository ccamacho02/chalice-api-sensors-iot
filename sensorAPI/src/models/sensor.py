from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Sensor:
    id_zona: int
    id: Optional[int] = None
    nombre_sensor: str = ""
    tipo_sensor: str = ""
    ubicacion_sensor: str = ""
    estado_sensor: str = "active"
    fecha_creacion: Optional[datetime] = None
