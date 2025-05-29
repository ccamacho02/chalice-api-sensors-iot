from chalice import Chalice
from src.controllers.sensor_controller import SensorController

app = Chalice(app_name="sensorAPI")


sensor_controler = SensorController()


@app.route("/sensors", methods=["GET"])
def get_sensors():
    return sensor_controler.get_sensors()


@app.route("/sensors", methods=["POST"])
def create_sensor():
    return sensor_controler.create_sensor(app.current_request)
