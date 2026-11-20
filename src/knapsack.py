"""
knapsack.py
Implementation of 0/1 Knapsack Dynamic Programming for Box / Vehicle Packing.
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

from typing import List, Tuple, Dict, Any
from src.models import Parcel


class KnapsackResult:
    """Contains the complete result of the Knapsack optimization."""

    def __init__(
        self,
        max_value: int,
        total_weight: int,
        capacity: int,
        selected_parcels: List[Parcel],
        dp_table: List[List[int]],
        parcels_considered: List[Parcel]
    ):
        self.max_value = max_value
        self.total_weight = total_weight
        self.capacity = capacity
        self.selected_parcels = selected_parcels
        self.dp_table = dp_table
        self.parcels_considered = parcels_considered

    def print_dp_table(self, max_cols: int = 15) -> str:
        """
        Formats the DP table into a readable string matrix for reporting & viva evidence.
        Truncates columns if capacity is too large for terminal display.
        """
        lines = []
        n = len(self.parcels_considered)
        w_limit = min(self.capacity + 1, max_cols + 1)

        # Header row
        header = f"{'Item / W':<12}" + "".join(f"{w:>5}" for w in range(w_limit))
        if self.capacity + 1 > w_limit:
            header += "  ... (truncated)"
        lines.append(header)
        lines.append("-" * len(header))

        # Row 0 (0 items)
        row0 = f"{'Base (0)':<12}" + "".join(f"{self.dp_table[0][w]:>5}" for w in range(w_limit))
        lines.append(row0)

        # Subsequent rows
        for i, p in enumerate(self.parcels_considered, start=1):
            lbl = f"{p.id}(w={p.weight},v={p.priority})"
            row_str = f"{lbl:<12}" + "".join(f"{self.dp_table[i][w]:>5}" for w in range(w_limit))
            lines.append(row_str)

        return "\n".join(lines)


def solve_01_knapsack(parcels: List[Parcel], capacity: int) -> KnapsackResult:
    """
    0/1 Knapsack Dynamic Programming solver (Maximizes Priority Value within Weight Capacity).

    Recurrence Relation:
      dp[i][w] = dp[i-1][w]                                    if weight[i-1] > w
      dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i-1]] + val[i-1]) otherwise

    Time Complexity: O(n * W)
    Space Complexity: O(n * W) (to reconstruct the selected items)
    """
    n = len(parcels)
    if capacity <= 0 or n == 0:
        return KnapsackResult(
            max_value=0,
            total_weight=0,
            capacity=capacity,
            selected_parcels=[],
            dp_table=[[0] * (capacity + 1)] if capacity >= 0 else [[]],
            parcels_considered=parcels,
        )

    # Initialize (n + 1) x (capacity + 1) table with 0s
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        p = parcels[i - 1]
        w_i = p.weight
        v_i = p.priority

        for w in range(capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtracking to identify selected parcels
    selected: List[Parcel] = []
    curr_w = capacity
    for i in range(n, 0, -1):
        # If the value came from including item i-1
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            p = parcels[i - 1]
            selected.append(p)
            curr_w -= p.weight

    # Reverse to keep original order
    selected.reverse()
    total_wt = sum(p.weight for p in selected)

    return KnapsackResult(
        max_value=dp[n][capacity],
        total_weight=total_wt,
        capacity=capacity,
        selected_parcels=selected,
        dp_table=dp,
        parcels_considered=parcels,
    )


def greedy_knapsack_heuristic(parcels: List[Parcel], capacity: int) -> Tuple[int, int, List[Parcel]]:
    """
    Greedy approximation using Value-to-Weight ratio (v_i / w_i).
    Useful for comparing against DP in Phase 4 (Demonstrates why Greedy fails for 0/1 Knapsack).
    """
    sorted_parcels = sorted(parcels, key=lambda p: (p.priority / p.weight), reverse=True)
    selected = []
    curr_weight = 0
    total_val = 0

    for p in sorted_parcels:
        if curr_weight + p.weight <= capacity:
            selected.append(p)
            curr_weight += p.weight
            total_val += p.priority

    return total_val, curr_weight, selected
