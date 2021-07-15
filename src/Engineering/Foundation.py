from math import log, sin, pi
from matplotlib import pyplot as plt


def q5_5():
    sig = [156.0, 309.4, 763.8, 1512.8, 3000, 4500]
    tao = [105.6, 202.3, 474.5, 903.5, 1732.1, 2598.1]
    plt.title('5-5 Shear Envelope')
    plt.plot(sig, tao, markerfacecolor='black', marker='o')
    for s, t in zip(sig, tao):
        plt.text(s - 250, t + 50, '({}, {})'.format(s, t))
    plt.xlabel('sigma(kpa)')
    plt.ylabel('Shear Strength(kpa)')
    plt.show()


def q5_12():
    fip, fic, gama, k0, rq, q = 36, 30, 22, 0.45, 1, 10
    gama -= 9.81
    k = 1
    x, ang = [], []
    # k = 2
    for z in range(1, 11):
        sigv = gama*z
        sigh = k0*sigv
        sig3 = (sigv + 2*sigh)/3
        dr = 0.6 + 0.015*z
        while True:
            sigm = sig3/(1 - sin(fip/180 * pi))
            # sigm = sig3/(1 - sin(fip/180 * pi))*(3 - sin(fip/180 * pi))/3
            ir = dr * (q - log(sigm)) - rq
            fip_new = fic + (5 - 2 * (k - 1)) * ir
            # fip_new = fic + (5 - 2 * (k - 1)) * ir
            if abs(fip_new - fip) < 1e-1:
                x.append(z)
                ang.append(fip)
                fip = 36
                break
            else:
                fip = fip_new
    # plt.title('5-14 Triaxial')
    plt.title('5-14 Plane strain')
    plt.plot(x, ang)
    plt.xlabel('Z(m)')
    plt.ylabel('Peak friction angle')
    plt.show()


def q5_13():
    emax, emin, cg, eg, ng = 0.8, 0.48, 650, 2.17, 0.45
    gama, k0 = 22, 0.45
    # gama -= 9.81
    x, g = [], []
    for z in range(1, 11):
        sigv = gama*z
        sigh = k0*sigv
        sig3 = (sigv + 2*sigh)/3
        dr = 0.6 + 0.015*z
        e = emax - dr*(emax - emin)
        g0 = cg*(eg - e)*(eg - e)/(1 + e)*pow(sig3/100, ng)*100
        x.append(z)
        g.append(g0)
    plt.title('5-13')
    plt.plot(x, g)
    plt.xlabel('Z(m)')
    plt.ylabel('G0(Kpa)')
    plt.show()


q5_5()
