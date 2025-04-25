import math

def euclidean_distance(data, vars, obj, index):
    sum_sq = 0
    for var in vars:
        diff = obj[var] - data[var][index]
        sum_sq += diff ** 2
    return math.sqrt(sum_sq)

def manhattan_distance(data, vars, obj, index):
    total = 0
    for var in vars:
        diff = abs(obj[var] - data[var][index])
        total += diff
    return total
