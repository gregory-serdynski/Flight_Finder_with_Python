from twilio.rest import Client
import os
from dotenv import load_dotenv
import data_manager as dm
import smtplib

load_dotenv("env")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


EMAIL = "メール"
PASSWORD = os.getenv("EMAIL_PASSWORD")
ORIGIN_CITY = "Tokyo"


class NotificationManager:
    def __init__(self, dept_city, dept_iata, dest_city, dest_iata, flight_price, dept_date, return_date):
        self.dept_city = dept_city
        self.dept_iata = dept_iata
        self.dest_city = dest_city
        self.dest_iata = dest_iata
        self.price = flight_price
        self.dept_date = dept_date
        self.return_date = return_date

        # self.send_message()
        self.send_email()

    def send_message(self):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Low price alert! '
                 f'Only ￥{self.price} to fly from {ORIGIN_CITY}-{self.dept_iata} '
                 f'to {self.dest_city}-{self.dest_iata}, from {self.dept_date} to {self.return_date}.',
            from_='whatsapp:+14155238886',
            to='whatsapp:<個人番号>'
        )
        # print(message.status)

    def send_email(self):
        users = dm.get_users_data()
        for user in users["users"]:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=EMAIL,
                                    to_addrs=user["email"],
                                    msg=f"Subject:CHEAP FLIGHT SPOTTED!\n\nOnly {self.price}JPY to fly "
                                        f"from {ORIGIN_CITY}-{self.dept_iata} to {self.dest_city}-{self.dest_iata}, "
                                        f"from {self.dept_date} to {self.return_date}.")

    def create_link(self):
        return f"https://www.google.com/travel/flights?q=Flights%20to%20{self.dest_iata}%20from%20{self.dept_iata}%20on%20{self.dept_date}%20through%20{self.return_date}"

