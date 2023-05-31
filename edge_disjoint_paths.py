from core import Predecessors
from push_relabel import *


def edge_disjoint_paths(g: Digraph, source: Node, sink: Node) -> Iterable:
    """Given directed graph G, and two nodes s and t, find k paths from
        s to t such that no two paths share an edge.

    Menger’s Theorem: Given a directed graph G with nodes s,t the maximum number of
        edge-disjoint s-t paths equals the minimum number of edges whose
        removal separates s from t.

    Suppose you want to send k large files from s to t but never have two files use
        the same network link (to avoid congestion on the links).
    """

    for u in g:
        for v in g[u]:
            g[u][v].cap = 1
    fifo_push_relabel(g, source, sink)

    # use dfs to find the paths
    S, paths = [source], []
    visited: set[Node] = set()
    pred: Predecessors = defaultdict(lambda: None)

    while S:
        u = S.pop()
        if u == sink:
            path = [sink]
            current = pred[sink]
            while current is not None:
                path.append(current)
                current = pred[current]
            paths.append(tuple(reversed(path)))
            continue
        if u in visited:
            continue
        visited.add(u)
        for v in adjacency(g, u):
            if u not in visited and g[u][v].flow:
                S.append(v)
                pred[v] = u
    return iter(paths)
