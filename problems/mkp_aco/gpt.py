import numpy as np

def heuristics_v3(prize, weight):
    # Calculate the maximum weight for each item across all dimensions
    max_weight = np.max(weight, axis=1)
    
    # Calculate the sum of weights for each item across all dimensions
    weights_sum = np.sum(weight, axis=1)
    
    # Calculate the variance of the prizes
    prize_variance = np.var(prize)
    
    # Calculate the variance of the weights
    weight_variance = np.var(weight)
    
    # Calculate the weighted sum for each item by dividing its prize by the sum of weights and the maximum weight
    weighted_prize = prize / (weights_sum * max_weight + 1e-8)
    
    # Calculate the dynamic weights based on the variance of the prizes and the weights
    dynamic_weights = np.sqrt(prize_variance) / (weight_variance + 1e-8)
    
    # Calculate the heuristics for each item by multiplying the weighted prize with the prize and the cube root of the prize
    heuristics_matrix = (weighted_prize * prize * np.cbrt(prize)) * dynamic_weights * np.log(weights_sum + 1e-8)
    
    # Normalize the heuristics by the maximum heuristics across all items
    max_heuristics = np.max(heuristics_matrix)
    heuristics_matrix = heuristics_matrix / (max_heuristics + 1e-8)
    
    return heuristics_matrix
