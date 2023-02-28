from dataclasses import dataclass
import numpy as np
from util import format_set

@dataclass
class ParetoResults:
    optimal: set
    only_weakly_dominated: set
    strongly_dominated: set

    def repr_labelled(self, labels) -> str:
        return f"""\
optimal:            {format_set(self.optimal, labels)}
weakly dominated:   {format_set(self.only_weakly_dominated, labels)}
strongly dominated: {format_set(self.strongly_dominated, labels)}"""

def pareto(dataset, feat_mul) -> ParetoResults:
    x_norm = dataset * feat_mul
    
    all_indices = set(range(dataset.shape[0]))
    optimal = set(all_indices)
    only_weakly_dominated = set()

    for i in all_indices:
        for j in (optimal | only_weakly_dominated) - {i}:
            if np.all(x_norm[i] > x_norm[j]):
                only_weakly_dominated.discard(j)
                optimal.discard(j)
            elif np.all(x_norm[i] >= x_norm[j]):
                only_weakly_dominated.add(j)
                optimal.discard(j)

    return ParetoResults(
        optimal=optimal,
        only_weakly_dominated=only_weakly_dominated,
        strongly_dominated=all_indices - optimal - only_weakly_dominated
    )