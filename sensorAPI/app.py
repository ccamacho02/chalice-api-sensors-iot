from chalice import Chalice, Response
import psycopg2
import psycopg2.extras
import json
import os
from datetime import datetime
import logging


app = Chalice(app_name="sensorAPI")


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configure database connection
DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "database": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD"),
    "port": os.environ.get("DB_PORT", 5432),
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def create_response(data, status_code=200):
    return Response(
        body=json.dumps(data, default=str),
        status_code=status_code,
        headers={"Content-Type": "application/json"},
    )


@app.route("/sensors", methods=["GET"])
def get_sensors():
    # This is a placeholder for the sensors data.
    # In a real application, you would fetch this from a database or another source.
    # sensors_data = [
    #     {"id": 1, "name": "Temperature Sensor", "value": 22.5, "unit": "C"},
    #     {"id": 2, "name": "Humidity Sensor", "value": 45.0, "unit": "%"},
    #     {"id": 3, "name": "Pressure Sensor", "value": 1013.25, "unit": "hPa"},
    # ]
    # return {"sensors": sensors_data}

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            """SELECT id, sensor_name, sensor_type, sensor_location, status, created_at, updated_at
            FROM sensors
            ORDER BY created_at DESC;"""
        )

        sensors = cursor.fetchall()
        cursor.close()
        conn.close()

        return create_response(
            {
                "success": True,
                "data": sensors,
                "count": len(sensors),
            }
        )
    except Exception as e:
        logger.error(f"Error obteniendo sensores: {e}")
        return create_response({"success": False, "error": str(e)}, status_code=500)


@app.route("/sensors", methods=["POST"])
def create_sensor():
    request = app.current_request
    sensor_data = request.json_body

    try:
        # Here you would typically save the sensor data to a database.
        # For this example, we'll just return the data back to the user.
        sensor_id = sensor_data.get("id", None)
        sensor_status = sensor_data.get("status", "active")
        sensor_unit = sensor_data.get("unit", "unknown")
        return {"sensor_id": sensor_id, "status": sensor_status, "unit": sensor_unit}
    except Exception as e:
        raise ValueError(f"Invalid sensor data: {e}")


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
