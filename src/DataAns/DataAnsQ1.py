# 对数的近似计算
from math import log10
from sympy import log, symbols


def effect_num(r_num):  # 计算有效位数
    accurate = log(2).evalf(n=6)  # 准确值
    pow_num = int(log10(abs(accurate - r_num)))  # 获取误差的数量级
    if abs(accurate - r_num) < 0.5 * pow(10, pow_num):
        return "有效位数共：" + str(-pow_num) + "位，最大误差为：" + str(abs(accurate - r_num))
    return "有效位数共：" + str(-pow_num - 1) + "位，最大误差为：" + str(abs(accurate - r_num))


def main():
    x = symbols('x')
    y1 = log(1 + x)
    y2 = log(1 / (1 + x))
    y3 = log((1 + x) / (1 - x))

    # 计算 y1 在 x=0 处的泰勒展开式（移除余项）的前十项之和，取初值为 x0=1
    s1 = y1.series(x, 0, 11).removeO().evalf(subs={x: 1}, n=6)
    s2 = y2.series(x, 0, 11).removeO().evalf(subs={x: -0.5}, n=6)
    s3 = y3.series(x, 0, 11).removeO().evalf(subs={x: 1 / 3}, n=6)
    print("以 y1 = {0:} 近似时，".format(y1) + effect_num(s1))
    print("以 y2 = {0:} 近似时，".format(y2) + effect_num(s2))
    print("以 y3 = {0:} 近似时，".format(y3) + effect_num(s3))


main()
