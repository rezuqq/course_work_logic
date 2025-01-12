
def dfs(x, vis, px, py, adj):
    if vis[x]:
        return False
    vis[x] = True

    for y in adj[x]:
        if py[y] == -1:  # Если вершина y свободна
            py[y] = x
            px[x] = y
            return True
        elif dfs(py[y], vis, px, py, adj):  # Если путь можно продолжить через y
            py[y] = x
            px[x] = y
            return True

    return False

def max_matching_ford_fulkerson(n, m, edges):
    """
    Реализация алгоритма Форда-Фалкерсона для двудольного графа.

    :param n: Количество вершин в первой доле.
    :param m: Количество вершин во второй доле.
    :param edges: Список рёбер графа, где каждое ребро задаётся как (u, v).
    :return: Список максимального паросочетания в формате [(u1, v1), (u2, v2), ...].
    """
    adj = {x: [] for x in range(n)}  # Список смежности для вершин первой доли
    for u, v in edges:
        adj[u].append(v)

    px = {x: -1 for x in range(n)}  # Соответствие для вершин первой доли
    py = {y: -1 for y in range(n, n + m)}  # Соответствие для вершин второй доли

    is_path = True
    while is_path:
        is_path = False
        vis = {x: False for x in range(n)}  # Посещённые вершины первой доли

        for x in range(n):
            if px[x] == -1:  # Если вершина x свободна
                if dfs(x, vis, px, py, adj):
                    is_path = True

    # Формирование результата в виде списка пар
    matching = [(x, px[x]) for x in range(n) if px[x] != -1]
    return matching

