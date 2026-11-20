"""
test_planner.py
Comprehensive unit test suite for the Mini-Courier Planner Capstone Project.
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

import unittest
from src.models import Parcel, DeliveryGraph
from src.sorting import merge_sort, quick_sort, prioritize_parcels
from src.knapsack import solve_01_knapsack, greedy_knapsack_heuristic
from src.shortest_path import dijkstra_shortest_path, reconstruct_path, compute_all_pairs_shortest_paths
from src.tsp_route import nearest_neighbor_tsp, two_opt_optimize


class TestSortingAlgorithms(unittest.TestCase):

    def setUp(self):
        self.parcels = [
            Parcel("P1", "Alice", "C1", weight=5, priority=10, deadline_hours=3.0),
            Parcel("P2", "Bob", "C2", weight=3, priority=15, deadline_hours=1.5),
            Parcel("P3", "Charlie", "C3", weight=2, priority=8, deadline_hours=1.5),
            Parcel("P4", "Dave", "C4", weight=6, priority=12, deadline_hours=4.0),
        ]

    def test_merge_sort_numbers(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        sorted_arr = merge_sort(arr)
        self.assertEqual(sorted_arr, [11, 12, 22, 25, 34, 64, 90])

    def test_quick_sort_numbers(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        sorted_arr = quick_sort(arr)
        self.assertEqual(sorted_arr, [11, 12, 22, 25, 34, 64, 90])

    def test_prioritize_parcels_merge_sort(self):
        # Earliest deadline first; if tied, highest priority first.
        # P2 has deadline 1.5, pri 15
        # P3 has deadline 1.5, pri 8 -> P2 comes before P3
        # P1 has deadline 3.0
        # P4 has deadline 4.0
        res = prioritize_parcels(self.parcels, algorithm="merge_sort")
        expected_ids = ["P2", "P3", "P1", "P4"]
        self.assertEqual([p.id for p in res], expected_ids)

    def test_prioritize_parcels_quick_sort(self):
        res = prioritize_parcels(self.parcels, algorithm="quick_sort")
        expected_ids = ["P2", "P3", "P1", "P4"]
        self.assertEqual([p.id for p in res], expected_ids)

    def test_empty_and_single_element(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(merge_sort([42]), [42])
        self.assertEqual(quick_sort([42]), [42])


class TestKnapsackDP(unittest.TestCase):

    def test_textbook_knapsack(self):
        # Classical test case: weights=[1, 2, 5, 6, 7], values=[1, 6, 18, 22, 28], cap=11
        parcels = [
            Parcel("A", "C1", "Dest", weight=1, priority=1, deadline_hours=1),
            Parcel("B", "C2", "Dest", weight=2, priority=6, deadline_hours=1),
            Parcel("C", "C3", "Dest", weight=5, priority=18, deadline_hours=1),
            Parcel("D", "C4", "Dest", weight=6, priority=22, deadline_hours=1),
            Parcel("E", "C5", "Dest", weight=7, priority=28, deadline_hours=1),
        ]
        result = solve_01_knapsack(parcels, capacity=11)
        # Optimal: B(wt=2, val=6) + C(wt=5, val=18) + D(wt=6) is 13 wt (over cap).
        # Optimal: B (2) + E (7) + A (1) = 10wt, val=35 or C(5)+D(6)=11wt, val=40!
        self.assertEqual(result.max_value, 40)
        self.assertEqual(result.total_weight, 11)
        self.assertEqual([p.id for p in result.selected_parcels], ["C", "D"])

    def test_zero_capacity(self):
        parcels = [Parcel("A", "C1", "Dest", weight=2, priority=5, deadline_hours=1)]
        res = solve_01_knapsack(parcels, capacity=0)
        self.assertEqual(res.max_value, 0)
        self.assertEqual(len(res.selected_parcels), 0)

    def test_greedy_vs_dp(self):
        # Case where Greedy (value/weight) fails for 0/1 knapsack:
        # Item 1: wt=10, val=60 (ratio 6.0)
        # Item 2: wt=20, val=100 (ratio 5.0)
        # Item 3: wt=30, val=120 (ratio 4.0)
        # Capacity = 50.
        # Greedy picks Item 1 (10kg, 60val), Item 2 (20kg, 100val) -> total wt 30, val 160.
        # DP picks Item 2 (20kg) + Item 3 (30kg) -> total wt 50, val 220!
        parcels = [
            Parcel("I1", "C1", "Dest", weight=10, priority=60, deadline_hours=1),
            Parcel("I2", "C2", "Dest", weight=20, priority=100, deadline_hours=1),
            Parcel("I3", "C3", "Dest", weight=30, priority=120, deadline_hours=1),
        ]
        dp_res = solve_01_knapsack(parcels, capacity=50)
        gr_val, gr_wt, _ = greedy_knapsack_heuristic(parcels, capacity=50)
        self.assertEqual(dp_res.max_value, 220)
        self.assertEqual(gr_val, 160)
        self.assertGreater(dp_res.max_value, gr_val)


class TestGraphAndDijkstra(unittest.TestCase):

    def setUp(self):
        self.graph = DeliveryGraph(is_directed=False)
        # Triangle with shortcut
        # A - 2 - B - 3 - C
        # A ----- 6 ----- C
        self.graph.add_edge("A", "B", 2.0)
        self.graph.add_edge("B", "C", 3.0)
        self.graph.add_edge("A", "C", 6.0)

    def test_dijkstra_shortest_path(self):
        distances, predecessors = dijkstra_shortest_path(self.graph, "A")
        self.assertEqual(distances["C"], 5.0) # A -> B -> C = 5.0 < 6.0
        path = reconstruct_path(predecessors, "C")
        self.assertEqual(path, ["A", "B", "C"])

    def test_all_pairs_shortest_paths(self):
        dist_mat, path_mat = compute_all_pairs_shortest_paths(self.graph, ["A", "B", "C"])
        self.assertEqual(dist_mat[("A", "C")], 5.0)
        self.assertEqual(dist_mat[("C", "A")], 5.0)
        self.assertEqual(path_mat[("A", "C")], ["A", "B", "C"])


class TestTSPRouting(unittest.TestCase):

    def test_nearest_neighbor_and_two_opt(self):
        # 4 nodes on a square:
        # D0 (0,0), N1 (0,2), N2 (2,2), N3 (2,0)
        # Distances:
        graph = DeliveryGraph(is_directed=False)
        graph.add_edge("D0", "N1", 2.0)
        graph.add_edge("N1", "N2", 2.0)
        graph.add_edge("N2", "N3", 2.0)
        graph.add_edge("N3", "D0", 2.0)
        # Diagonals
        graph.add_edge("D0", "N2", 3.0)
        graph.add_edge("N1", "N3", 3.0)

        dist_mat, path_mat = compute_all_pairs_shortest_paths(graph)
        stops = ["N1", "N2", "N3"]
        plan = nearest_neighbor_tsp("D0", stops, dist_mat, path_mat)

        self.assertEqual(plan.stop_sequence[0], "D0")
        self.assertEqual(plan.stop_sequence[-1], "D0")
        self.assertEqual(set(plan.stop_sequence), {"D0", "N1", "N2", "N3"})
        self.assertGreater(plan.total_distance, 0)

        # 2-opt check
        opt_plan = two_opt_optimize(plan, dist_mat, path_mat)
        self.assertLessEqual(opt_plan.total_distance, plan.total_distance)


if __name__ == "__main__":
    unittest.main()
