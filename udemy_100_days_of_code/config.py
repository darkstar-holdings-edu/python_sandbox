from typing import Sequence, TypedDict

from config42 import ConfigManager
from config42.handlers import FileHandler


class ConfigPixelApi(TypedDict):
    username: str
    token: str


class ConfigEmailOption(TypedDict):
    from_address: str
    to_addresses: str | Sequence[str]


class ConfigData(TypedDict):
    smtp_host: str
    smtp_username: str
    smtp_password: str
    email: ConfigEmailOption
    pixela_api: ConfigPixelApi


CONFIG: ConfigData = ConfigManager(
    handler=FileHandler, path="udemy_100_days_of_code/config.json"
).as_dict()
