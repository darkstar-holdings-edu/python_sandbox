def climbStairs(n: int) -> int:
    if n < 3:
        return n

    m: list[int] = [-1] * (n)
    m[0] = 1
    m[1] = 2

    for i in range(2, n):
        m[i] = m[i - 2] + m[i - 1]

    return m[n - 1]


print(climbStairs(5))
