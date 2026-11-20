"""
main.py
Interactive CLI & Automated Demonstration Runner for Mini-Courier Planner.
Course: Design & Analysis of Algorithms (ETCCDA302)
Faculty: Dr. Shweta Agarwal | K.R. Mangalam University
"""

import sys
import json
import argparse
from typing import Dict, Any, List

from src.models import Parcel, DeliveryGraph
from src.sorting import prioritize_parcels, merge_sort, quick_sort
from src.knapsack import solve_01_knapsack, greedy_knapsack_heuristic, KnapsackResult
from src.shortest_path import dijkstra_shortest_path, compute_all_pairs_shortest_paths
from src.tsp_route import nearest_neighbor_tsp, two_opt_optimize, DeliveryPlan
from benchmark import run_all_benchmarks


def load_dataset(filepath: str) -> Tuple[str, int, DeliveryGraph, List[Parcel]]:
    """Loads dataset from JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)

    depot = data.get("depot", "D0")
    capacity = int(data.get("vehicle_capacity_kg", 20))
    graph = DeliveryGraph.from_dict(data["graph"])
    parcels = [Parcel.from_dict(p) for p in data["parcels"]]

    return depot, capacity, graph, parcels


from typing import Tuple


def print_banner():
    banner = """
================================================================================
     MINI-COURIER PLANNER: ALGORITHMIC OPTIMIZATION ENGINE
     Student: Parikshit Chauhan | Roll No: 2501730398
     Course: Design & Analysis of Algorithms (ETCCDA302)
     Faculty: Dr. Shweta Agarwal | K.R. Mangalam University
