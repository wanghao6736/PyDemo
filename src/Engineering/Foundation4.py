import math


def design(cfg, clm):
    dl, ll = cfg['clm']['dl'], cfg['clm']['ll']  # dead load, live load
    b, l, depth = cfg['b'], cfg['l'], cfg['depth']  # B, L, footing embedment
    g1, k0, phic = cfg['sand']['g'], cfg['k0'], cfg['phic']  # soil properties

    fdl, fll = 1.2, 1.6  # dead load, live load factors, table 2-3 p31
    dload = fdl * dl + fll * ll  # design load
    clm['dload'] = dload

    """ get Dr """
    n60 = cfg['sand']['n60']
    A, B, C = 36, 27, 1  # example 11-3 p486
    rdepth = depth + 0.5 * b  # representative density is at this depth
    sigv = (g1 - 9.81) * rdepth
    dr = math.sqrt(n60 / (A + B * C * sigv / 100))  # 7-6 p292
    clm['dr'] = dr

    """-------------- compute settlement --------------"""
    lr = 1.0  # reference length, p372
    zf0 = pow(b / lr, 0.79) * lr  # depth of influence 9-32, p373

    """ blow count correction """
    n60 = [30, 25, 35, 30]
    avgn = sum(n60[:int(zf0)]) / int(zf0) if int(zf0) > 0 else n60[0]  # average blow counts within zf0
    print("\nAverage N60 is {:.2f}, zf0 is {:.4f}m".format(avgn, zf0))

    """ get modification factors """
    fs = (1.25 * l / (l + 0.25 * b)) ** 2  # shape factor, square footing = 1, 9-33, p374
    fl = 1  # layer factor, sand layer is deep enough, 9-34
    ft = 1  # time factor, ignore the settlement increasing with time
    ic = 1.71 / pow(avgn, 1.4)  # 9-31

    """ get settlement for sand layer """
    qb = dload / (b * l) + sigv
    wss = 0.1 * fs * fl * ft * ic * (qb - 2 / 3 * sigv) * pow(b / lr, 0.7) * lr / 100  # 9-30
    print("\nfs = {:.2f}, fl = {:.2f}, ft = {:.2f}, ic = {:.2f}, w = {:.2f}m".format(fs, fl, ft, ic, wss))
    clm['wss'] = wss

    """ get settlement for clay layer """
    """ load spreading """
    qb0 = dload / (b + 3) / (l + 3)

    h1, h2, g2 = cfg['sand']['h'], cfg['clay']['h'], cfg['clay']['g']
    print("\nD/B = {:.2f}, L/B = {:.2f}, H/B = {:.2f}".format(depth / b, l / b, h2 / b))
    i0, i1 = eval(input("Refer to Fig.9-12 p387, input I0, I1 ..."))  # 0.87,0.69 // 0.88,0.68 // 0.89,0.66

    """ immediate settlement """
    pi = cfg['clay']['ll'] - cfg['clay']['pl']
    # print("\nPI = {:.2f}, OCR = {:.2f}".format(pi, cfg['clay']['ocr']))
    # k = eval(input("Refer to Fig.9-13 p388, input K ..."))  # 800
    k = 800

    zr = depth + 3 + h2 / 3
    su = (0.11 + 0.0037 * pi) * ((g1 - 9.81) * h1 + (g2 - 9.81) * (zr - h1))

    eu = k * su
    wci = i0 * i1 * (qb0 - sigv) * b / eu
    print("\nk = {:.2f}, zr = {:.2f}, su = {:.2f}, wci = {:.2f}".format(k, zr, su, wci))
    clm['wci'] = wci

    """ consolidation settlement """
    alpha = eval(input("\nH/B = {:.2f}, refer to Table 9-4 p390, input alpha ...".format(h2/b)))  # 0.16//0.177//0.198
    a = 2/3  # assumed value, p392
    miu = a + alpha * (1 - a)  # 9-53

    dlt = dload / (b + h2/2 + 3) / (l + h2 / 2 + 3)  # just 1 layer, no sublayer
    sigv0 = (g1 - 9.81) * h1 + (g2 - 9.81) * h2/2

    e0, cc = cfg['clay']['e'], cfg['clay']['cc']
    wcc = miu * cc * h2 / (1 + e0) * math.log10((sigv0 + dlt)/sigv0)
    print("\nu = {:.2f}, wcc = {:.2f}".format(miu, wcc))
    clm['wcc'] = wcc

    """ total settlement """
    clm['w'] = wss + wci + wcc
    print("\nTotal settlement is {:.2f}".format(clm['w']))

    """-------------- bearing capacity check --------------"""
    bearing_check(cfg, clm)
    print(clm)


