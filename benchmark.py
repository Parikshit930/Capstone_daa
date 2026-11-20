"""
benchmark.py
Performance Benchmarking Suite & Runtime Analysis for Mini-Courier Planner.
Generates performance metrics tables and high-resolution matplotlib charts.
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

import time
import random
import matplotlib.pyplot as plt
from typing import List, Dict, Any

from src.models import Parcel, DeliveryGraph
from src.sorting import merge_sort, quick_sort
from src.knapsack import solve_01_knapsack, greedy_knapsack_heuristic
from src.shortest_path import dijkstra_shortest_path
from src.tsp_route import nearest_neighbor_tsp


def generate_synthetic_parcels(n: int, seed: int = 42) -> List[Parcel]:
    random.seed(seed)
    parcels = []
    for i in range(n):
        parcels.append(Parcel(
            id=f"P{i}",
            customer_name=f"Cust_{i}",
            destination=f"Loc_{random.randint(1, max(1, n // 5))}",
            weight=random.randint(1, 15),
            priority=random.randint(1, 20),
            deadline_hours=round(random.uniform(0.5, 12.0), 2)
        ))
    return parcels


def generate_synthetic_graph(v: int, edge_factor: int = 3, seed: int = 42) -> DeliveryGraph:
    random.seed(seed)
    g = DeliveryGraph(is_directed=False)
    # Ensure connectivity
    for i in range(1, v):
        parent = random.randint(0, i - 1)
        g.add_edge(f"N{parent}", f"N{i}", round(random.uniform(2.0, 25.0), 1))
    
    # Extra edges
    for _ in range(v * edge_factor):
        u = f"N{random.randint(0, v - 1)}"
        w = f"N{random.randint(0, v - 1)}"
        if u != w:
            g.add_edge(u, w, round(random.uniform(2.0, 30.0), 1))
    return g


def benchmark_sorting(sizes: List[int]) -> Dict[str, List[float]]:
    results = {"merge_sort": [], "quick_sort": [], "builtin_timsort": []}
    key_func = lambda p: (p.deadline_hours, -p.priority)

    for n in sizes:
        parcels = generate_synthetic_parcels(n)
        
        # Merge Sort
        t0 = time.perf_counter()
        _ = merge_sort(parcels, key=key_func)
        results["merge_sort"].append((time.perf_counter() - t0) * 1000)

        # Quick Sort
        t0 = time.perf_counter()
        _ = quick_sort(parcels, key=key_func)
        results["quick_sort"].append((time.perf_counter() - t0) * 1000)

        # Builtin Timsort
        t0 = time.perf_counter()
        _ = sorted(parcels, key=key_func)
        results["builtin_timsort"].append((time.perf_counter() - t0) * 1000)

    return results


def benchmark_knapsack(sizes: List[int], capacity_multiplier: int = 2) -> Dict[str, List[float]]:
    results = {"dp_01_knapsack": [], "greedy_heuristic": []}

    for n in sizes:
        parcels = generate_synthetic_parcels(n)
        cap = n * capacity_multiplier

        # DP
        t0 = time.perf_counter()
        _ = solve_01_knapsack(parcels, capacity=cap)
        results["dp_01_knapsack"].append((time.perf_counter() - t0) * 1000)

        # Greedy
        t0 = time.perf_counter()
        _ = greedy_knapsack_heuristic(parcels, capacity=cap)
        results["greedy_heuristic"].append((time.perf_counter() - t0) * 1000)

    return results


def benchmark_dijkstra(vertex_counts: List[int]) -> List[float]:
    times = []
    for v in vertex_counts:
        g = generate_synthetic_graph(v)
        t0 = time.perf_counter()
        _ = dijkstra_shortest_path(g, "N0")
        times.append((time.perf_counter() - t0) * 1000)
    return times


def benchmark_tsp(stop_counts: List[int]) -> List[float]:
    times = []
    for k in stop_counts:
        stops = [f"N{i}" for i in range(1, k + 1)]
        all_nodes = ["D0"] + stops
        # Mock complete metric distance matrix
        random.seed(k)
        dist_mat = {}
        path_mat = {}
        for u in all_nodes:
            for v in all_nodes:
                d = 0.0 if u == v else random.uniform(5.0, 50.0)
                dist_mat[(u, v)] = d
                path_mat[(u, v)] = [u, v]
        
        t0 = time.perf_counter()
        _ = nearest_neighbor_tsp("D0", stops, dist_mat, path_mat)
        times.append((time.perf_counter() - t0) * 1000)
    return times


def run_all_benchmarks():
    print("=" * 70)
    print("  RUNNING MINI-COURIER PLANNER BENCHMARKS (PHASE 4)")
    print("=" * 70)

    sort_sizes = [10, 50, 100, 250, 500, 1000, 2000]
    knap_sizes = [10, 25, 50, 100, 150, 250, 400]
    graph_sizes = [10, 25, 50, 100, 200, 400, 800]
    tsp_sizes = [5, 15, 30, 60, 120, 250, 500]

    print("\n1. Benchmarking Sorting Algorithms...")
    sort_res = benchmark_sorting(sort_sizes)
    print(f"{'N':<8}{'MergeSort (ms)':<18}{'QuickSort (ms)':<18}{'Timsort (ms)':<18}")
    print("-" * 62)
    for i, n in enumerate(sort_sizes):
        print(f"{n:<8}{sort_res['merge_sort'][i]:<18.4f}{sort_res['quick_sort'][i]:<18.4f}{sort_res['builtin_timsort'][i]:<18.4f}")

    print("\n2. Benchmarking 0/1 Knapsack (DP vs Greedy)...")
    knap_res = benchmark_knapsack(knap_sizes)
    print(f"{'N Items':<10}{'Capacity W':<14}{'DP 0/1 (ms)':<18}{'Greedy (ms)':<18}")
    print("-" * 60)
    for i, n in enumerate(knap_sizes):
        cap = n * 2
        print(f"{n:<10}{cap:<14}{knap_res['dp_01_knapsack'][i]:<18.4f}{knap_res['greedy_heuristic'][i]:<18.4f}")

    print("\n3. Benchmarking Dijkstra Shortest Path...")
    dijk_times = benchmark_dijkstra(graph_sizes)
    print(f"{'Vertices (|V|)':<18}{'Dijkstra (ms)':<18}")
    print("-" * 36)
    for i, v in enumerate(graph_sizes):
        print(f"{v:<18}{dijk_times[i]:<18.4f}")

    print("\n4. Benchmarking Nearest Neighbor TSP Route Planner...")
    tsp_times = benchmark_tsp(tsp_sizes)
    print(f"{'Stops (k)':<18}{'NN-TSP (ms)':<18}")
    print("-" * 36)
    for i, k in enumerate(tsp_sizes):
        print(f"{k:<18}{tsp_times[i]:<18.4f}")

    # Generate Matplotlib plots
    print("\nGenerating performance plots -> performance_charts.png ...")
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Mini-Courier Planner: Algorithm Performance Analysis (ETCCDA302)", fontsize=16, fontweight="bold")

    # Plot 1: Sorting
    axs[0, 0].plot(sort_sizes, sort_res["merge_sort"], "o-", label="Merge Sort O(n log n)", color="#2b5c8f")
    axs[0, 0].plot(sort_sizes, sort_res["quick_sort"], "s-", label="Quick Sort O(n log n)", color="#d95f02")
    axs[0, 0].plot(sort_sizes, sort_res["builtin_timsort"], "^--", label="Built-in Timsort", color="#7570b3")
    axs[0, 0].set_title("1. Sorting Algorithms Runtime Comparison")
    axs[0, 0].set_xlabel("Number of Parcels (N)")
    axs[0, 0].set_ylabel("Execution Time (ms)")
    axs[0, 0].grid(True, linestyle="--", alpha=0.6)
    axs[0, 0].legend()

    # Plot 2: Knapsack
    axs[0, 1].plot(knap_sizes, knap_res["dp_01_knapsack"], "o-", label="DP 0/1 Knapsack O(n·W)", color="#e7298a")
    axs[0, 1].plot(knap_sizes, knap_res["greedy_heuristic"], "s--", label="Greedy Heuristic O(n log n)", color="#66a61e")
    axs[0, 1].set_title("2. 0/1 Knapsack: DP vs Greedy Runtime")
    axs[0, 1].set_xlabel("Number of Parcels (N) [W = 2N]")
    axs[0, 1].set_ylabel("Execution Time (ms)")
    axs[0, 1].grid(True, linestyle="--", alpha=0.6)
    axs[0, 1].legend()

    # Plot 3: Dijkstra
    axs[1, 0].plot(graph_sizes, dijk_times, "o-", label="Dijkstra Min-Heap O((V+E) log V)", color="#1b9e77")
    axs[1, 0].set_title("3. Dijkstra Single-Source Shortest Path")
    axs[1, 0].set_xlabel("Number of Vertices (|V|)")
    axs[1, 0].set_ylabel("Execution Time (ms)")
    axs[1, 0].grid(True, linestyle="--", alpha=0.6)
    axs[1, 0].legend()

    # Plot 4: TSP
    axs[1, 1].plot(tsp_sizes, tsp_times, "o-", label="Nearest Neighbor TSP O(k²)", color="#e6ab02")
    axs[1, 1].set_title("4. Nearest Neighbor TSP Heuristic")
    axs[1, 1].set_xlabel("Number of Delivery Stops (k)")
    axs[1, 1].set_ylabel("Execution Time (ms)")
    axs[1, 1].grid(True, linestyle="--", alpha=0.6)
    axs[1, 1].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("performance_charts.png", dpi=300)
    print("Performance charts saved successfully as 'performance_charts.png'!")


if __name__ == "__main__":
    run_all_benchmarks()
