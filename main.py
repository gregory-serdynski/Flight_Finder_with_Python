import data_manager
from notification_manager import NotificationManager as send_notification
import data_manager as dm

# -------OPTIONAL------- #
# data_manager.update_iata()
# ---------END---------- #

# ----------------- Register User ------------------ #

# user_choice = input("Do you want to register new user? Type 'y' or 'n': ")

# if user_choice == "y":
#     dm.register_user()

# ----------------- Search Flights ------------------ #
print("Searching for flights. Please wait.")

cities_data = dm.get_cities_data()
destination_index = 0

# Searching to find the cheapest flight to all  destination places
for data in cities_data["flights"]:
    destination_iata = data["iataCode"]

    flight_data = dm.get_flight_data(destination_iata)

    # Search Results
    destination_city = data["city"]
    departure_city = flight_data["route"][0]["cityFrom"]
    departure_iata = flight_data["route"][0]["flyFrom"]

    departure_date = flight_data["route"][0]["local_departure"].split("T")[0]
    return_date = flight_data["route"][-1]["local_departure"].split("T")[0]

    flight_price = int(flight_data["fare"]["adults"])
    minimal_price = cities_data["flights"][destination_index]["highestPrice"]

    # Checking if price is lower than required "lowest price"
    if flight_price <= minimal_price:
        print(f"We found cheap flight to {destination_city}.")
        send_notification(departure_city, departure_iata, destination_city, destination_iata,
                          flight_price, departure_date, return_date)

    else:
        print(f"Currently cannot find cheap flights to {destination_city}.")

    destination_index += 1






