import numpy as np

#nは次元数

#最適解[0, ..., 0]^n, 評価値0.0, 単峰性 
def Sphere(x):
    eval = float (((x) * (x)).sum())
    return eval

#最適解[0, ..., 0]^n, 評価値0, 多峰性
def Rastrigin(x):
    value  = 0
    n = x.shape[0]
    for i in range(n):
        value +=  (x[i])**2 - 10 * np.cos(2 * np.pi * (x[i]))

    value += 10  * n
    return value

#最適解[1, ..., 1]^n, 評価値0, 変数間依存性 
def RozenBlock(x):
    dim = x.shape[0]
    value = 0.0
    for i in range(dim - 1):
        value += 100.0 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1.0) ** 2
    return value  