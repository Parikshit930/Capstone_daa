"""
tsp_route.py
Implementation of Nearest Neighbor TSP Approximation and 2-Opt Optimization.
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

from typing import List, Dict, Tuple, Optional
from src.models import DeliveryGraph
from src.shortest_path import compute_all_pairs_shortest_paths


class DeliveryPlan:
    """Encapsulates the final route plan and metrics."""

    def __init__(
        self,
        stop_sequence: List[str],
        full_road_path: List[str],
        total_distance: float,
        leg_details: List[Dict[str, Any]],
    ):
        self.stop_sequence = stop_sequence      # [Depot, C1, C3, C2, Depot]
        self.full_road_path = full_road_path    # Detailed road turn-by-turn node list
        self.total_distance = total_distance    # Total kilometers travelled
        self.leg_details = leg_details          # Details for each leg of the trip


from typing import Any


def nearest_neighbor_tsp(
    depot: str,
    delivery_stops: List[str],
    dist_matrix: Dict[Tuple[str, str], float],
    path_matrix: Dict[Tuple[str, str], List[str]]
) -> DeliveryPlan:
    """
    Nearest Neighbor Heuristic for the Traveling Salesperson Problem (TSP).

    Greedy strategy:
      1. Start at depot.
      2. Repeatedly visit the closest unvisited delivery stop.
      3. Return to depot after all stops are visited.

    Time Complexity: O(k^2) where k is the number of stops.
    Approximation Ratio: Within O(log k) of optimal for metric TSP.
    """
    unique_stops = list(dict.fromkeys(delivery_stops))
    # Remove depot if mistakenly passed in delivery_stops
    if depot in unique_stops:
        unique_stops.remove(depot)

    if not unique_stops:
        return DeliveryPlan(
            stop_sequence=[depot],
            full_road_path=[depot],
            total_distance=0.0,
            leg_details=[],
        )

    unvisited = set(unique_stops)
    current = depot
    stop_sequence = [depot]
    full_road_path = [depot]
    total_distance = 0.0
    leg_details = []

    # Visit all stops
    while unvisited:
        next_node = None
        min_dist = float("inf")

        for candidate in unvisited:
            d = dist_matrix.get((current, candidate), float("inf"))
            if d < min_dist:
                min_dist = d
                next_node = candidate

        if next_node is None or min_dist == float("inf"):
            raise RuntimeError(f"Unreachable delivery stop from {current}. Check graph connectivity.")

        total_distance += min_dist
        stop_sequence.append(next_node)
        unvisited.remove(next_node)

        # Append intermediate road nodes
        leg_path = path_matrix.get((current, next_node), [current, next_node])
        if len(leg_path) > 1:
            full_road_path.extend(leg_path[1:])

        leg_details.append({
            "from": current,
            "to": next_node,
            "distance_km": round(min_dist, 2),
            "road_path": leg_path,
        })
        current = next_node

    # Return trip to depot
    return_dist = dist_matrix.get((current, depot), float("inf"))
    if return_dist == float("inf"):
        raise RuntimeError(f"Cannot return to depot from {current}. Check graph connectivity.")

    total_distance += return_dist
    stop_sequence.append(depot)
    return_path = path_matrix.get((current, depot), [current, depot])
    if len(return_path) > 1:
        full_road_path.extend(return_path[1:])

    leg_details.append({
        "from": current,
        "to": depot,
        "distance_km": round(return_dist, 2),
        "road_path": return_path,
    })

    return DeliveryPlan(
        stop_sequence=stop_sequence,
        full_road_path=full_road_path,
        total_distance=round(total_distance, 2),
        leg_details=leg_details,
    )


def two_opt_optimize(
    initial_plan: DeliveryPlan,
    dist_matrix: Dict[Tuple[str, str], float],
    path_matrix: Dict[Tuple[str, str], List[str]]
) -> DeliveryPlan:
    """
    2-Opt Local Search heuristic to eliminate crossing paths in the tour.
    Iteratively swaps pairs of edges if doing so reduces total tour distance.
    """
    stops = list(initial_plan.stop_sequence)
    if len(stops) <= 4:
        # Depot -> 1 or 2 stops -> Depot: cannot be improved by 2-opt
        return initial_plan

    depot = stops[0]
    inner_stops = stops[1:-1] # Stops excluding start and end depot

    def calculate_tour_distance(route_stops: List[str]) -> float:
        d = 0.0
        for i in range(len(route_stops) - 1):
            pair = (route_stops[i], route_stops[i + 1])
            d += dist_matrix.get(pair, float("inf"))
        return d

    improved = True
    best_inner = list(inner_stops)
    best_dist = initial_plan.total_distance

    while improved:
        improved = False
        for i in range(len(best_inner) - 1):
            for j in range(i + 1, len(best_inner)):
                # 2-opt swap reverses the segment between i and j
                new_inner = best_inner[:i] + best_inner[i:j + 1][::-1] + best_inner[j + 1:]
                candidate_tour = [depot] + new_inner + [depot]
                cand_dist = calculate_tour_distance(candidate_tour)

                if cand_dist < best_dist - 1e-4:
                    best_inner = new_inner
                    best_dist = cand_dist
                    improved = True
                    break
            if improved:
                break

    optimized_tour = [depot] + best_inner + [depot]

    # Reconstruct leg details
    full_road_path = [depot]
    leg_details = []
    for i in range(len(optimized_tour) - 1):
        u, v = optimized_tour[i], optimized_tour[i + 1]
        leg_dist = dist_matrix.get((u, v), 0.0)
        leg_path = path_matrix.get((u, v), [u, v])
        if len(leg_path) > 1:
            full_road_path.extend(leg_path[1:])
        leg_details.append({
            "from": u,
            "to": v,
            "distance_km": round(leg_dist, 2),
            "road_path": leg_path,
        })

    return DeliveryPlan(
        stop_sequence=optimized_tour,
        full_road_path=full_road_path,
        total_distance=round(best_dist, 2),
        leg_details=leg_details,
    )
