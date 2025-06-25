import numpy as np
from collections import Counter

def entropy(S):
    total = len(S)
    counts = Counter(S)
    return -sum((c/total) * np.log2(c/total) for c in counts.values() if c > 0)

def gain(S, A):
    total = len(S)
    subsets = {}
    for i, value in enumerate(A):
        subsets.setdefault(value, []).append(S[i])
    weighted_entropy = sum((len(subset)/total) * entropy(subset) for subset in subsets.values())
    return entropy(S) - weighted_entropy

def split_info(A):
    total = len(A)
    counts = Counter(A)
    return -sum((c/total) * np.log2(c/total) for c in counts.values() if c > 0)

def gain_ratio(S, A):
    g = gain(S, A)
    si = split_info(A)
    return g, g / si if si != 0 else 0

def mejor_variable_por_gain_ratio(data, ids, excluidas):
    class_labels = [data['class'][i] for i in ids]
    mejor = (None, 0, 0)  # (nombre_variable, ganancia, índice de ganancia)

    for var in data:
        if var not in excluidas and var != 'class':
            atributo = [data[var][i] for i in ids]
            g, gr = gain_ratio(class_labels, atributo)
            if gr > mejor[2]:
                mejor = (var, round(g, 4), round(gr, 4))
    
    return mejor
