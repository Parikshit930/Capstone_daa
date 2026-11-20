"""
shortest_path.py
Implementation of Dijkstra's Algorithm for Single-Source & All-Pairs Shortest Paths.
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

import heapq
from typing import Dict, List, Tuple, Optional
from src.models import DeliveryGraph


def dijkstra_shortest_path(
    graph: DeliveryGraph,
    source: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Computes shortest path distances and predecessors from `source` to all reachable nodes
    using Dijkstra's algorithm with a Min-Heap (Priority Queue).

    Time Complexity: O((V + E) * log V)
    Space Complexity: O(V) for distance and predecessor dictionaries
    """
    if source not in graph.adj_list:
        raise ValueError(f"Source node '{source}' does not exist in graph.")

    distances: Dict[str, float] = {node: float("inf") for node in graph.get_nodes()}
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph.get_nodes()}

    distances[source] = 0.0
    # Priority queue stores tuples of (distance, node)
    pq: List[Tuple[float, str]] = [(0.0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        # Skip if we found a shorter path already
        if curr_dist > distances[u]:
            continue

        for v, weight in graph.get_neighbors(u):
            new_dist = curr_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))

    return distances, predecessors


def reconstruct_path(predecessors: Dict[str, Optional[str]], target: str) -> List[str]:
    """Reconstructs the sequence of nodes from source to target."""
    path = []
    curr: Optional[str] = target
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    path.reverse()
    return path


def compute_all_pairs_shortest_paths(
    graph: DeliveryGraph,
    nodes_subset: Optional[List[str]] = None
) -> Tuple[Dict[Tuple[str, str], float], Dict[Tuple[str, str], List[str]]]:
    """
    Runs Dijkstra from each node in `nodes_subset` (or all nodes) to construct:
    1. dist_matrix: (u, v) -> shortest distance
    2. path_matrix: (u, v) -> full list of nodes [u, ..., v]
    """
    nodes = nodes_subset if nodes_subset is not None else graph.get_nodes()
    dist_matrix: Dict[Tuple[str, str], float] = {}
    path_matrix: Dict[Tuple[str, str], List[str]] = {}

    for u in nodes:
        distances, predecessors = dijkstra_shortest_path(graph, u)
        for v in nodes:
            dist_matrix[(u, v)] = distances.get(v, float("inf"))
            if distances.get(v, float("inf")) < float("inf"):
                path_matrix[(u, v)] = reconstruct_path(predecessors, v)
            else:
                path_matrix[(u, v)] = []

    return dist_matrix, path_matrix
