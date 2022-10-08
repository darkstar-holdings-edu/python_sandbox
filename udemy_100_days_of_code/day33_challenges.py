import datetime as dt
import smtplib
import time
from datetime import timezone
from tkinter import Button, Canvas, PhotoImage, Tk
from typing import Literal, TypedDict
from signal import signal, SIGINT

import requests
from config42 import ConfigManager
from config42.handlers import FileHandler
from menutools import Menu

ASSETS_DIRECTORY = "udemy_100_days_of_code/day33_assets"
LATITUDE = 34.052235
LONGITUDE = -118.243683


CONFIG = ConfigManager(
    handler=FileHandler, path="udemy_100_days_of_code/config.json"
).as_dict()


class ISS_POSITION_RESPONSE(TypedDict):
    message: Literal["success"]
    timestamp: float
    iss_position: dict[Literal["longitude", "latitude"], float]


class KANYE_API_RESPONSE(TypedDict):
    quote: str


SUNRISE_SUNSET_RESULTS_KEYS = Literal[
    "sunrise",
    "sunset",
    "solar_noon",
    "day_length",
    "civil_twilight_begin",
    "civil_twilight_end",
    "nautical_twilight_begin",
    "nautical_twilight_end",
    "astronomical_twilight_begin",
    "astronomical_twilight_end",
]


class SUNRISE_SUNSET_API_RESPONSE(TypedDict):
    status: Literal["OK"]
    results: dict[SUNRISE_SUNSET_RESULTS_KEYS, str]


def get_iss_position() -> tuple[dt.datetime, float, float]:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    response_data: ISS_POSITION_RESPONSE = response.json()

    position_data = response_data["iss_position"]
    current_position = (
        dt.datetime.fromtimestamp(response_data["timestamp"]).astimezone(
            tz=timezone.utc
        ),
        float(position_data["latitude"]),
        float(position_data["longitude"]),
    )

    return current_position


def kanye_says() -> None:
    def get_quote():
        response = requests.get(url="https://api.kanye.rest")
        response.raise_for_status()
        data: KANYE_API_RESPONSE = response.json()

        canvas.itemconfig(quote_text, text=data["quote"])

    window = Tk()
    window.title("Kanye Says...")
    window.config(padx=50, pady=50)

    canvas = Canvas(width=300, height=414)
    background_img = PhotoImage(file=f"{ASSETS_DIRECTORY}/background.png")
    canvas.create_image(150, 207, image=background_img)
    quote_text = canvas.create_text(
        150,
        207,
        text='Kanye says, "Click my head"',
        width=250,
        font=("Arial", 30, "bold"),
        fill="white",
    )
    canvas.grid(row=0, column=0)

    kanye_img = PhotoImage(file=f"{ASSETS_DIRECTORY}/kanye.png")
    kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
    kanye_button.grid(row=1, column=0)

    window.mainloop()


def get_sunrise_sunset() -> tuple[dt.datetime, dt.datetime]:
    payload = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=payload)
    response.raise_for_status()

    data: SUNRISE_SUNSET_API_RESPONSE = response.json()

    sunrise = dt.datetime.fromisoformat(data["results"]["sunrise"])
    sunset = dt.datetime.fromisoformat(data["results"]["sunset"])

    return (sunrise, sunset)


def is_dark(now: dt.datetime) -> bool:
    sunrise_sunset_data = get_sunrise_sunset()
    sunrise = sunrise_sunset_data[0]
    sunset = sunrise_sunset_data[1]

    if now > sunset or now < sunrise:
        return True

    return False


def is_iss_overhead() -> bool:
    iss_position = get_iss_position()
    iss_latitude = iss_position[1]
    iss_longitude = iss_position[2]

    delta_latitude = abs(LATITUDE - iss_latitude)
    delta_longitude = abs(LONGITUDE - iss_longitude)

    if int(delta_latitude) <= 5 and int(delta_longitude) <= 5:
        return True
    else:
        print(f"Current ISS Delta: {delta_latitude} lat, {delta_longitude} lng")

    return False


def iss_tracker() -> None:
    running = True

    def handler(sig, frame) -> None:
        print("Process interrupted. Exiting!")
        main()

    signal(SIGINT, handler)

    while running:
        current_time = dt.datetime.now().astimezone(tz=timezone.utc)

        if is_dark(now=current_time):
            print("Checking if the ISS is overhead")
            if is_iss_overhead():
                send_mail(
                    subject="Look up!",
                    body="Look up! The ISS is currently overhead!",
                )

                running = False

        else:
            running = False

        time.sleep(60)


def send_mail(subject: str, body: str) -> None:
    with smtplib.SMTP(CONFIG["smtp_host"]) as connection:
        connection.starttls()
        connection.login(user=CONFIG["smtp_username"], password=CONFIG["smtp_password"])
        connection.sendmail(
            from_addr=CONFIG["email"]["from"],
            to_addrs=CONFIG["email"]["to"],
            msg=f"Subject:{subject}\n\n{body}",
        )


def main() -> None:
    def print_iss_position() -> None:
        print(get_iss_position())

    def print_sunrise_sunset() -> None:
        print(get_sunrise_sunset())

    menu = Menu("100 Days of Code Challenges")
    menu.add(
        (
            "Day 33",
            [
                ("ISS Position", print_iss_position),
                ("Kanye Says", kanye_says),
                ("Sunrise/Sunset", print_sunrise_sunset),
                ("ISS Tracker", iss_tracker),
                ("Exit", menu.exit),
            ],
        )
    )
    menu.execute()


if __name__ == "__main__":
    main()
