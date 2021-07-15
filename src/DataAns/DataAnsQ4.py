# 圆的拟合
from math import sin, cos, pi, sqrt
import numpy as np


def save_x_y(_f, _x, _y, delta):  # 以列表保存已知的坐标点
    for i in range(1, 101):
        _f.append(1)
        _x.append(1 + (-1) ** i * delta + 3 * cos(i / 50 * pi))
        _y.append(10 + 3 * sin((i / 50 + delta) * pi))


def get_para(f0, f1, f2):  # 计算 a b c 的值
    matrix_a = np.array([f0, f1, f2]).T  # 将列向量 fi0 fi1 fi2 构造成矩阵
    b_t = []
    for i in range(len(f1)):
        b_t.append(f1.pop() ** 2 + f2.pop() ** 2)  # 计算列向量 b 的转置
    matrix_formal = np.dot(matrix_a.T, matrix_a)  # 计算正规方程组的系数矩阵
    b_t.reverse()   # b_t 是逆序存储的，需要将顺序还原
    b = np.array([b_t]).T  # 计算列向量 b
    matrix_b = np.dot(matrix_a.T, b)  # 计算正规方程组的右端列向量 (b, fi)
    return np.linalg.solve(matrix_formal, matrix_b)  # 求解正规方程组，得到 a b c


def get_cir_para(para):
    para = para.tolist()  # 将数组转换为 list
    c = para.pop().pop()  # 得到 a b c 的具体值
    b = para.pop().pop()
    a = para.pop().pop()
    x, y = b / 2, c / 2  # 解得 x y r
    r = sqrt(a + x ** 2 + y ** 2)
    return "(a, b, c) = ({0:}, {1:}, {2:}), \n(x*, y*) = ({3:}, {4:}), \nr = {5:}".format(a, b, c, x, y, r)


def main():
    delta = 0.05
    f, x, y = [], [], []
    save_x_y(f, x, y, delta)    # 根据已知条件求得坐标值
    para = get_para(f, x, y)    # 求解 a, b, c
    print(get_cir_para(para))   # 求解 x, y, r 并输出计算结果


main()
