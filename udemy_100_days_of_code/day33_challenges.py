import datetime as dt
from tkinter import Button, Canvas, PhotoImage, Tk
from typing import Literal, TypedDict

import requests
from menutools import Menu

ASSETS_DIRECTORY = "udemy_100_days_of_code/day33_assets"


class ISS_POSITION_RESPONSE(TypedDict):
    message: Literal["success"]
    timestamp: float
    iss_position: dict[Literal["longitude", "latitude"], float]


class KANYE_API_RESPONSE(TypedDict):
    quote: str


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


def main() -> None:
    def print_iss_position() -> None:
        print(iss_position())

    menu = Menu("100 Days of Code Challenges")
    menu.add(
        (
            "Day 33",
            [
                ("ISS Position", print_iss_position),
                ("Kanye Says", kanye_says),
                ("Exit", menu.exit),
            ],
        )
    )
    menu.execute()


if __name__ == "__main__":
    main()
