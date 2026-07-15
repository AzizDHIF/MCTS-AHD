import numpy as np

def heuristics_v2(prize, weight):
    n = len(prize)
    heuristics = np.zeros(n)
    for i in range(n):
        sum_weights = np.sum(weight[i])
        if sum_weights == 0:
            heuristics[i] = 0.0
        else:
            heuristics[i] = prize[i] / sum_weights
    return heuristics_matrix
