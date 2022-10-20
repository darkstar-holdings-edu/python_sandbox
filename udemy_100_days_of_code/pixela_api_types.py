from typing import Literal, TypedDict

GRAPH_COLOR = Literal["shibafu", "momiji", "sora", "ichou", "ajisai", "kuro"]
GRAPH_TYPE = Literal["int", "float"]
YES_OR_NO = Literal["yes", "no"]


class CreateGraphPayload(TypedDict):
    id: str
    name: str
    unit: str
    type: GRAPH_TYPE
    color: GRAPH_COLOR


class CreateGraphPixelPayload(TypedDict):
    date: str
    quantity: str


class CreateUserPayload(TypedDict):
    token: str
    username: str
    agreeTermsOfService: YES_OR_NO
    notMinor: YES_OR_NO


class StandardApiResponse(TypedDict):
    message: str
    isSuccess: bool
