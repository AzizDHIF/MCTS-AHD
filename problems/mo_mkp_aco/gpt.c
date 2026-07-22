#include "HBACO.h"
double heuristic(int index_item, double weights[dimension][NBITEMS], double capacity[dimension], int nb_voisinage, int voisinage[NBITEMS], double profit[NBITEMS] ) {
double total_weight = 0.0;
for (int d = 0; d < dimension; d++) {
total_weight += weights[d][index_item];
for (int i = 0; i < nb_voisinage; i++) {
total_weight += weights[d][voisinage[i]];
}
}
double remaining_capacity = 1.0;
for (int d = 0; d < dimension; d++) {
remaining_capacity = remaining_capacity * capacity[d];
}
double heuristic_value = (total_weight > 0.0) ? (profit[index_item] / total_weight) * remaining_capacity : 0.0;
return heuristic_value;
}
