from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Sensor:
    id: Optional[int] = None
    id_zona: int
    nombre_sensor: str = ""
    tipo_sensor: str = ""
    ubicacion_sensor: str = ""
    estado_sensor: str = "activo"
    fecha_creacion: Optional[datetime] = None
