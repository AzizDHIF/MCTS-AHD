#include "HBACO.h"
double heuristic(int index_item, double **weights, double *capacity, int nb_voisinage, int *voisinage, double *profit) {
/* The algorithm evaluates the potential inclusion of an item by calculating a score based on the profit contribution and incorporating a penalty for weight usage, promoting items that offer high profit while minimally impacting the remaining capacities. */
double score = 0.0;
double profit_penalty = 0.0;

for (int d = 0; d < dimension; d++) {
if (weights[d][voisinage[index_item]] <= capacity[d]) {
score += profit[voisinage[index_item]]; // Accumulate the profit
profit_penalty += weights[d][voisinage[index_item]]; // Add a penalty for weight usage
}
}

return score - profit_penalty; // Incorporate penalty into the score
}
