import datetime as dt
import random
import smtplib


def get_random_quote() -> str:
    with open(file="udemy_100_days_of_code/day32_data.txt") as file:
        lines = file.read().splitlines()

    return random.choice(lines)


def send_mail(quote: str) -> None:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user="hashref@gmail.com", password="")
        connection.sendmail(
            to_addrs="hashref@gmail.com",
            from_addr="hashref@gmail.com",
            msg=f"Subject:Be Inspired\n\n{quote}",
        )


def main() -> None:
    now = dt.datetime.now()
    if now.weekday() == 3:
        quote = get_random_quote()
        send_mail(quote=quote)


if __name__ == "__main__":
    main()
