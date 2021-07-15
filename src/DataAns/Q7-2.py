import numpy as np


def q1():
    m = np.array([[2, -0.5, 0, 0],
                  [-0.5, 2, -0.5, 0],
                  [0, -0.5, 2, -0.5],
                  [0, 0, -0.5, 2]])
    b = np.array([[0.16 + 0.01, 0.24, 0.24, 0.16]]).T
    c = np.linalg.solve(m, b)
    # print(np.dot(m, c))
    # print("------------")
    print(c)
    print("------------")
    c[0] = c[0] + 0.02
    d = np.linalg.solve(m, c)
    # print(np.dot(m, d))
    # print("------------")
    print(d)


q1()
