# Hilbert 矩阵的条件数
import numpy as np
import matplotlib.pyplot as plt


def get_hilbert(n):  # 生成n阶Hilbert矩阵
    return 1. / (np.arange(1, n + 1) + np.arange(0, n)[:, np.newaxis])


def get_norm_inf(matrix):  # 计算矩阵的无穷范数
    s, matrix = 0.0, matrix.T
    for tpl in matrix:
        s = s + tpl.max()
    return s


def get_norm_inf_cond(n):  # 计算Hilbert矩阵无穷范数的条件数
    hilbert = get_hilbert(n)
    hilbert_inv = np.linalg.inv(hilbert)  # 求逆
    return get_norm_inf(hilbert) * get_norm_inf(hilbert_inv)


def paint_cond(n_list):  # 绘制 ln(cond(H)oo) - n 图
    cond_list = []  # 保存条件数的值
    for i in n_list.tolist():
        cond_list.append(get_norm_inf_cond(i))
    plt.plot(n_list, np.log(cond_list))
    plt.xlabel('n')
    plt.ylabel('ln(cond(H)oo)')
    plt.show()


def solve_hx(n_list):  # 求解 H · _x = b
    for n in n_list:
        x = np.ones(n)[:, np.newaxis]  # 生成 n 维 x 列向量(每行元素为1)
        h = get_hilbert(n)
        b = np.dot(h, x)  # 计算 b, b = H * x
        _x = np.linalg.solve(h, b)  # 求解 H * _x = b 得到 _x
        dx = x - _x
        dy = b - np.dot(h, _x)  # 计算 b - H * _x
        inf_dx = get_norm_inf(dx)  # 计算 x - _x 的无穷范数
        inf_dy = get_norm_inf(dy)  # 计算 b - H * _x 的无穷范数
        print("n = {2:} 时，x - _x 为：\n{0:}，\n它的无穷范数为：\t{1:.6f}".format(dx, inf_dx, n))
        print("n = {2:} 时，b - H * _x 为：\n{0:}，\n它的无穷范数为：\t{1:.6f}\n".format(dy, inf_dy, n))


def main():
    n_list = np.arange(10, 101, 10)  # 生成[10, 20, ..., 100]序列
    paint_cond(n_list)  # 绘制 ln(cond(H)oo) - n 图
    solve_hx([10, 50, 100])  # 求解 H · _x = b


main()
