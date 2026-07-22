double heuristic_eval_100(int index_item, double weights[dimension][NBITEMS_100], double capacity[dimension], int nb_voisinage, int voisinage[NBITEMS_100], double profit[NBITEMS_100] ) {
    double sum_weights = 0.0;
    for (int i = 0; i < dimension; i++) {
        sum_weights += weights[i][index_item];
    }
    double average_weight = sum_weights / dimension;
    double max_profit = -1.0;
    for (int i = 0; i < nb_voisinage; i++) {
        if (profit[voisinage[i]] > max_profit) {
            max_profit = profit[voisinage[i]];
        }
    }
    double heuristic_value = max_profit / (average_weight + 1);
    for (int i = 0; i < dimension; i++) {
        if (weights[i][index_item] > capacity[i]) {
            heuristic_value = -1.0;
            break;
        }
    }
    return heuristic_value;
}
