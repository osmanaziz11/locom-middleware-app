from flask import Blueprint, jsonify
from util.helper import VonageManager
import json

app = Blueprint('api', __name__)


@app.route("/", methods=['GET'])
def index():
    return "Endpoints: Server is running."


@app.route("/api/numbers/<country_code>", methods=['GET'])
def view_numbers(country_code):
    try:
        vonage_manager = VonageManager()
        response = vonage_manager.get_available_numbers(country_code)
        if isinstance(response, str):
            return jsonify({"status": 400, "response": "Invalid response object from Vonage"})
        if isinstance(response, dict):
            return jsonify({"status": 200, "response": response})
        return jsonify({"status": 400, "response": "nvalid response object from Vonage"})
    except Exception as exe:
        return jsonify({"status": 500, "error": exe})
