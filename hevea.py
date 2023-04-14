import pandas as pd
from pathlib import Path
import numpy as np
import graphviz as gv

from electre import electre, make_electre_linear_step
from promethee import promethee

root = Path("data/hevea/")

data = pd.read_csv(root / "donnees.csv", header=None).values
weights = pd.read_csv(root / "poids.csv", header=None).values.squeeze() / 100.0
threshs = pd.read_csv(root / "seuilpref.csv", header=None).values.squeeze()

print(f"Data shape: {data.shape}")
print(f"Weights shape: {weights.shape}")
print(f"Thresholds shape: {threshs.shape}")

col_count = data.shape[-1]
instance_count = data.shape[0]

feat_mul = np.ones((col_count,))
feat_mul[0] = -1  # âge d'ouverture => à minimiser

# print("=== RÉSULTATS POUR PROMETHEE ===")

# promethee_results = promethee(
#     dataset=data,
#     feat_mul=feat_mul,
#     feat_weights=weights
# )

# labels = list(str(name) for name in range(instance_count))

# promethee_rank = list(reversed(np.argsort(promethee_results.phi_total)))
# promethee_sorted_data = data[promethee_rank]

# # as LaTeX table
# promethee_sorted_data = pd.DataFrame(promethee_sorted_data)
# promethee_sorted_data.columns = [
#     "Ouv",
#     "P15",
#     "Vent",
#     "TPD",
#     "DL",
#     "Col",
#     "Cor",
#     "Oid",
#     "Tech",
#     "Bois",
#     "Gref"
# ]

# # index starts at 1, named "rang"
# promethee_sorted_data.index += 1
# promethee_sorted_data.index.name = "Rang"

# # insert column "instance id" according to promethee_rank
# promethee_sorted_data.insert(0, "Instance", promethee_rank)

# print(promethee_sorted_data.style.set_table_styles([
#     {'selector': 'toprule', 'props': ':hline;'},
#     {'selector': 'midrule', 'props': ':hline;'},
#     {'selector': 'bottomrule', 'props': ':hline;'},
# ], overwrite=False).to_latex())

# print(promethee_results.repr_labelled(labels))

print("\n\n\n=== RÉSULTATS POUR ELECTRE ===")

results = electre(
    dataset=data,
    feat_mul=feat_mul,
    feat_weights=weights,
    pref_func=make_electre_linear_step(threshs),
    match_thresh=0,
    veto_threshs=None
)

print(results)