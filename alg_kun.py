import random
from collections import defaultdict

g = defaultdict(list)
mt = []
used = []

def generate_random_bipartite_edges(n, m, edge_probability):
    edges = []
    for i in range(n):
        for j in range(m):
            if random.random() < edge_probability:
                edges.append((i, n + j))
    return edges

def try_kuhn(v):
    if used[v]:
        return False
    used[v] = True
    for to in g[v]:
        if mt[to] == -1 or try_kuhn(mt[to]):
            mt[to] = v
            return True
    return False


def max_matching_kun_algorithm(n, m, edges):
    global g, mt, used

    g = defaultdict(list)
    for u, v in edges:
        if u < 0 or u >= n or v < n or v >= n + m:
            raise ValueError(
                f"Некорректное ребро: ({u}, {v}). Убедитесь, что u в [0, {n - 1}], а v в [{n}, {n + m - 1}].")
        g[u].append(v - n)

    mt = [-1] * m
    for v in range(n):
        used = [False] * n
        try_kuhn(v)

    matching = [(u, v + n) for v, u in enumerate(mt) if u != -1]
    return matching