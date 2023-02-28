from dataclasses import dataclass
import numpy as np
import graphviz as gv
from util import yield_pairs


@dataclass
class ElectreResults:
    kernel: list[tuple[int, int]]
    score_table: np.ndarray
    non_veto_table: np.ndarray
    graph: gv.Digraph

    def repr_labelled(self, labels) -> str:
        return f"""\
kernel: {list((labels[i], labels[j]) for i, j in self.kernel)}
score_table:
{self.score_table.T}
non_veto_table:
{self.non_veto_table.T}"""


def electre_binary_step(x):
    return np.where(x >= 0, 1, 0)


def make_electre_linear_step(threshs):
    return lambda x: (np.clip(x + threshs, 0, threshs) / threshs)



def electre(
    dataset,
    feat_mul,
    feat_weights,
    pref_func,
    match_thresh,
    veto_threshs
):
    x_norm = dataset * feat_mul

    num_items = dataset.shape[0]

    score_table = np.zeros((num_items, num_items))

    # given [i][j], is i NOT vetoed by j?
    non_veto_table = np.zeros((num_items, num_items), dtype=np.bool_)

    for i, j in yield_pairs(num_items):
        diff = x_norm[j] - x_norm[i]

        stepped = pref_func(diff)
        weights = stepped * feat_weights
        score_table[i][j] = weights.sum()

        j_vetoes_i = diff >= veto_threshs
        non_veto_table[j][i] = not np.any(j_vetoes_i)

        # print(f"Test veto A{j+1} -> A{i+1}: {diff}, {diff < veto_threshs}")

    for test_thresh in np.arange(0.5, 1.0, 0.02):
        kernel = []

        for i, j in yield_pairs(num_items):
            if score_table[i][j] >= test_thresh and non_veto_table[i][j]:
                kernel.append((i, j))
        
        print(f"s={test_thresh:.2f}: {', '.join(f'A{i+1}<-A{j+1}' for i, j in kernel)}")

    kernel = []

    # build graph
    g = gv.Digraph()

    for i in range(num_items):
        g.node(str(i), f"A{i+1}")

    for i, j in yield_pairs(num_items):
        if score_table[i][j] >= match_thresh and non_veto_table[i][j]:
            kernel.append((j, i))
            g.edge(str(j), str(i), label=f"{score_table[i][j]:.2f}")
    
    return ElectreResults(kernel, score_table, non_veto_table, g)