from chalice import Response
import json


class ResponseHelper:
    @staticmethod
    def create_response(data, status_code=200):
        return Response(
            body=json.dumps(data, default=str),
            status_code=status_code,
            headers={"Content-Type": "application/json"},
        )

    @staticmethod
    def success_response(data, message="Success"):
        return ResponseHelper.create_response(
            {"success": True, "message": message, "data": data}
        )

    @staticmethod
    def error_response(error_message, status_code=500):
        return ResponseHelper.create_response(
            {"success": False, "error": error_message}, status_code=status_code
        )
