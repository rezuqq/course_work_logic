
def dfs(x, vis, px, py, adj):
    if vis[x]:
        return False
    vis[x] = True

    for y in adj[x]:
        if py[y] == -1:
            py[y] = x
            px[x] = y
            return True
        elif dfs(py[y], vis, px, py, adj):
            py[y] = x
            px[x] = y
            return True

    return False

def max_matching_ford_fulkerson(n, m, edges):

    adj = {x: [] for x in range(n)}
    for u, v in edges:
        adj[u].append(v)

    px = {x: -1 for x in range(n)}
    py = {y: -1 for y in range(n, n + m)}

    is_path = True
    while is_path:
        is_path = False
        vis = {x: False for x in range(n)}

        for x in range(n):
            if px[x] == -1:
                if dfs(x, vis, px, py, adj):
                    is_path = True

    matching = [(x, px[x]) for x in range(n) if px[x] != -1]
    return matching

