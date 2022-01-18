import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 53.682968
MY_LONG = -1.499100
MY_POSITION = (MY_LAT, MY_LONG)
ERROR = 5
MY_EMAIL = "***"
MY_PASSWORD = "***"

url = "http://api.open-notify.org/iss-now.json"
response = requests.get(url)
response.raise_for_status()
data = response.json()
iss_latitude = float(data['iss_position']['latitude'])
iss_longitude = float(data['iss_position']['longitude'])
iss_position = (iss_latitude, iss_longitude)


def on_pos():
    if (MY_LAT + ERROR) >= iss_latitude >= (MY_LAT - ERROR) and (MY_LONG + ERROR) >= iss_longitude >= (MY_LONG - ERROR):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    url_2 = "https://api.sunrise-sunset.org/json"
    response_2 = requests.get(url_2, params=parameters)
    response_2.raise_for_status()
    data = response_2.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split(":")[0])

    now_hour = datetime.now().hour

    if now_hour >= sunset_hour or now_hour <= sunrise_hour:
        return True


while True:
    time.sleep(60)
    if on_pos() and is_night():
        connection = smtplib.SMTP("smtp.mail.yahoo.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg="Subject: Look Up\n\nThe IIS is above you in the sky!")
