import json
from flask import Blueprint, request, jsonify
from util.helper import VonageManager
# Create a Blueprint instance
app = Blueprint('api', __name__)


@app.route("/", methods=['GET'])
def index():
    return "Endpoints: Server is running."

# country code should be in capital letters


@app.route("/api/numbers/<country_code>", methods=['GET'])
def view_numbers(country_code):
    try:
        vonage_manager = VonageManager()
        response = vonage_manager.get_available_numbers(country_code)
        if isinstance(response, str):
            return jsonify({"status": 400, "error": response})
        return jsonify({"status": 200, "response": response})
    except Exception as exe:
        return jsonify({"status": 500, "error": exe})
