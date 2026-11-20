"""
sorting.py
Implementation of Divide-and-Conquer Sorting Algorithms:
1. Merge Sort (Guaranteed O(n log n), Stable)
2. Quick Sort (Average O(n log n), Partition-based)
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

from typing import List, Callable, Any, Tuple
from src.models import Parcel


def default_parcel_key(parcel: Parcel) -> Tuple[float, int]:
    """
    Default prioritization policy:
    1. Earliest deadline first (ascending order of deadline_hours)
    2. Highest priority first (descending order of priority, hence -priority)
    """
    return (parcel.deadline_hours, -parcel.priority)


# ---------------------------------------------------------------------------
# MERGE SORT
# ---------------------------------------------------------------------------
def merge_sort(
    arr: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> List[Any]:
    """
    Stable Divide-and-Conquer Merge Sort.
    Time Complexity: Best = Average = Worst = O(n log n)
    Space Complexity: O(n) auxiliary space
    """
    if len(arr) <= 1:
        return list(arr)

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key, reverse=reverse)
    right = merge_sort(arr[mid:], key=key, reverse=reverse)

    return _merge(left, right, key=key, reverse=reverse)


def _merge(
    left: List[Any],
    right: List[Any],
    key: Callable[[Any], Any],
    reverse: bool
) -> List[Any]:
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key(left[i])
        right_val = key(right[j])

        # If reverse=False: take smaller first (ascending). If True: take larger first.
        condition = (left_val <= right_val) if not reverse else (left_val >= right_val)

        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ---------------------------------------------------------------------------
# QUICK SORT
# ---------------------------------------------------------------------------
def quick_sort(
    arr: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> List[Any]:
    """
    Divide-and-Conquer Quick Sort (Median-of-three pivot selection).
    Time Complexity:
      - Best / Average: O(n log n)
      - Worst: O(n^2) (mitigated by median-of-three pivot selection)
    Space Complexity: O(log n) call stack space
    """
    arr_copy = list(arr)
    _quick_sort_helper(arr_copy, 0, len(arr_copy) - 1, key=key, reverse=reverse)
    return arr_copy


def _quick_sort_helper(
    arr: List[Any],
    low: int,
    high: int,
    key: Callable[[Any], Any],
    reverse: bool
) -> None:
    if low < high:
        p_index = _partition(arr, low, high, key=key, reverse=reverse)
        _quick_sort_helper(arr, low, p_index - 1, key=key, reverse=reverse)
        _quick_sort_helper(arr, p_index + 1, high, key=key, reverse=reverse)


def _partition(
    arr: List[Any],
    low: int,
    high: int,
    key: Callable[[Any], Any],
    reverse: bool
) -> int:
    # Median-of-three pivot selection to prevent worst-case O(n^2) on sorted inputs
    mid = (low + high) // 2
    candidates = [
        (key(arr[low]), low),
        (key(arr[mid]), mid),
        (key(arr[high]), high),
    ]
    candidates.sort(key=lambda item: item[0])
    pivot_idx = candidates[1][1]

    # Swap chosen pivot with high
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]

    pivot_val = key(arr[high])
    i = low - 1

    for j in range(low, high):
        val_j = key(arr[j])
        condition = (val_j <= pivot_val) if not reverse else (val_j >= pivot_val)
        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def prioritize_parcels(
    parcels: List[Parcel],
    algorithm: str = "merge_sort",
    criterion: str = "deadline_and_priority"
) -> List[Parcel]:
    """
    Wrapper to prioritize parcels using a specified algorithm and criterion.
    Criteria:
      - 'deadline_and_priority': earliest deadline first, tie-break by highest priority.
      - 'priority_only': highest priority first.
      - 'deadline_only': earliest deadline first.
    """
    if criterion == "deadline_and_priority":
        key = lambda p: (p.deadline_hours, -p.priority)
    elif criterion == "priority_only":
        key = lambda p: -p.priority
    elif criterion == "deadline_only":
        key = lambda p: p.deadline_hours
    else:
        raise ValueError(f"Unknown criterion: {criterion}")

    if algorithm == "merge_sort":
        return merge_sort(parcels, key=key)
    elif algorithm == "quick_sort":
        return quick_sort(parcels, key=key)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}. Use 'merge_sort' or 'quick_sort'.")
