import math
from matplotlib import pyplot as plt


class MyLayer:
    lid = 0
    top, btm, dz, zf = 0., 0., 0., 0.
    gama, dr, phi25, phi, iz = 0., 0., 0., 0., 0.
    ei, sigv, sigh, k0, qc, s = 0., 0., 0., 0.5, 0., 0.

    def __str__(self):
        return "top={}, dz={}, btm={:.2f}, qc={}, dr={:.2f}, zf={:.2f}, iz={:.2f}, s={:.5f}, ei={:.2f}," \
               " sigv={:.2f}, sigh={:.2f}, phi={:.2f}".format(self.top, self.dz, self.btm, self.qc, self.dr, self.zf,
                                                              self.iz, self.s, self.ei, self.sigv, self.sigh, self.phi
        )


def ini():
    lr, qr = [], []
    lr.append([0.55, 0.8, 0.4, 0.25])  # zf0=2m
    qr.append([3, 2, 4, 5])  # zf0=2m
    lr.append([0.55, 0.8, 0.4, 0.8, 1, 0.45])  # zf0=4m
    qr.append([3, 2, 4, 5, 13, 17])  # zf0=4m
    lr.append([0.55, 0.8, 0.4, 0.8, 1, 1, 0.8, 0.65])  # zf0=6m
    qr.append([3, 2, 4, 5, 13, 16.5, 19.5, 19])  # zf0=6m

    rad, wx, z0, wl = [1, 2, 3], [25, 37.5, 50], 0.45, 3
    phi_c, k0, rls, rds = 30, 0.5, {}, []
    i = 1
    for lri, qri in zip(lr, qr):
        tz, sig = z0, 19 * z0
        ls, ds = [], []
        for dz, qci in zip(lri, qri):
            ly = MyLayer()
            ly.top, ly.dz = tz, dz
            ly.btm, tz = ly.top + ly.dz, tz + dz

            ly.qc = qci
            ly.gama = 19 if ly.btm <= wl else 21 - 9.81
            ly.zf = ly.top + ly.dz / 2
            sig += ly.gama * ly.dz
            ly.sigv = sig - ly.gama * ly.dz / 2
            ly.sigh = k0 * ly.sigv
            ly.dr = (math.log(ly.qc * 10) - 0.4947 - 0.1041 * phi_c - 0.841 * math.log(ly.sigh / 100)) / (
                    0.0264 - 0.0002 * phi_c - 0.0047 * math.log(ly.sigh / 100)
            )
            ls.append(ly)
            ds.append(ly.dr)
        rls['r' + str(i)] = ls
        rds.append(ds)
        i += 1
    phi = cal_phi(rds)

    for r in rad[2:]:
        zf0, zfp, iz0 = 2 * r, 0.5 * r, 0.1
        q = 4865 / (math.pi * r ** 2) + 19 * z0
        # q = 450 + 24 * z0
        sig0 = 19 * z0
        sigp = sig0 + 19 * zfp
        izp = 0.5 + 0.1 * math.sqrt((q - sig0) / sigp)
        ph = phi['r' + str(r)]
        wn = ['w25', 'w37.5', 'w50']
        for w in wn[2:]:
            print("r = {}m, w = {}mm, q = {}".format(r, w, q - 24 * z0))
            s = []
            c1 = 1 - 0.5 * sig0 / (q - sig0)
            for p, ly in zip(ph[w], rls['r' + str(r)]):
                ly.phi = p
                if ly.zf < zfp:
                    ly.iz = iz0 + ly.zf / zfp * (izp - iz0)
                else:
                    ly.iz = izp * (zf0 - ly.zf) / (zf0 - zfp)
                ly.ei = p * ly.qc
                ly.s = ly.iz * ly.dz / ly.ei
                s.append(ly.s)
                print(ly)
            print("sum(s) = {:.3f}, c1 = {:.3f}".format(sum(s), c1))
            lg = c1 * (q - sig0) * sum(s)
            print("w = ", lg)


def cal_phi(dr):
    phi = [
        [
            [2.51, 1.77, 1.39, 1.11],  # r=1m
            [3.15, 2.28, 1.78, 1.38],  # r=2m
            [3.58, 2.67, 2.09, 1.74]  # r=3m
        ],  # w=25mm
        [
            [2.16, 1.5, 1.22, 1.0],  # r=1m
            [2.75, 2.03, 1.55, 1.21],  # r=2m
            [3.15, 2.4, 1.8, 1.6]  # r=3m
        ],  # w=37.5mm
        [
            [1.9, 1.4, 1.15, 0.95],  # r=1m
            [2.54, 1.93, 1.5, 1.17],  # r=2m
            [2.93, 2.28, 1.85, 1.53]  # r=3m
        ]  # w=50mm
    ]
    ret = {}
    w = ['w25', 'w37.5', 'w50']
    r = ['r1', 'r2', 'r3']
    for d in dr:
        jiao = {}
        for ph in phi:
            pi = ph[dr.index(d)]
            ji, p = [], 0.
            for di in d:
                if di < 50:
                    p = di / 50 * pi[1]
                if 50 < di < 70:
                    p = (di - 50) / 20 * (pi[2] - pi[1]) + pi[1]
                if 70 < di < 90:
                    p = (di - 70) / 20 * (pi[3] - pi[2]) + pi[2]
                if di > 90:
                    p = di / 90 * pi[3]
                ji.append(p)
            jiao.setdefault(w[phi.index(ph)], ji)
        ret.setdefault(r[dr.index(d)], jiao)
    return ret


def plot_phi(w):
    x = [2, 4, 6, 8, 10]
    dr = [
        [
            [2.65, 2.09, 1.74, 1.56, 1.44],  # dr = 30%
            [1.88, 1.5, 1.32, 1.18, 1.12],  # dr = 50%
            [1.44, 1.21, 1.09, 1.0, 0.88],  # dr = 70%
            [1.15, 1.0, 0.91, 0.79, 0.76]  # dr = 90%
        ],  # r = 1m
        [
            [3.31, 2.69, 2.39, 2.15, 2.0],  # dr = 30%
            [2.38, 2.0, 1.86, 1.65, 1.55],  # dr = 50%
            [1.85, 1.55, 1.45, 1.35, 1.25],  # dr = 70%
            [1.44, 1.19, 1.15, 1.08, 1.06]  # dr = 90%
        ],  # r = 2m
        [
            [3.74, 3.13, 2.75, 2.53, 2.43],  # dr = 30%
            [2.76, 2.4, 2.15, 2.0, 1.9],  # dr = 50%
            [2.16, 1.91, 1.79, 1.65, 1.52],  # dr = 70%
            [1.78, 1.61, 1.46, 1.4, 1.37]  # dr = 90%
        ]  # r = 3m
    ]
    for dri in dr:
        drn = 30
        for d in dri:
            lab = str(drn) + '%'
            drn += 20
            plt.plot(x, d, label=lab)
            plt.axvline(w, color='r', linestyle='--', label='x' + str(w))
        plt.title('r = ' + str(dr.index(dri) + 1))
        plt.legend()
        plt.show()
        pos = plt.ginput(4)
        print(pos)
        plt.close()


def a():
    phi_c = 30
    k0 = 0.45
    sigh = k0 * 56.38
    qc = 3.9
    dr = (math.log(qc * 10) - 0.4947 - 0.1041 * phi_c - 0.841 * math.log(sigh / 100)) / (
            0.0264 - 0.0002 * phi_c - 0.0047 * math.log(sigh / 100)
    )
    print(dr)


a()
