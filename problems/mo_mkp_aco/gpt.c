def heuristic2(index_item, weights, capacity, nb_voisinage, voisinage, profit):
    NBITEMS = len(profit)
    dimension = len(capacity)
    heuristics_matrix = []
    
    for i in range(NBITEMS):
        heuristic_value = 0
        weight_sum = 0
        
        for d in range(dimension):
            if capacity[d] - weights[d][i] >= 0:
                weight_sum += weights[d][i]
        
        if weight_sum > 0:
            heuristic_value = profit[i] / weight_sum
        
        for j in range(nb_voisinage):
            if voisinage[j] == i:
                heuristic_value -= 0.1  # decrease heuristic value for items with neighbours
        
        heuristics_matrix.append(heuristic_value)
    
    return heuristics_matrix
