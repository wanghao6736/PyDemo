# 数值积分
from sympy import sqrt, ln, symbols, limit, exp, solve, integrate, oo
import matplotlib.pyplot as plt

x = symbols('x')


def trapezium(a, b, h, func):  # 函数func在(a,b)上取步长h以梯形公式进行积分近似
    n = int((b - a) / h)
    return h / 2 * (limit(func, x, a)
                    + 2 * sum([func.evalf(subs={x: a + i * h}) for i in range(1, n)])
                    + func.evalf(subs={x: b}))


def simpson(a, b, h, func):  # 函数func在(a,b)上取步长h以Simpson公式进行积分近似
    n = int((b - a) / h)
    return h / 6 * (limit(func, x, 0)
                    + 2 * sum([func.evalf(subs={x: a + i * h}) for i in range(1, n)])
                    + 4 * sum([func.evalf(subs={x: a + (i + 0.5) * h}) for i in range(n)])
                    + func.evalf(subs={x: b}))


def romberg(a, b, m, start, func):  # 函数func在(a,b)上的Romberg公式积分近似，结果为R2^(m-1)
    t = [trapezium(a, b, 2 ** (-i), func) for i in range(start, m + 3)]
    s = [4 / 3 * t[i + 1] - 1 / 3 * t[i] for i in range(len(t) - 1)]
    c = [16 / 15 * s[i + 1] - 1 / 15 * s[i] for i in range(len(s) - 1)]
    r = [64 / 63 * c[i + 1] - 1 / 63 * c[i] for i in range(len(c) - 1)]
    return r    # 根据start返回[R2^start,..., R2^(m-1)], start >= 0


def q1():  # 求解第一问
    a, b = 0, 1  # 指定区间端点
    f = sqrt(x) * ln(x)  # 指定函数方程
    tra, sim, rom = [], [], []  # 保存各种近似方法的计算结果
    xi = []
    for m in range(1, 13):  # 计算不同m值不同近似方法的积分近似值
        h = 2 ** (-m)
        t = trapezium(a, b, h, f)
        s = simpson(a, b, h, f)
        r = romberg(a, b, m, m - 1, f)[-1]
        tra.append(t)
        sim.append(s)
        rom.append(r)
        xi.append(m)
        print(m)
    plt.xlabel('m')  # 绘制图像
    plt.ylabel('Y')
    plt.plot(xi, tra, label='trapezium')
    plt.plot(xi, sim, label='simpson')
    plt.plot(xi, rom, label='romberg')
    plt.axhline(y=-4 / 9, label='y=-4/9', color='red', ls=':')
    plt.legend()
    plt.show()


def q23():  # 求解第二、三问
    er = 0.5e-8  # 指定误差限
    f_prime = x * exp(-3/2 * x)  # 指定函数方程
    f = integrate(f_prime, x)  # 求得不定积分（原函数）
    foo = limit(f, x, oo)  # 求得 f(+oo)
    a = solve(foo - f - 2.5e-9, x)  # f(+oo) - f(a) = 0.5er
    for i in a:     # 找到正数 a
        if i > 0:
            a = i
            break
    print("a = {}".format(a))
    a0, b0, m = 0, a, 2
    while True:     # 求K的近似值
        r = romberg(a0, b0, m, m - 2, -f_prime)
        rn, r2n = r[0], r[1]
        if abs(r2n - rn) / 255 <= er:
            print("|(-4/9)-R2n| = {}".format(abs(-4/9 - r2n)))
            break
        else:
            m = m + 1   # 误差不满足要求，继续增加节点
    print("所用节点数为：%d" % (2**(m+2)+1))


# q1()
q23()
