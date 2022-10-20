from datetime import datetime
import requests

from config import CONFIG
from pixela_api_types import (
    GRAPH_COLOR,
    GRAPH_TYPE,
    CreateGraphPayload,
    CreateUserPayload,
    CreateGraphPixelPayload,
    StandardApiResponse,
)

BASE_URL = "https://pixe.la/v1/users"


class PixelaAPI:
    username: str
    api_token: str

    def __init__(self) -> None:
        self.username = CONFIG["pixela_api"]["username"]
        self.api_token = CONFIG["pixela_api"]["token"]

    def create_user(self) -> bool:
        """
        Creates a user account at Pixela.

        Requires Pixela config options. See config.json.template.
        """

        url = BASE_URL

        payload: CreateUserPayload = {
            "token": self.api_token,
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }

        response = requests.post(url=url, json=payload)
        response.raise_for_status()
        data: StandardApiResponse = response.json()

        return data["isSuccess"]

    def post(
        self,
        url: str,
        payload: CreateGraphPayload | CreateGraphPixelPayload,
    ) -> StandardApiResponse:

        headers = {"X-USER-TOKEN": self.api_token}

        response = requests.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        data: StandardApiResponse = response.json()

        return data

    def create_graph(
        self,
        id: str,
        name: str,
        unit: str,
        type: GRAPH_TYPE,
        color: GRAPH_COLOR,
    ) -> bool:
        """
        Creates a new Pixela graph.

        Requires Pixela config options and a valid Pixela User Account. See
        config.json.template.
        """

        url = f"{BASE_URL}/{self.username}/graphs"
        payload: CreateGraphPayload = {
            "id": id,
            "name": name,
            "unit": unit,
            "type": type,
            "color": color,
        }

        data = self.post(url=url, payload=payload)

        return data["isSuccess"]

    def delete_graph(self, id: str) -> bool:
        url = f"{BASE_URL}/{self.username}/graphs/{id}"

        headers = {"X-USER-TOKEN": self.api_token}
        response = requests.delete(
            url=url,
            headers=headers,
        )
        response.raise_for_status()
        data: StandardApiResponse = response.json()

        return data["isSuccess"]

    def create_pixel(self, id: str, qty: int | float) -> bool:
        """
        Creates a new Pixela graph pixel.

        Requires Pixela config options and a valid Pixela User Account. See
        config.json.template.
        """

        url = f"{BASE_URL}/{self.username}/graphs/{id}"
        payload: CreateGraphPixelPayload = {
            "date": datetime.now().strftime("%Y%m%d"),
            "quantity": str(qty),
        }

        data = self.post(url=url, payload=payload)

        return data["isSuccess"]
