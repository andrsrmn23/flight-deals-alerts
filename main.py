import requests_cache
from datetime import datetime, timedelta
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import cheapest_flight
from notification_manager import NotificationManager
import time


requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

# SHEETY
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
sheet_data_users = data_manager.get_customer_emails()

email_list = [row["email"] for row in sheet_data_users]

# TIME / DATES
tomorrow = datetime.now() + timedelta(days=1)
one_month_from_today = datetime.now() + timedelta(days=30)
from_time = tomorrow.strftime("%Y-%m-%d")
to_time = one_month_from_today.strftime("%Y-%m-%d")

# FLIGHT SEARCH

flight_search = FlightSearch()
notification_manager = NotificationManager()

for destination in sheet_data:
    print(f"Searching for direct flights to {destination['city']}....")

    flights_result = flight_search.check_flights("SJO", destination["iataCode"], from_time, to_time)

    flight_data_cheapest = cheapest_flight(flights_result, to_time)

    pprint(f"{destination['city']}: USD {flight_data_cheapest.price}")

    if flight_data_cheapest.price == "N/A":
        pprint(f"No direct flights to {destination['city']}. Looking for indirect flights....")

        stop_flights = flight_search.check_flights("SJO", destination["iataCode"], from_time, to_time, is_direct=False)

        flight_data_cheapest = cheapest_flight(stop_flights, to_time)
        print(f"Cheapest flight with stops is: USD {flight_data_cheapest.price}")

    if flight_data_cheapest.price != "N/A" and flight_data_cheapest.price < destination['lowestPrice']:

        data_manager.update_sheet(destination["id"], flight_data_cheapest.price)

        if flight_data_cheapest.stops == 0:
            message = f"Low price alert! Only USD {flight_data_cheapest.price} to fly direct "\
                      f"from {flight_data_cheapest.origin} to {flight_data_cheapest.destination}, "\
                      f"on {flight_data_cheapest.out_date} until {flight_data_cheapest.return_date}."
        else:
            message = f"Low price alert! Only USD {flight_data_cheapest.price} to fly "\
                      f"from {flight_data_cheapest.origin} to {flight_data_cheapest.destination}, "\
                      f"with {flight_data_cheapest.stops} stop(s) "\
                      f"departing on {flight_data_cheapest.out_date} and returning on {flight_data_cheapest.return_date}."

        notification_manager.send_message(message=message)

        notification_manager.send_emails(emails=email_list, message=message)


    time.sleep(15)





















































"""
ENDPOINT URL AND AFTER THE QUESTION MARK THERE ARE PARAMETERS ||| ENDPOINT ? KEY = VALUE & .....
response codes apis
1XX: Hold on
2XX: SUCCESSFUL
3XX: MISSING VERIFICATION
4XX: BAD REQUEST
5XX: BAD RESPONSE

CREATE AND ENVIRONMENTAL VARIABLE:
1.TERMINAL
2. export variable_name=value
3.to check it type env on terminal
4. Use os module to tap into the varialbe: import os-------api_key = os.environ.get('variable_name')

REQUEST HEADERS:

headers = {
    X-USER-TOKEN": TOKEN,
}

then pass headers in request after the params or json
"""
