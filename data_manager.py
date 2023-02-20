import requests
import datetime as dt
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv

load_dotenv("env")
TEQUILA_API = os.getenv("TEQUILA_API")

TEQUILA_HEADERS = {"apikey": TEQUILA_API}
destination_cities_endpoint = "https://api.sheety.co/0ed6dc8c31e4a8a86db86ee622ee2195/flightSearch/flights"
users_endpoint = "https://api.sheety.co/0ed6dc8c31e4a8a86db86ee622ee2195/flightSearch/users"

iata_search_endpoint = "https://api.tequila.kiwi.com/locations/query"
flight_search_endpoint = "https://api.tequila.kiwi.com/v2/search"

tomorrow_row = dt.datetime.today() + relativedelta(days=1)
tomorrow = tomorrow_row.strftime("%d/%m/%Y")
six_month_later_row = tomorrow_row + relativedelta(months=6)
six_month_later = six_month_later_row.strftime("%d/%m/%Y")


def register_user():
    print("Welcome to Flight Club!")
    print("We find the best flight deals and email you.")
    user_name = input("What is your first name? \n")
    user_last_name = input("What is your last name? \n")
    user_email = input("What is your email? \n")

    user_params = {
        "user": {
            "firstName": user_name,
            "lastName": user_last_name,
            "email": user_email
        }
    }
    register = requests.post(url=users_endpoint, json=user_params)
    register.raise_for_status()


def update_iata():
    response = requests.get(url=destination_cities_endpoint)
    sheety_data = response.json()
    id = 2

    for row in sheety_data["flights"]:
        city_name = row["city"]

        iata_search_params = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "airport"
        }
        iata_search_response = requests.get(url=iata_search_endpoint, params=iata_search_params, headers=TEQUILA_HEADERS)
        iata_data = iata_search_response.json()
        iata_code = iata_data["locations"][0]["city"]["code"]

        data = {
            "flights": {
                "iataCode": iata_code,
            }
        }
        response = requests.put(url=f"{destination_cities_endpoint}/{id}", json=data)
        response.raise_for_status()
        id += 1


def get_cities_data():
    response = requests.get(url=destination_cities_endpoint)
    return response.json()


def get_users_data():
    response = requests.get(url=users_endpoint)
    return response.json()


def get_flight_data(destination_iata):

    search_params = {
        "fly_from": "TYO",
        "fly_to": destination_iata,
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 16,
        "max_stopovers": 1,
        "stopover_to": "4:00",
        "date_from": tomorrow,
        "date_to": six_month_later,
        "flight_type": "round",
        "curr": "JPY",
        "limit": 1
    }

    search_response = requests.get(url=flight_search_endpoint, headers=TEQUILA_HEADERS, params=search_params)
    search_response.raise_for_status()
    return search_response.json()["data"][0]
