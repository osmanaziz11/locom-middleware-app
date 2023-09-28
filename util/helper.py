import os
import vonage
from dotenv import load_dotenv

load_dotenv()


class VonageManager:
    def __init__(self):
        self.client = vonage.Client(key=os.environ.get('VONAGE_API_KEY'),
                                    secret=os.environ.get('VONAGE_API_SECRET'))

        self.VONAGE_NUMBER_CONFIG = {
            "type": "mobile-lvn",
            "features": "SMS,VOICE"
        }

        self.VONAGE_APP_CONFIG = {
            "msisdn": "",
            "country": "",
            "app_id": os.environ.get('VONAGE_APP_ID'),
        }

    def get_available_numbers(self, country_code):
        try:
            response = self.client.numbers.get_available_numbers(
                country_code,
                self.VONAGE_NUMBER_CONFIG
            )
            return response
        except Exception as exc:
            return exc

    def buy_number(self, number_info):
        try:
            response = self.client.numbers.buy_number(number_info)
            return response
        except Exception as exc:
            return exc

    def update_number(self, number_info):
        try:
            self.VONAGE_APP_CONFIG['msisdn'] = number_info['msisdn']
            self.VONAGE_APP_CONFIG['country'] = number_info['country']
            response = self.client.numbers.update_number(
                self.VONAGE_APP_CONFIG)
            return response
        except Exception as exc:
            return exc

    def verify_number(self, number):
        try:
            
           client = vonage.Client(
                application_id="5a0fdc41-15e5-4b1b-b669-8f010afa2e75",
                private_key="./key.txt",
                )
           params = {
                'brand': "Locom AI",
                'workflow': [
                    {'channel': 'sms', 'to': number},
                        ],
                }

           return client.verify2.new_request(params)
        except Exception as exc:
            return exc
