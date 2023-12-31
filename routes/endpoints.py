# from util.agent import Agent
from util.twilio import TwilioManager
from flask import Blueprint, make_response, request

app = Blueprint('api', __name__)


@app.route("/", methods=['GET'])
def index():
    return "Endpoints: Server is running."

#### Number API routes ####


@app.route("/api/numbers/<country_code>", methods=['GET'])
def view_numbers(country_code):
    try:
        twilio_manager = TwilioManager()
        response = twilio_manager.get_available_numbers(country_code)
        if isinstance(response, str):
            return make_response(response, 401)  # 401 for Unauthorized
        else:
            # If it's a successful response, return it with the 200 status code
            return make_response(response, 200)
    except Exception as exe:
        return make_response(str(exe), 500)  # 500 for Internal Server Error


@app.route("/api/purchase-number/<phone_number>", methods=['GET'])
def number_purchase(phone_number):
    try:
        twilio_manager = TwilioManager()
        response = twilio_manager.purchase_number(phone_number)
        if isinstance(response, str):
            return make_response(response, 401)  # 401 for Unauthorized
        else:
            # If it's a successful response, return it with the 200 status code
            return make_response(response.phone_number, 200)
    except Exception as exe:
        return make_response(str(exe), 500)  # 500 for Internal Server Error

#### Verify API Routes ####

@app.route("/api/verify/<number>", methods=['GET'])
def verify_number(number):
    try:
        twilio_manager = TwilioManager()
        response = twilio_manager.verify_number(number)
        if isinstance(response, str):
            return make_response(response, 401)  # 401 for Unauthorized
        else:
            # If it's a successful response, return it with the 200 status code
            return make_response(response.status, 200)
    except Exception as exe:
        return make_response(str(exe), 500)  # 500 for Internal Server Error


@app.route("/api/verify/<number>/<code>", methods=['GET'])
def verify_otp(number, code):
    try:
        twilio_manager = TwilioManager()
        response = twilio_manager.verify_otp(number, code)
        if isinstance(response, str):
            return make_response(response, 401)  # 401 for Unauthorized
        else:
            # If it's a successful response, return it with the 200 status code
            return make_response(response.status, 200)
    except Exception as exe:
        return make_response(str(exe), 500)  # 500 for Internal Server Error
