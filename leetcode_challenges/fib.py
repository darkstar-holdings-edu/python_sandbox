def fib(n: int) -> int:
    if n == 0:
        return 0

    m: list[int] = [-1] * (n + 1)
    m[0], m[1] = 0, 1

    for i in range(2, n + 1):
        m[i] = m[i - 2] + m[i - 1]

    return m[n]


def trifib(n: int) -> int:
    if n < 2:
        return n
    elif n == 2:
        return 1

    m: list[int] = [-1] * (n + 1)
    m[0], m[1], m[2] = 0, 1, 1

    for i in range(3, n + 1):
        m[i] = m[i - 3] + m[i - 2] + m[i - 1]

    return m[n]


print(trifib(25))
