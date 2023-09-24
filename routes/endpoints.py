from flask import Blueprint, jsonify, request
from util.helper import VonageManager

app = Blueprint('api', __name__)

# Define common error responses


def error_response(status_code, error_message):
    return jsonify({"status": status_code, "error": error_message})


def success_response(status_code, api_response):
    return jsonify({"status": status_code, "response": api_response})


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
            return success_response(200, response)
        else:
            return error_response(502, "Invalid request")
    except Exception as exe:
        return error_response(500, exe)


@app.route("/api/buy-number", methods=['POST'])
def buy_number():
    try:
        vonage_manager = VonageManager()
        response = vonage_manager.buy_number(request.json)
        print("New Error")
        print(type(response))
        print(response)

        if isinstance(response, dict):
            if response['error-code'] == 200:
                updateResp = vonage_manager.update_number(request.json)
            if updateResp['error-code'] == 200:
                return success_response(200, updateResp)
            else:
                return error_response(401, updateResp)
        else:
            return error_response(420, "You are required to complete the sender ID registration process.")
    except Exception as exe:
        return error_response(500, exe)
