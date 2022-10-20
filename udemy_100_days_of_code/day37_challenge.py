import string
import random

from pixela_api import PixelaAPI

api = PixelaAPI()

CREATE_USER = False
GRAPH_ID = "xgxj949gd8ok16l2"


def generate_graph_id() -> str:
    id = random.choice(string.ascii_lowercase)
    id += "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(15)
    )
    return id


def main() -> None:

    if CREATE_USER:
        api.create_user()

    if not GRAPH_ID:
        graph_id = generate_graph_id()
        api.create_graph(
            id=graph_id,
            name="Graph1",
            type="int",
            unit="minutes",
            color="kuro",
        )
        print(graph_id)

    # print(api.delete_graph(id=GRAPH_ID))

    api.create_pixel(id=GRAPH_ID, qty=10)


if __name__ == "__main__":
    main()