def bearing_check(cfg, clm):
    b, l, depth = cfg['b'], cfg['l'], cfg['depth']  # B, L, footing embedment
    g1, k0, phic = cfg['sand']['g'], cfg['k0'], cfg['phic']  # soil properties
    dload, dr = clm['dload'], clm['dr']

    """ get phip """
    q, rq = 10, 1
    sigmp = 2000 * math.pow(g1 * b / 100, 0.7) * (1 - 0.32 * b / l)  # 10-34
    aphi = (l / b + 8) / 3  # 10-37, 1 <= l/b < 7, p443
    ir = dr * (q - math.log(sigmp)) - rq  # 5-8
    phip = phic + aphi * ir  # p445 example 10-13
    phipr = phip * math.pi / 180

    """ get modification factors """
    q0 = g1 * depth  # uint load at the foundation level
    nq = (1 + math.sin(phipr)) / (1 - math.sin(phipr)) * math.exp(math.pi * math.tan(phipr))  # 10-6
    ng = (nq - 1) * math.tan(1.32 * phipr)  # 10-13
    sq = 1 + (0.0952 * phip - 1.6) * math.pow(depth / b, 0.583 - 0.0079 * phip) * math.pow(b / l, 1 - 0.15 * depth / b)
    sg = 1 + (0.0345 * phip - 1.0611) * b / l  # table 11-8
    dq = 1 + (0.0044 * phip + 0.356) * math.pow(depth / b, -0.28)
    dg = 1
    qbl = sq * dq * q0 * nq + 0.5 * sg * dg * g1 * b * ng  # 10-34
    print("\nsq = {:.2f}, dq = {:.2f}, q0 = {:.2f}, nq = {:.2f}, sg = {:.2f}, dg = {:.2f}, g1 = {:.2f}, b = {:.2f}, "
          "ng = {:.2f}, qbl = {:.2f}".format(sq, dq, q0, nq, sg, dg, g1, b, ng, qbl))

    """ verify using  WSD & LRFD """
    rf, dfos = cfg['rf'], cfg['fos']
    rn = qbl * b * l  # limit bearing load
    r = rn * rf
    fos = rn / dload

    print("\nResistance is {:.2f}kN, design load is {:.2f}kN, safety factor is {:.2f}".format(r, dload, fos))
    clm['lrfd'] = True if r > dload else False
    clm['wsd'] = True if fos > dfos else False


def main():
    clms = {
        '1': {  # corner columns 0.6X0.6
            'dl': 450,
            'll': 530,
        },
        '2': {  # exterior columns 0.8X0.8
            'dl': 550,
            'll': 620,
        },
        '3': {  # interior columns 1.2X1.2
            'dl': 650,
            'll': 730,
        }
    }
    cfg = {
        'sand': {
            'g': 19,
            'n60': 30,  # depth = 3m, figure 11-15
            'h': 6,
        },
        'clay': {
            'll': 45,
            'pl': 22,
            'g': 18,
            'cc': 0.28,
            'ocr': 1,
            'e': 0.9,
            'h': 5,
        },
        'k0': 0.45,
        'phic': 33,
        'rf': 0.2,  # table 11-5 p492 SPT
        'fos': 2,  # safety factor, table 2-2, p29
        'depth': 3,
        'space': 6
    }
    ret = {}
    w = []
    while True:
        print("What type of column do you want to design?")
        clm = input("[1:corner columns, 2:exterior columns, 3:interior columns]")
        cfg['clm'] = clms[clm]
        ret[clm] = cfg['clm']

        cfg['b'], cfg['l'] = eval(input("\nProportioning footing size [B, L]: "))
        design(cfg, ret[clm])
        if ret[clm]['wsd'] and ret[clm]['lrfd']:
            print("\nBearing capacity qualified!")
        else:
            print("\nNeed to redesign current column!")
            continue

        w.append(ret[clm]['w'])

        """-------------- settlement check --------------"""
        alpha = (max(w) - min(w)) / cfg['space']

        print("\nSettlement qualified! Alpha is {:.4f}".format(alpha)) if alpha < 1 / 300 else w.clear() and print(
            "\nNeed to redesign all columns!")

        flag = input("\nBreak now? [y/n]")
        if flag == 'y':
            break


main()
