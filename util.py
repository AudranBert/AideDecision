def format_set(indices, labels) -> str:
    if len(indices) == 0:
        return "∅"

    return ", ".join(labels[i] for i in indices)


def yield_pairs(num_items: int):
    for j in range(num_items):
        for i in range(num_items):
            if i != j:
                yield i, j
