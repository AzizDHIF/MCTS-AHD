double heuristic(int index_item, double weights[dimension][NBITEMS], double capacity[dimension], int nb_voisinage, int voisinage[NBITEMS], double profit[NBITEMS]) {
    double item_weight_sum = 0.0;
    int feasible = 1;
    for (int d = 0; d < dimension; d++) {
        if (weights[d][index_item] > capacity[d]) {
            feasible = 0;
            break;
        }
        item_weight_sum += weights[d][index_item];
    }
    if (!feasible) return 0.0;
    
    double item_ratio = profit[index_item] / (1.0 + item_weight_sum);
    double neighbor_sum = 0.0;
    for (int i = 0; i < nb_voisinage; i++) {
        int n_idx = voisinage[i];
        double n_weight = 0.0;
        for (int d = 0; d < dimension; d++) {
            n_weight += weights[d][n_idx];
        }
        neighbor_sum += profit[n_idx] / (1.0 + n_weight);
    }
    if (nb_voisinage > 0) {
        item_ratio += 0.5 * (neighbor_sum / (double)nb_voisinage);
    }
    return item_ratio;
}
