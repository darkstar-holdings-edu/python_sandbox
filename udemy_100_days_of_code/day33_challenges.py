from typing import Literal, TypedDict
import requests
import datetime as dt


class ISS_POSITION_RESPONSE(TypedDict):
    message: Literal["success"]
    timestamp: float
    iss_position: dict[Literal["longitude", "latitude"], float]


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


def main() -> None:
    print(iss_position())


if __name__ == "__main__":
    main()
