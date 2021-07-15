import math


class Layer:
    top = 0
    btm = 0
    h = 0
    cc = 0
    cs = 0
    gm = 0
    e0 = 0
    ez = 0
    dh = 0

    def print_val(self):
        print("{},{},{},{},{},{},{},{},{}"
              .format(self.top, self.btm, self.gm, self.cc, self.cs, self.e0, self.h, self.ez, self.dh))


def read_val():
    cc = [0.22, 0.25, 0.92, 0.62, 0.91, 0.32, 0.33, 0.36, 0.68, 0.4, 0.42, 0.45, 0]
    cs = [0.025, 0.05, 0.14, 0.12, 0.15, 0.04, 0.05, 0.06, 0.11, 0.08, 0.09, 0.08, 0]
    e0 = [0.9, 0.95, 1.22, 1.4, 1.66, 0.66, 0.79, 0.76, 0.81, 0.9, 1.0, 1.14, 0.5]
    fp = open(r"result.txt")
    ls = fp.readlines()
    fp.close()
    ls = [eval(i.replace('\n', '')) for i in ls]
    ls.reverse()
    ly = []
    while len(ls) != 0:
        t = Layer()
        t.cc = cc[len(ly)]
        t.cs = cs[len(ly)]
        t.e0 = e0[len(ly)]
        t.top = ls.pop()
        t.btm = ls.pop()
        t.gm = ls.pop()
        t.h = t.top - t.btm
        ly.append(t)
    cal(ly)


def cal(ls):
    q = 497.51
    sig1 = 0
    for t in ls:
        sig0 = t.h/2 * t.gm + sig1 + (t.btm + t.h/2 + 1)*9.81
        sig1 += t.h * t.gm
        sig = sig0 + q
        if ls.index(t) < 5:
            oc = t.cs/(1+t.e0)*math.log10(sig/sig0)
            t.ez = oc
        else:
            nc = t.cc/(1+t.e0)*math.log10(sig/sig0)
            t.ez = nc
        t.dh = t.ez * t.h
        print("Gm: {:.1f}, sig0: {:.1f}, sig: {:.1f}, e0: {:.3f}, Cc: {:.3f}, Cs: {:.3f}, Ez: {:.3f}, dH: {:.3f}"
              .format(t.gm, sig0, sig, t.e0, t.cc, t.cs, t.ez, t.dh))
    print("Total settlement: ", sum([i.dh for i in ls]))


read_val()
