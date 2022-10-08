import datetime as dt
from tkinter import Button, Canvas, PhotoImage, Tk
from typing import Literal, TypedDict

import requests
from menutools import Menu

ASSETS_DIRECTORY = "udemy_100_days_of_code/day33_assets"
LATITUDE = 34.052235
LONGITUDE = -118.243683


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


def iss_position() -> tuple[dt.datetime, float, float]:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    response_data: ISS_POSITION_RESPONSE = response.json()

    position_data = response_data["iss_position"]
    current_position = (
        dt.datetime.fromtimestamp(response_data["timestamp"]),
        position_data["latitude"],
        position_data["longitude"],
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


def sunrise_sunset() -> tuple[str, str]:
    payload = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=payload)
    response.raise_for_status()

    data: SUNRISE_SUNSET_API_RESPONSE = response.json()

    return (data["results"]["sunrise"], data["results"]["sunset"])


def main() -> None:
    def print_iss_position() -> None:
        print(iss_position())

    def print_sunrise_sunset() -> None:
        print(sunrise_sunset())

    menu = Menu("100 Days of Code Challenges")
    menu.add(
        (
            "Day 33",
            [
                ("ISS Position", print_iss_position),
                ("Kanye Says", kanye_says),
                ("Sunrise/Sunset", print_sunrise_sunset),
                ("Exit", menu.exit),
            ],
        )
    )
    menu.execute()


if __name__ == "__main__":
    main()
