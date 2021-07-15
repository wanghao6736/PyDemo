from sympy import symbols, limit, integrate

x = symbols('x')


def trapezium(a, b, m, func):  # 函数func在(a,b)上取步长h以梯形公式进行积分近似
    n = 2 ** m
    h = (b - a) / n
    return h / 2 * (limit(func, x, a)
                    + 2 * sum([func.evalf(subs={x: a + i * h}) for i in range(1, n)])
                    + func.evalf(subs={x: b}))


def romberg(a, b, m, start, func):  # 函数func在(a,b)上以Romberg公式近似, 计算到R2^(m-3)
    t = [trapezium(a, b, i, func) for i in range(start, m + 1)]
    s = [4 / 3 * t[i + 1] - 1 / 3 * t[i] for i in range(len(t) - 1)]
    c = [16 / 15 * s[i + 1] - 1 / 15 * s[i] for i in range(len(s) - 1)]
    r = [64 / 63 * c[i + 1] - 1 / 63 * c[i] for i in range(len(c) - 1)]
    return r     # [R2^(m-4), R2^(m-3)]


def main():
    f = 1 / (1 + 100 * x ** 2)      # 指定函数
    a, b, m = -1, 1, 4      # 指定区间端点并设置初始分段数为2^3, 对应于R1
    er = 0.5e-7     # 指定误差
    while True:  # 计算近似值
        r = romberg(a, b, m, m - 4, f)   # 以Romberg公式近似
        rn, r2n = r[0], r[1]
        e2n = abs(r2n - rn) / 255   # 计算误差
        if e2n <= er:
            print("该积分具有7位有效数的近似值为 => {2:}, 分段数为 => {0:}, "
                  "误差为 => {1:}, 满足题目要求!".format(2**m, e2n, r2n.evalf(n=7)))
            break
        else:
            m = m + 1  # 误差不满足要求，继续增加节点


main()
