
class FlightData:
    def __init__(self, price, origin, destination, out_date, return_date, stops):
        self.price = price
        self.origin = origin
        self.destination = destination
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def cheapest_flight(data, return_date):

    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    total_flights = data.get("best_flights", []) + data.get("other_flights", [])

    flight_one = total_flights[0]
    destination = flight_one["flights"][0]["arrival_airport"]["id"]
    origin = flight_one["flights"][0]["departure_airport"]["id"]
    lowest_price = flight_one["price"]
    out_date = flight_one["flights"][0]["departure_airport"]["time"].split(" ")[0]

    stops = len(flight_one["flights"]) - 1

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

    for flight in total_flights:
        try:
            price = flight["price"]
        except KeyError:
            print("Flight has no price")
            continue

        if price < lowest_price:

            lowest_price = price
            destination = flight["flights"][0]["arrival_airport"]["id"]
            origin = flight["flights"][0]["departure_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            stops = len(flight["flights"]) - 1
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

            print(f"Lowest price to {destination} is USD {lowest_price}")

    return cheapest_flight

