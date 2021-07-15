# 方程求根的Newton法
from sympy import symbols, exp, diff
import numpy as np
import matplotlib.pyplot as plt


x = symbols('x')


def paint_fun(f, x_ext, y_ext):  # 绘制函数图像
    x_aix = np.arange(-x_ext, x_ext, 0.1)  # 绘制区域
    y_aix = []
    for t in x_aix:  # 计算 y 值
        y = f.evalf(subs={x: t})
        y_aix.append(y)
    plt.plot(x_aix, y_aix, label=f)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-y_ext, y_ext)
    plt.legend()  # 显示 label
    plt.grid()  # 显示 grid
    plt.show()


def solve_fun(f, x_ext, y_ext):
    print("y = {0:} 的曲线如图：".format(f))
    paint_fun(f, x_ext, y_ext)  # 绘制函数图像
    n = eval(input("请输入根的个数："))  # 根据图像输入根的个数
    intervals = []
    for i in range(n):  # 得到根的区间
        interval = input("请输入第{0:}个根的区间（形如：[1,2]）：".format(i + 1))
        intervals.append(eval(interval))
    for interval in intervals:  # 在每个区间上运用牛顿法迭代
        x0 = newton(f, interval.pop())
        print("第{0:}个根的近似值为：{1:.8f}".format(n - i, x0))
        i -= 1


def static_var(**kwargs):   # 定义装饰器，用于保存迭代次数
    def decorate(func):
        for i in kwargs:
            setattr(func, i, kwargs[i])
        return func
    return decorate


@static_var(count=0)    # 为牛顿迭代函数添加一个count属性
def newton(f, x0):      # 牛顿迭代法
    newton.count += 1   # 迭代次数加一
    x_nt = x - f / diff(f, x)  # 迭代格式
    x_k = x_nt.evalf(subs={x: x0})  # 计算 xk
    er = abs(x0 - x_k)
    if er < 0.5e-8:  # 误差小于 0.5e-8 时迭代结束，此时近似值至少含有8位有效数
        return x0.evalf(n=8)
    return newton(f, x_k)  # 迭代计算下个值


def print_er(f):    # 打印迭代初值和迭代次数的关系图
    span, h = 18, 0.1   # 定义区间广度、迭代步长
    xr = np.arange(-span, span, h)
    px, itr = [], []    # 保存迭代点和迭代次数
    for i in xr:
        px.append(i)    # 记录迭代点
        newton(f, i)    # 迭代计算
        itr.append(newton.count)    # 记录迭代次数
        newton.count = 0    # 将次数清零以进行下次迭代
    plt.plot(px, itr, label=f)
    plt.xlabel('x-step')
    plt.ylabel('iteration count')
    plt.legend()
    plt.show()


def main():
    fx = 3 * x ** 2 - exp(x)
    gx = diff(fx, x)

    solve_fun(gx, 10, 10)  # 求解g(x)
    solve_fun(fx, 10, 10)  # 求解f(x)
    print_er(fx)    # 用于分析迭代初值的选取范围
    print_er(gx)


main()
