from flask import Blueprint, jsonify, request
from util.helper import VonageManager

app = Blueprint('api', __name__)

# Define common error responses


def error_response(status_code, error_message):
    return jsonify({"status": status_code, "error": error_message})


@app.route("/", methods=['GET'])
def index():
    return "Endpoints: Server is running."


@app.route("/api/numbers/<country_code>", methods=['GET'])
def view_numbers(country_code):
    try:
        vonage_manager = VonageManager()
        response = vonage_manager.get_available_numbers(country_code)

        if isinstance(response, str):
            return error_response(401, "Authentication is required, and the provided credentials are invalid or missing.")
        elif isinstance(response, dict):
            return jsonify({"status": 200, "response": response})
        else:
            return error_response(502, "Invalid request")
    except Exception as exe:
        return error_response(500, exe)


@app.route("/api/buy-number", methods=['POST'])
def buy_number():
    try:
        vonage_manager = VonageManager()
        response = vonage_manager.buy_number(request.json)
        print("Error Handler")
        print(response['error-code'])
        # if isinstance(response, dict):
        #     if response['error-code'] == 200:
        #         response = vonage_manager.update_number(request.json)
        #     if response['error-code'] == 200:
        #         return jsonify({"status": 200, "response": response})
        #     else:
        #         return error_response(401, "Error Updating Number")
        # else:
        return error_response(401, "Error purchasing number.")
    except Exception as exe:
        return error_response(500, exe)
