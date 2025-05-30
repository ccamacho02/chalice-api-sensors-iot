import psycopg2.extras
import logging
from typing import List
from src.utils.database import DatabaseConnection
from src.models.sensor import Sensor

logger = logging.getLogger(__name__)


class SensorRepository:

    def get_all_sensors(self) -> List[dict]:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute(
                """SELECT id_sensor, id_zona, nombre_sensor, tipo_sensor, ubicacion_sensor, estado_sensor, fecha_creacion
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

    def get_sensor_events(self, sensor_id: int) -> List[dict]:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute(
                "SELECT tipo_sensor, nombre_sensor FROM sensores WHERE id_sensor = %s;",
                (sensor_id,),
            )

            resultado_sensor = cursor.fetchone()

            tipo_sensor = resultado_sensor["tipo_sensor"]

            tabla_config = {
                "temperatura_humedad": {
                    "tabla": "eventos_temperatura_humedad",
                    "columnas": "id_evento, id_sensor, temperatura, humedad, fecha_creacion",
                },
                "movimiento": {
                    "tabla": "eventos_movimiento",
                    "columnas": "id_evento, id_sensor, movimiento_detectado, fecha_creacion",
                },
                "peso": {
                    "tabla": "eventos_peso",
                    "columnas": "id_evento, id_sensor, peso_kg, fecha_creacion",
                },
            }

            if tipo_sensor not in tabla_config:
                raise ValueError(f"Tipo de sensor desconocido: {tipo_sensor}")

            config = tabla_config[tipo_sensor]

            query = f"""
                SELECT {config['columnas']}
                FROM {config['tabla']}
                WHERE id_sensor = %s
                """

            cursor.execute(query, (sensor_id,))
            resultados = cursor.fetchall()

            eventos = []

            for fila in resultados:
                evento = dict(fila)
                evento["tipo_sensor"] = tipo_sensor
                evento["nombre_sensor"] = resultado_sensor["nombre_sensor"]
                eventos.append(evento)

            cursor.close()
            conn.close()

            return eventos

        except Exception as e:
            logger.error(f"Error fetching sensor events for sensor {sensor_id}: {e}")
            raise
