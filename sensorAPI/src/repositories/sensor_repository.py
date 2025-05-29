import psycopg2.extras
import logging
from typing import List, Optional
from src.utils.database import DatabaseConnection
from src.models.sensor import Sensor

logger = logging.getLogger(__name__)


class SensorRepository:

    def get_all_sensors(self) -> List[dict]:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute(
                """SELECT id_sensor, nombre_sensor, tipo_sensor, ubicacion_sensor, estado_sensor, fecha_creacion
                FROM sensores
                ORDER BY fecha_creacion DESC;"""
            )

            sensors = cursor.fetchall()
            cursor.close()
            conn.close()

            return sensors

        except Exception as e:
            logger.error(f"Error fetching sensors: {e}")
            raise

    def create_sensor(self, sensor: Sensor) -> dict:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO sensores (id_zona, nombre_sensor, tipo_sensor, ubicacion_sensor, estado_sensor)
                VALUES (%s, %s, %s, %s, )
                RETURNING id_sensor, id_zona, nombre_sensor, tipo_sensor, ubicacion_sensor, estado_sensor, fecha_creacion""",
                (
                    sensor.id_zona,
                    sensor.nombre_sensor,
                    sensor.tipo_sensor,
                    sensor.ubicacion_sensor,
                    sensor.estado_sensor,
                ),
            )

            nuevo_sensor = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()

            return nuevo_sensor

        except Exception as e:
            logger.error(f"Error creating sensor: {e}")
            raise
