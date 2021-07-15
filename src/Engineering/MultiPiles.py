# multiple piles calculation
import math


var_dict = {}   # 保存计算所得数据
para_dict = {   # 计算所需基本参数
    'P': 21889.0,   # 桩顶所受轴向压力
    'H': 25886.0,   # 桩顶所受水平剪力
    'M': 29372.0,   # 桩顶所受弯矩
    'b': 1,         # 桩横截面的宽度
    'd': 4,         # 桩横截面的长度
    'h': 20,        # 桩的埋入深度
    'kf': 1.0,      # 桩的截面系数，矩形截面取 1.0
    'L1': 4.0,      # 平行于水平力方向的桩间净距
    'b2': 0.45,     # 平行于水平力方向的桩数为 4 根，b2 取 0.45
    'nx': 4,        # 平行水平力方向每排桩的数量
    'ny': 3,        # 垂直水平力方向每排桩的数量
    'l0': 0.0,      # 承台离地面的高度
    'ksi': 1.0,     # 对端承桩，取 1.0
    'ec': 2.8e7,    # 混凝土抗压弹性模量，混凝土等级为 C25，Kpa
    'm': 120000,     # 弹性地基系数
    'c0': 1e7,    # 岩石地基抗力系数，frk >= 25 Mpa
    'ki': 3,        # 垂直水平力方向第 i 排桩根数
    'x': [-7.5, -2.5, 2.5, 7.5],    # 由坐标原点 O 至各桩轴线的距离
    'area': 4.0,    # 桩的平均截面积
    'area0': 4.0    # 土的受压面积
}


def fmt_num(num):   # 格式化小数
    num = '%.4g' % num
    return eval(num)


def get_b1(d):  # 计算宽度
    kf, l1, b2, ny = para_dict.get('kf'), para_dict.get('L1'), para_dict.get('b2'), para_dict.get('ny')

    h1 = 3 * (1 + d)    # 桩的计算深度
    k = b2 + (1 - b2) * l1 / (0.6 * h1)    # L1 < 0.6 * h1
    b1 = k * kf * (1 + d)    # d > 1.0 m
    b1 = round(b1 * ny, 2)    # 垂直水平力方向有 ny 根桩，计算宽度取 ny * b1，且 ny * b1 <= B + 1 = 19 m
    var_dict.setdefault('b1', b1)
    return b1


