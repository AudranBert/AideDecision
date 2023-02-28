import pandas as pd
from pathlib import Path
import numpy as np
import graphviz as gv

from electre import electre, make_electre_linear_step
from promethee import promethee

root = Path("data/hevea/")

data = pd.read_csv(root / "donnees.csv", header=None).values
weights = pd.read_csv(root / "poids.csv", header=None).values.squeeze()
threshs = pd.read_csv(root / "seuilpref.csv", header=None).values.squeeze()

print(f"Data shape: {data.shape}")
print(f"Weights shape: {weights.shape}")
print(f"Thresholds shape: {threshs.shape}")

col_count = data.shape[-1]
instance_count = data.shape[0]

feat_mul = np.ones((col_count,))
feat_mul[0] = -1  # âge d'ouverture => à minimiser

print("=== RÉSULTATS POUR PROMETHEE ===")

promethee_results = promethee(
    dataset=data,
    feat_mul=feat_mul,
    feat_weights=weights
)

labels = list(str(name) for name in range(instance_count))

print(promethee_results.repr_labelled(labels))

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