def add(*args: int) -> int:
    """Adds numbers together and returns the sum"""
    sum = 0
    for n in args:
        sum += n

    return sum


def calculate(n: int, **kwargs: int) -> int:
    n += kwargs["add"]
    n *= kwargs["multiply"]

    return n


def main() -> None:
    print(add(3, 5, 6))
    print(calculate(2, add=3, multiply=5))


if __name__ == "__main__":
    main()