def run_core(alpha, ei, ec):
    # 无量纲系数，对应 h_prime = alpha * h = 4
    a1, b1, c1, d1 = -5.85333, -5.94097, -0.92677, 4.54780
    a2, b2, c2, d2 = -6.53316, -12.15810, -10.60840, -3.76647
    # a3, b3, c3, d3 = -1.61428, -11.73066, -17.91860, -15.07550
    # a4, b4, c4, d4 = 9.24368, -0.35762, -15.61050, -23.14040

    base = a2 * b1 - a1 * b2

    # --------------------------------------------单位力作用下，单排桩的变位-------------------------------------------------
    # H0 = 1:
    dlt0_hh = fmt_num(1 / (alpha ** 3 * ei) * (b2 * d1 - b1 * d2) / base)
    dlt0_mh = fmt_num(1 / (alpha ** 2 * ei) * (a2 * d1 - a1 * d2) / base)

    # M0 = 1:
    dlt0_hm = dlt0_mh
    # dlt0_hm = 1 / (a ** 2 * ei) * (b2 * c1 - b1 * c2) / base
    dlt0_mm = fmt_num(1 / (alpha * ei) * (a2 * c1 - a1 * c2) / base)

    var_dict.setdefault('dlt0_hh', dlt0_hh)
    var_dict.setdefault('dlt0_mh', dlt0_mh)
    var_dict.setdefault('dlt0_hm', dlt0_hm)
    var_dict.setdefault('dlt0_mm', dlt0_mm)

    # --------------------------------------------单位力作用下，多排桩的变位-------------------------------------------------
    l0 = para_dict.get('l0')
    # H0 = 1:
    dlt_hh = fmt_num(l0 ** 3 / (3 * ei) + dlt0_mm * l0 ** 2 + 2 * l0 * dlt0_mh + dlt0_hh)
    dlt_mh = fmt_num(l0 ** 2 / (2 * ei) + l0 * dlt0_mm + dlt0_mh)

    # M0 = 1:
    dlt_hm = dlt_mh
    dlt_mm = fmt_num(l0 / ei + dlt0_mm)

    var_dict.setdefault('dlt_hh', dlt_hh)
    var_dict.setdefault('dlt_mh', dlt_mh)
    var_dict.setdefault('dlt_hm', dlt_hm)
    var_dict.setdefault('dlt_mm', dlt_mm)

    # ------------------------------------------任一桩顶发生单位变位时，桩顶产生的作用效应--------------------------------------
    ksi, area, area0 = para_dict.get('ksi'), para_dict.get('area'), para_dict.get('area0')
    c0, h = para_dict.get('c0'), para_dict.get('h')

    base = dlt_hh * dlt_mm - dlt_mh ** 2

    # 沿轴线单位位移时桩顶产生的轴向力
    rou_pp = round(1 / ((l0 + ksi * h) / (0.8 * ec * area) + 1 / (c0 * area0)), 1)
    # rou_pp = 1 / ((l0 + ksi * h) / (ec * area) + 1 / (c0 * area0))

    # 垂直桩轴线方向单位位移时桩顶产生的水平力
    rou_hh = round(dlt_mm / base, 1)

    # 垂直桩轴线方向单位位移时桩顶产生的弯矩
    rou_mh = round(dlt_mh / base, 1)

    # 桩顶单位转角时桩顶产生的水平力
    rou_hm = rou_mh

    # 桩顶单位转角时桩顶产生的弯矩
    rou_mm = round(dlt_hh / base, 1)

    var_dict.setdefault('rou_pp', rou_pp)
    var_dict.setdefault('rou_hh', rou_hh)
    var_dict.setdefault('rou_mh', rou_mh)
    var_dict.setdefault('rou_hm', rou_hm)
    var_dict.setdefault('rou_mm', rou_mm)

    # --------------------------------------承台发生单位变位时，所有桩顶对承台作用“反力”之和-------------------------------------
    nx, ny, ki, x = para_dict.get('nx'), para_dict.get('ny'), para_dict.get('ki'), para_dict.get('x')
    n = nx * ny

    # 承台产生竖向单位位移时，桩顶竖向反力之和
    gma_cc = round(n * rou_pp, 1)

    # 承台产生水平向单位位移时，桩顶水平反力之和
    gma_aa = round(n * rou_hh, 1)

    # 承台绕原点O产生单位转角时，桩顶水平反力之和或水平方向产生单位位移时，桩柱顶反弯矩之和
    gma_ab = round(-n * rou_hm, 1)
    # gma_ba = -n * rou_mh

    # 承台发生单位转角时，桩顶反弯矩之和
    gma_bb = round(n * rou_mm + rou_pp * ki * sum(i ** 2 for i in x), 1)

    var_dict.setdefault('gma_cc', gma_cc)
    var_dict.setdefault('gma_aa', gma_aa)
    var_dict.setdefault('gma_ab', gma_ab)
    var_dict.setdefault('gma_bb', gma_bb)

    # -----------------------------------------------------承台变位------------------------------------------------------
    P, H, M = para_dict.get('P'), para_dict.get('H'), para_dict.get('M')
    # 竖直位移
    c = fmt_num(P / gma_cc)
    # 水平位移
    a = fmt_num((gma_bb * H - gma_ab * M) / (gma_aa * gma_bb - gma_ab ** 2))
    # 转角
    b = fmt_num((gma_aa * M - gma_ab * H) / (gma_aa * gma_bb - gma_ab ** 2))

    var_dict.setdefault('c', c)
    var_dict.setdefault('a', a)
    var_dict.setdefault('b', b)

    # ---------------------------------------------------桩顶作用效应-----------------------------------------------------
    # 任一桩顶轴向力
    Ni = []
    for i in x:
        Ni.append(round((c + b * i) * rou_pp, 1))
    # 任一桩顶剪力
    Qi = round(a * rou_hh - b * rou_hm, 1)
    # 任一桩顶弯矩
    Mi = round(b * rou_mm - a * rou_mh, 1)

    var_dict.setdefault('Ni', Ni)
    var_dict.setdefault('Qi', Qi)
    var_dict.setdefault('Mi', Mi)

    # -------------------------------------------------------校核--------------------------------------------------------
    zl = round(ny * sum(Ni), 1)
    jl = round(n * Qi, 1)
    wj = round(sum(ni * xi for ni, xi in zip(Ni, x)) * ny + n * Mi, 1)

    var_dict.setdefault('zl', zl)
    var_dict.setdefault('jl', jl)
    var_dict.setdefault('wj', wj)

    # -------------------------------------------地面或局部冲刷线处桩顶截面上的作用“力”----------------------------------------
    # 水平力
    # 弯矩


def main():
    ec, b, d, m = para_dict.get('ec'), para_dict.get('b'), para_dict.get('d'), para_dict.get('m')

    i = b * d ** 3 / 12
    ei = 0.8 * ec * i
    b1 = get_b1(d)

    alpha = math.pow(m * b1 / ei, 1 / 5)
    alpha = fmt_num(alpha)
    var_dict.setdefault('alpha', alpha)

    run_core(alpha, ei, ec)

    for it in var_dict.keys():
        print(it + " : " + str(var_dict.get(it)))


main()
