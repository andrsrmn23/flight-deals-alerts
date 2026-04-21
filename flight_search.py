from dotenv import load_dotenv
import os
import requests

load_dotenv()

class FlightSearch:
    def __init__(self):
        self._api_key = os.environ.get('SERPAPI_API_KEY')
        self.serp_endpoint = os.environ.get('SERPAPI_ENDPOINT')

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):

        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time,
            "return_date": to_time,
            "type": "1",
            "adults": "1",
            "currency": "USD",
            "api_key": self._api_key,
        }

        if is_direct:
            params["stops"] = "1"

        response = requests.get(url=self.serp_endpoint, params=params)

        response.raise_for_status()

        result = response.json()

        return result


