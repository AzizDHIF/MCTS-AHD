import numpy as np

def heuristics_v2(prize, weight):
    n, m = len(prize), len(weight[0])
    heuristics_matrix = np.zeros(n)
    temperature = 1.0
    for i in range(n):
        weights_perturbed = weight[i] + np.random.normal(0, 0.1, m)
        weights_perturbed = np.clip(weights_perturbed, 0, 1)
        heuristics_matrix[i] = prize[i] / np.sum(weights_perturbed)
        if np.random.rand() < temperature:
            heuristics_matrix[i] *= np.random.uniform(0.9, 1.1)
        temperature *= 0.99
    return heuristics_matrix
