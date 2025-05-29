import logging
from typing import Dict
from src.models.sensor import Sensor
from src.repositories.sensor_repository import SensorRepository


logger = logging.getLogger(__name__)


class SensorService:
    def __init__(self):
        self.sensor_repository = SensorRepository()

    def get_all_sensors(self) -> Dict:
        try:
            sensores = self.sensor_repository.get_all_sensors()

            # Filtrar por sensores activos
            sensores_activos = [
                sensor for sensor in sensores if sensor["estado_sensor"] == "active"
            ]

            return {
                "sensors": sensores,
                "total_count": len(sensores),
                "active_count": len(sensores_activos),
            }

        except Exception as e:
            logger.error(f"Error al obtener sensores: {e}")
            raise

    def create_sensor(self, sensor_data: Dict) -> Dict:
        try:
            if not sensor_data.get("id_zona"):
                raise ValueError("El campo 'id_zona' es obligatorio.")

            if not sensor_data.get("nombre_sensor"):
                raise ValueError("El campo 'nombre_sensor' es obligatorio.")

            if not sensor_data.get("tipo_sensor"):
                raise ValueError("El campo 'tipo_sensor' es obligatorio.")

            sensor = Sensor(
                id_zona=sensor_data.get("id_zona"),
                nombre_sensor=sensor_data.get("nombre_sensor"),
                tipo_sensor=sensor_data.get("tipo_sensor"),
                ubicacion_sensor=sensor_data.get("ubicacion_sensor", ""),
                estado_sensor=sensor_data.get("estado_sensor", "active"),
            )

            nuevo_sensor = self.sensor_repository.create_sensor(sensor)

            return nuevo_sensor

        except Exception as e:
            logger.error(f"Error al crear sensor: {e}")
            raise