================================================================================
    """
    print(banner)


def run_pipeline(dataset_path: str = "data/sample_small.json", verbose: bool = True):
    print("\n" + "=" * 80)
    print(f"  RUNNING END-TO-END PIPELINE ON: {dataset_path}")
    print("=" * 80)

    # ---------------------------------------------------------
    # PHASE 1: Data Modeling & Problem Setup
    # ---------------------------------------------------------
    print("\n[PHASE 1] COURIER PROBLEM DESIGN & DATA MODELING")
    print("-" * 80)
    depot, capacity, graph, parcels = load_dataset(dataset_path)
    print(f"• Central Dispatch Depot : {depot}")
    print(f"• Vehicle Max Payload    : {capacity} kg")
    print(f"• Road Network Vertices  : {len(graph.get_nodes())} locations")
    print(f"• Total Parcels Received : {len(parcels)} parcels\n")

    print(f"{'ID':<6}{'Customer':<18}{'Destination':<14}{'Weight(kg)':<12}{'Priority':<10}{'Deadline(h)':<10}")
    print("-" * 72)
    for p in parcels:
        print(f"{p.id:<6}{p.customer_name:<18}{p.destination:<14}{p.weight:<12}{p.priority:<10}{p.deadline_hours:<10.1f}")

    # ---------------------------------------------------------
    # PHASE 2: Prioritization & Box Packing (0/1 Knapsack DP)
    # ---------------------------------------------------------
    print("\n[PHASE 2] PACKAGE PRIORITIZATION & BOX FILLING")
    print("-" * 80)
    print("1. Sorting Parcels by Earliest Deadline First (ties broken by highest priority)...")
    prioritized = prioritize_parcels(parcels, algorithm="merge_sort")

    print(f"{'Rank':<6}{'ID':<6}{'Destination':<14}{'Deadline(h)':<14}{'Priority':<10}{'Weight(kg)':<10}")
    print("-" * 62)
    for rank, p in enumerate(prioritized, start=1):
        print(f"{rank:<6}{p.id:<6}{p.destination:<14}{p.deadline_hours:<14.1f}{p.priority:<10}{p.weight:<10}")

    print("\n2. Applying 0/1 Knapsack Dynamic Programming for Vehicle Packing...")
    knap_res = solve_01_knapsack(prioritized, capacity)

    if len(prioritized) <= 10 and capacity <= 25:
        print("\nDynamic Programming Table (Rows: Items considered, Cols: Vehicle Weight):")
        print(knap_res.print_dp_table(max_cols=capacity))

    print("\nOptimal Packing Plan for Delivery Trip:")
    print(f"  • Total Parcels Loaded : {len(knap_res.selected_parcels)} / {len(parcels)}")
    print(f"  • Total Weight Loaded  : {knap_res.total_weight} kg / {capacity} kg ({(knap_res.total_weight/capacity)*100:.1f}% capacity utilized)")
    print(f"  • Total Priority Score : {knap_res.max_value} points")
    print("\n  Selected Parcels Details:")
    for p in knap_res.selected_parcels:
        print(f"    - [{p.id}] To: {p.destination} ({p.customer_name}) | Wt: {p.weight}kg | Pri: {p.priority} | Ddl: {p.deadline_hours}h")

    # Greedy comparison for evaluation
    gr_val, gr_wt, _ = greedy_knapsack_heuristic(prioritized, capacity)
    print(f"\n  [Algorithm Insight] DP Optimal Value = {knap_res.max_value} vs Greedy Heuristic Value = {gr_val}")
    if knap_res.max_value > gr_val:
        print(f"  -> DP achieved a {((knap_res.max_value - gr_val)/gr_val)*100:.1f}% higher priority payoff than greedy selection!")

    # ---------------------------------------------------------
    # PHASE 3: Route Maker & Graph Processing
    # ---------------------------------------------------------
    print("\n[PHASE 3] ROUTE MAKER & GRAPH PROCESSING")
    print("-" * 80)
    destinations = [p.destination for p in knap_res.selected_parcels]
    unique_stops = list(dict.fromkeys(destinations))
    all_active_nodes = [depot] + [s for s in unique_stops if s != depot]

    print(f"1. Running Dijkstra's Algorithm from Depot '{depot}' across road network...")
    depot_dists, depot_preds = dijkstra_shortest_path(graph, depot)
    print(f"{'Location':<12}{'Shortest Distance from Depot':<30}")
    print("-" * 42)
    for n in sorted(graph.get_nodes()):
        dist_str = f"{depot_dists.get(n, float('inf')):.1f} km"
        print(f"{n:<12}{dist_str:<30}")

    print("\n2. Computing All-Pairs Shortest Paths for Active Delivery Stops...")
    dist_mat, path_mat = compute_all_pairs_shortest_paths(graph, all_active_nodes)

    print("3. Solving Delivery Route Sequence via Nearest-Neighbor TSP Heuristic...")
    initial_plan = nearest_neighbor_tsp(depot, unique_stops, dist_mat, path_mat)
    optimized_plan = two_opt_optimize(initial_plan, dist_mat, path_mat)

    print("\nFinal Delivery Route Sequence (Round Trip):")
    print(" -> ".join(optimized_plan.stop_sequence))

    print(f"\nTotal Round-Trip Distance : {optimized_plan.total_distance:.2f} km")
    if optimized_plan.total_distance < initial_plan.total_distance:
        print(f"(2-Opt optimization improved route by {initial_plan.total_distance - optimized_plan.total_distance:.2f} km)")

    print("\nTurn-by-Turn Leg Navigation:")
    for idx, leg in enumerate(optimized_plan.leg_details, start=1):
        path_str = " -> ".join(leg["road_path"])
        print(f"  Leg {idx}: {leg['from']} -> {leg['to']} ({leg['distance_km']} km) via [{path_str}]")

    print("\n" + "=" * 80)
    print("  PIPELINE EXECUTION COMPLETE (SUCCESS)")
    print("=" * 80)


def interactive_menu():
    print_banner()
    datasets = {
        "1": ("Small Dataset (6 Nodes, 8 Parcels - Recommended for Viva)", "data/sample_small.json"),
        "2": ("Medium Dataset (15 Nodes, 25 Parcels)", "data/sample_medium.json"),
        "3": ("Large Dataset (50 Nodes, 100 Parcels)", "data/sample_large.json"),
    }
    current_choice = "1"

    while True:
        print("\nMAIN MENU:")
        print(f"  Current Dataset: [{datasets[current_choice][0]}]")
        print("  1. Switch Dataset")
        print("  2. Phase 1: View Parcels and Delivery Network")
        print("  3. Phase 2: Sort Parcels (Merge Sort / Quick Sort)")
        print("  4. Phase 2: Pack Vehicle (0/1 Knapsack DP Table & Selection)")
        print("  5. Phase 3: Shortest Path via Dijkstra's Algorithm")
        print("  6. Phase 3: Generate Delivery Route (Nearest Neighbor TSP)")
        print("  7. Phase 4: Run Performance Benchmarking Suite (Matplotlib)")
        print("  8. Run Full End-to-End Pipeline")
        print("  0. Exit")

        choice = input("\nEnter choice [0-8]: ").strip()

        if choice == "0":
            print("\nExiting Mini-Courier Planner. Goodbye!")
            sys.exit(0)

        elif choice == "1":
            print("\nAvailable Datasets:")
            for k, (name, _) in datasets.items():
                print(f"  {k}. {name}")
            ds_choice = input("Select dataset [1-3]: ").strip()
            if ds_choice in datasets:
                current_choice = ds_choice
                print(f"Switched to: {datasets[current_choice][0]}")
            else:
                print("Invalid dataset choice.")

        elif choice == "2":
            _, filepath = datasets[current_choice]
            depot, capacity, graph, parcels = load_dataset(filepath)
            print(f"\n--- DATASET DETAILS ---")
            print(f"Depot: {depot} | Capacity: {capacity} kg | Nodes: {len(graph.get_nodes())} | Parcels: {len(parcels)}")
            print(f"\n{'ID':<6}{'Customer':<18}{'Destination':<14}{'Weight(kg)':<12}{'Priority':<10}{'Deadline(h)':<10}")
            print("-" * 72)
            for p in parcels[:20]:
                print(f"{p.id:<6}{p.customer_name:<18}{p.destination:<14}{p.weight:<12}{p.priority:<10}{p.deadline_hours:<10.1f}")
            if len(parcels) > 20:
                print(f"... and {len(parcels) - 20} more parcels.")

        elif choice == "3":
            _, filepath = datasets[current_choice]
            _, _, _, parcels = load_dataset(filepath)
            algo = input("Choose sorting algorithm ('merge' or 'quick') [default: merge]: ").strip().lower()
            algo_name = "quick_sort" if algo.startswith("q") else "merge_sort"
            sorted_parcels = prioritize_parcels(parcels, algorithm=algo_name)
            print(f"\nSorted using {algo_name.upper()} (Earliest Deadline First):")
            print(f"{'Rank':<6}{'ID':<6}{'Destination':<14}{'Deadline(h)':<14}{'Priority':<10}{'Weight(kg)':<10}")
            print("-" * 62)
            for i, p in enumerate(sorted_parcels[:15], 1):
                print(f"{i:<6}{p.id:<6}{p.destination:<14}{p.deadline_hours:<14.1f}{p.priority:<10}{p.weight:<10}")

        elif choice == "4":
            _, filepath = datasets[current_choice]
            _, capacity, _, parcels = load_dataset(filepath)
            prioritized = prioritize_parcels(parcels, algorithm="merge_sort")
            res = solve_01_knapsack(prioritized, capacity)
            if len(prioritized) <= 10 and capacity <= 25:
                print("\nDynamic Programming Table:")
                print(res.print_dp_table(max_cols=capacity))
            print(f"\nOptimal Selection: {len(res.selected_parcels)} items | Weight: {res.total_weight}/{capacity}kg | Priority: {res.max_value}")
            for p in res.selected_parcels:
                print(f"  - {p.id} to {p.destination} (wt: {p.weight}kg, pri: {p.priority})")

        elif choice == "5":
            _, filepath = datasets[current_choice]
            depot, _, graph, _ = load_dataset(filepath)
            dists, _ = dijkstra_shortest_path(graph, depot)
            print(f"\nDijkstra Shortest Distances from Depot '{depot}':")
            for node, dist in sorted(dists.items()):
                print(f"  {depot} -> {node}: {dist:.2f} km")

        elif choice == "6":
            _, filepath = datasets[current_choice]
            depot, capacity, graph, parcels = load_dataset(filepath)
            prioritized = prioritize_parcels(parcels)
            knap_res = solve_01_knapsack(prioritized, capacity)
            unique_stops = list(dict.fromkeys(p.destination for p in knap_res.selected_parcels))
            dist_mat, path_mat = compute_all_pairs_shortest_paths(graph, [depot] + unique_stops)
            plan = nearest_neighbor_tsp(depot, unique_stops, dist_mat, path_mat)
            print("\nNearest-Neighbor Route:")
            print(" -> ".join(plan.stop_sequence))
            print(f"Total Distance: {plan.total_distance:.2f} km")

        elif choice == "7":
            run_all_benchmarks()

        elif choice == "8":
            _, filepath = datasets[current_choice]
            run_pipeline(filepath)

        else:
            print("Invalid choice, please select between 0 and 8.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini-Courier Planner - DAA Capstone")
    parser.add_argument("--demo", "-d", choices=["small", "medium", "large"], help="Run automated demo on dataset")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run benchmark suite")
    args = parser.parse_args()

    if args.benchmark:
        run_all_benchmarks()
    elif args.demo:
        path_map = {
            "small": "data/sample_small.json",
            "medium": "data/sample_medium.json",
            "large": "data/sample_large.json",
        }
        run_pipeline(path_map[args.demo])
    else:
        # Default to demo on small dataset first if not interactive, or interactive if terminal
        interactive_menu()
