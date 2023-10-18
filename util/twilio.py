import os
import json
from twilio.rest import Client
from dotenv import load_dotenv
from twilio.base.exceptions import TwilioException


load_dotenv()


class TwilioManager:
    def __init__(self):
        self.client = Client(os.environ.get('TWILIO_ACCOUNT_SID'),
                             os.environ.get('TWILIO_AUTH_TOKEN'))

    def get_available_numbers(self, country_code):
        try:
            twilio_response = self.client.available_phone_numbers(
                country_code).local.list(voice_enabled=True, sms_enabled=True)

            virtual_numbers = []
            for number in twilio_response:
                virtual_numbers.append(number.phone_number)

            return virtual_numbers

        except TwilioException as exc:
            error_message = str(exc)
            return error_message

    def sendMessage(self, sender, to, message):
        return True
