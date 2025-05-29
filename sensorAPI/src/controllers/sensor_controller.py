import logging
from src.services.sensor_service import SensorService
from src.utils.response_helper import ResponseHelper


logger = logging.getLogger(__name__)


class SensorController:
    def __init__(self):
        self.sensor_service = SensorService()
        self.response_helper = ResponseHelper()

    def get_sensors(self):
        try:
            datos_sesores = self.sensor_service.get_all_sensors()
            return self.response_helper.success_response(
                datos_sesores, "Sensores obtenidos correctamente."
            )

        except Exception as e:
            logger.error(f"Error al obtener sensores: {e}")
            return self.response_helper.error_response(str(e))

    def create_sensor(self, request):
        try:
            datos_sensor = request.json_body

            if not datos_sensor:
                return self.response_helper.error_response(
                    "Datos del sensor no proporcionados.", status_code=400
                )

            resultado = self.sensor_service.create_sensor(datos_sensor)
            return self.response_helper.success_response(
                resultado, "Sensor creado correctamente."
            )

        except ValueError as ve:
            return self.response_helper.error_response(str(ve), status_code=400)

        except Exception as e:
            logger.error(f"Error al crear sensor: {e}")
            return self.response_helper.error_response(str(e))
