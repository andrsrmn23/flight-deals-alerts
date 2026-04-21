import requests
from dotenv import load_dotenv
import os

load_dotenv()

class DataManager:
        def __init__(self):
            self.sheety_endpoint = os.environ.get('SHEETY_ENDPOINT')
            self.auth_header = os.environ.get('SHEETY_AUTHORIZATION')
            self.sheety_endpoint_users = os.environ.get('SHEETY_ENDPOINT_USERS')
            self.authorization_header = {
                "Authorization": self.auth_header
            }

            if not self.sheety_endpoint or not self.auth_header:
                raise ValueError("Missing Environmental Variables")

            self.places_data = {}

        def get_destination_data(self):

            response = requests.get(url=self.sheety_endpoint, headers=self.authorization_header)

            response.raise_for_status()
            data = response.json()

            self.places_data = data["prices"]
            return self.places_data

        def update_sheet(self, row_id, new_price):

            new_data = {
                "price" : {
                    "lowestPrice" : new_price,
                }
            }

            requests.put(url=f"{self.sheety_endpoint}/{row_id}", json=new_data, headers=self.authorization_header)

        def get_customer_emails(self):

            response = requests.get(url=self.sheety_endpoint_users, headers=self.authorization_header)

            response.raise_for_status()

            data = response.json()

            return data["users"]

