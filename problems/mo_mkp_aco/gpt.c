{ The design idea and main steps of the algorithm involve calculating a heuristic value for each item based on its profit and the remaining capacity of the knapsacks, with the goal of selecting items that maximize profit while not exceeding capacity, and main steps include calculating the total weight of the item, checking if including the item exceeds the capacity, and calculating the heuristic value based on the profit and weight of the item. }
double heuristic(int index_item, double weights[dimension][NBITEMS], double capacity[dimension], int nb_voisinage, int voisinage[NBITEMS], double profit[NBITEMS] ) {
    double total_weight = 0;
    for (int i = 0; i < dimension; i++) {
        total_weight += weights[i][index_item];
    }
    if (total_weight > 1) {
        return -1;
    }
    double remaining_capacity = 1 - total_weight;
    double heuristic_value = profit[index_item] / total_weight;
    return heuristic_value;
}
