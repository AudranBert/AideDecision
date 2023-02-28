from dataclasses import dataclass
from enum import Enum
import itertools
import numpy as np
from util import yield_pairs

class PrometheeSortCriterion(Enum):
    PHI_POS = 0
    PHI_NEG = 1
    PHI_TOTAL = 2

@dataclass
class PrometheeResults:
    phi_pos: np.array
    phi_neg: np.array
    phi_total: np.array
    score_table: np.ndarray

    def repr_labelled(self, labels) -> str:
        return f"""\
ϕ+: {self.phi_pos}
ϕ-: {self.phi_neg}
ϕ*: {self.phi_total}

by ϕ+: {self.format_order_seq(PrometheeSortCriterion.PHI_POS, labels)}
by ϕ-: {self.format_order_seq(PrometheeSortCriterion.PHI_NEG, labels)}
by ϕ*: {self.format_order_seq(PrometheeSortCriterion.PHI_TOTAL, labels)}

scores:
{self.score_table.T}"""

    def format_order_seq(self, criterion, labels):
        if criterion == PrometheeSortCriterion.PHI_POS:
            phi = self.phi_pos
        elif criterion == PrometheeSortCriterion.PHI_NEG:
            phi = -self.phi_neg
        elif criterion == PrometheeSortCriterion.PHI_TOTAL:
            phi = self.phi_total
        
        best_order = np.argsort(phi)
        labelled = [labels[i] for i in best_order]
    

        signs = [
            "<=" if np.isclose(phi[a], phi[b]) else "<"
            for a, b in itertools.pairwise(best_order)
        ]
        
        out = labelled[0]

        for i in range(len(signs)):
            out += f" {signs[i]} {labelled[i+1]}"
        
        return out

def promethee_binary_step(x):
    return np.where(x > 0, 1, 0)

def make_promethee_linear_step(threshs):
    return lambda x: np.clip(x, 0, threshs) / threshs

def process_promethee_pair(
    xi, xj, pref_func, feat_weights
):
    diff = xj - xi
    stepped = pref_func(diff)
    weights = stepped * feat_weights
    return weights.sum()

def promethee(
    dataset,
    feat_mul,
    feat_weights,
    pref_func=promethee_binary_step
) -> PrometheeResults:
    x_norm = dataset * feat_mul

    num_items = dataset.shape[0]
    score_table = np.zeros((num_items, num_items))

    for i, j in yield_pairs(num_items):
        score_table[i][j] = process_promethee_pair(x_norm[i], x_norm[j], pref_func, feat_weights)

    phi_pos = np.sum(score_table, axis=0) / (num_items - 1)
    phi_neg = np.sum(score_table, axis=1) / (num_items - 1)
    phi_total = phi_pos - phi_neg

    return PrometheeResults(
        phi_pos,
        phi_neg,
        phi_total,
        score_table
    )