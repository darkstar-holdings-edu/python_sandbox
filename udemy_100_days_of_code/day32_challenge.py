import datetime as dt
import random
import smtplib

from config import CONFIG


def get_random_quote() -> str:
    with open(file="udemy_100_days_of_code/day32_data.txt") as file:
        lines = file.read().splitlines()

    return random.choice(lines)


def send_mail(quote: str) -> None:
    with smtplib.SMTP(CONFIG["smtp_host"]) as connection:
        connection.starttls()
        connection.login(user=CONFIG["smtp_username"], password=CONFIG["smtp_password"])
        connection.sendmail(
            from_addr=CONFIG["email"]["from_address"],
            to_addrs=CONFIG["email"]["to_addresses"],
            msg=f"Subject:Be Inspired\n\n{quote}",
        )


def main() -> None:
    now = dt.datetime.now()
    if now.weekday() == 3:
        quote = get_random_quote()
        send_mail(quote=quote)


if __name__ == "__main__":
    main()
