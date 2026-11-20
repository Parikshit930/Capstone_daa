# Capstone Project Report: Mini-Courier Planner
**Course Title & Code:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme & Semester:** B.Tech CSE & Specializations, Semester III  
**Institution:** K.R. Mangalam University, Gurugram, Haryana  
**Faculty Evaluator:** Dr. Shweta Agarwal  
**Assessment Type:** Coding-based Capstone Project (100 Marks, Scaled to 10 Marks)  
**Mapped Course Outcomes (COs):** CO1, CO2, CO3, CO4 (Blooms Level L5: Evaluate / Create)

---

## Executive Summary

The **Mini-Courier Planner** is an integrated algorithmic solution developed to solve the end-to-end dispatch, package prioritization, vehicle payload optimization, and routing challenge faced by modern logistics providers. By uniting four classical pillars of algorithmic design—**Divide-and-Conquer**, **Dynamic Programming**, **Greedy Graph Traversal**, and **Approximation Heuristics**—this prototype maximizes delivery utility, respects courier vehicle constraints, and minimizes transit mileage.

---

## Phase 1: Courier Problem Design and Planning (20 Marks)

### 1.1 Problem Formulation
A courier dispatch depot receives $N$ parcels destined for various customer locations across a metropolitan road network. Each parcel $p_i$ is characterized by:
* $id$: Unique parcel identifier (e.g., `P101`).
* $customer\_name$: Consignee name.
* $destination$: Destination vertex $v \in V$ on the city road graph.
* $weight$ ($w_i$): Package mass in integer kilograms.
* $priority$ ($v_i$): Delivery importance score ($1 \le v_i \le 20$).
* $deadline$ ($d_i$): Delivery SLA deadline in hours from dispatch ($d_i > 0$).

The delivery fleet consists of delivery vehicles with a fixed carrying capacity of $W$ kilograms. The central depot $D_0$ is located at a designated vertex on a weighted undirected road graph $G = (V, E)$, where edge weight $w(u, v) \ge 0$ represents physical road distance in kilometers.

### 1.2 System Architecture & Algorithmic Pipeline
The planner operates in four sequential algorithmic stages:

```
+-----------------------------------------------------------------------------------+
|                        MINI-COURIER PLANNER ARCHITECTURE                          |
+-----------------------------------------------------------------------------------+
  [Parcels Pool] + [Road Graph G=(V,E)] + [Vehicle Capacity W]
                         │
                         ▼
  [STAGE 1: PRIORITIZATION]
  Algorithm: Merge Sort / Quick Sort (Divide & Conquer)
  Policy   : Earliest Deadline First (EDF), Tie-break: Highest Priority
  Complexity: O(n log n) time, O(n) space
                         │
                         ▼
  [STAGE 2: VEHICLE PAYLOAD OPTIMIZATION]
  Algorithm: 0/1 Knapsack (Dynamic Programming)
  Objective: Maximize total priority sum subject to sum(w_i) <= W
  Complexity: O(n * W) pseudo-polynomial time, O(n * W) space
                         │
                         ▼
  [STAGE 3: SHORTEST PATH CALCULATION]
  Algorithm: Dijkstra's Algorithm with Min-Heap
  Target   : Compute all-pairs shortest distances between Depot and Selected Stops
  Complexity: O((V + E) log V) time, O(V) space
                         │
                         ▼
  [STAGE 4: ROUTE ORDERING & OPTIMIZATION]
  Algorithm: Nearest Neighbor TSP Approximation + 2-Opt Local Search
  Output   : Closed round-trip tour D0 -> C_a -> C_b -> ... -> D0
  Complexity: O(k^2) time where k is number of delivery stops
```

---

## Phase 2: Package Prioritization and Box Filling (20 Marks)

### 2.1 Package Prioritization (Divide-and-Conquer Sorting)
Parcels are sorted according to urgency:
$$\text{key}(p_i) = (d_i, -v_i)$$

* **Merge Sort**: Recursively divides the array into two halves ($T(n) = 2T(n/2) + O(n)$), sorts each half, and merges them. It guarantees strict $O(n \log n)$ worst-case time complexity and is **stable**, preserving the arrival order of parcels with identical deadlines and priorities.
* **Quick Sort**: Uses a median-of-three pivot selection ($low, mid, high$) to partition the array in-place. Offers $O(n \log n)$ average-case performance with low constant overhead.

### 2.2 Vehicle Box Filling (0/1 Knapsack Dynamic Programming)
Because a parcel cannot be fractionally divided (either loaded completely or left for the next trip), the greedy strategy based on value-to-weight ratio is sub-optimal. Dynamic Programming guarantees mathematical optimality.

#### Recurrence Relation:
Let $DP[i][w]$ denote the maximum priority achievable considering the first $i$ prioritized parcels with weight limit $w$:

$$DP[i][w] = \begin{cases} 
      0 & \text{if } i = 0 \text{ or } w = 0 \\
      DP[i-1][w] & \text{if } w_i > w \\
      \max\Big(DP[i-1][w], \; DP[i-1][w - w_i] + v_i\Big) & \text{if } w_i \le w 
   \end{cases}$$

#### DP Table Evidence (Small Dataset: $W=15$ kg, 8 Parcels):
```
Item / W        0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
--------------------------------------------------------------------------------------------
Base (0)        0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0
P105(w=2,v=5)   0    0    5    5    5    5    5    5    5    5    5    5    5    5    5    5
P102(w=5,v=10)  0    0    5    5    5   10   10   15   15   15   15   15   15   15   15   15
P104(w=6,v=12)  0    0    5    5    5   10   12   15   17   17   17   22   22   27   27   27
P101(w=3,v=7)   0    0    5    7    7   12   12   15   17   19   22   24   24   27   29   29
P106(w=4,v=8)   0    0    5    7    8   12   13   15   17   20   22   24   25   27   30   32
P108(w=3,v=6)   0    0    5    7    8   12   13   15   18   20   22   24   26   28   30   32
P103(w=4,v=6)   0    0    5    7    8   12   13   15   18   20   22   24   26   28   30   32
P107(w=7,v=11)  0    0    5    7    8   12   13   15   18   20   22   24   26   28   30   32
```
* **Optimal Value:** 32 points
* **Selected Parcels Backtracked:** `P105` (2kg, 5v), `P104` (6kg, 12v), `P101` (3kg, 7v), `P106` (4kg, 8v).
* **Total Weight Loaded:** $2 + 6 + 3 + 4 = 15$ kg (100% capacity utilization).
* **Comparison with Greedy:** Greedy selected ratio order yielding value = 30. DP achieved a **6.7% higher payoff**.

---

## Phase 3: Route Maker and Graph Processing (20 Marks)

### 3.1 Road Network Graph Representation
The physical network is represented as an Adjacency List:
$$G = (V, E, W)$$
Where $V$ consists of Depot `D0` and Customer delivery hubs `C1` to `C5`. Non-negative road distance $w(u, v)$ enables shortest path routing.

### 3.2 Dijkstra's Algorithm
Single-source shortest path is computed from `D0` using a priority queue (min-heap):
* **Heap Operations:** Extracted minimum vertex in $O(\log V)$.
* **Relaxation:** For each neighbor $v$ of $u$, if $dist[u] + w(u,v) < dist[v]$, update $dist[v]$ and push $(dist[v], v)$ into heap.
* **Results from D0:**
  * `D0 -> C1`: 5.0 km
  * `D0 -> C2`: 9.0 km (via `C1`)
  * `D0 -> C3`: 8.0 km
  * `D0 -> C4`: 12.0 km (via `C1 -> C2 -> C4`)
  * `D0 -> C5`: 14.0 km

### 3.3 Nearest Neighbor TSP Approximation & 2-Opt Local Search
The courier must visit unique destinations of loaded packages $\{C1, C4, C5\}$ and return to `D0`.
* **Nearest Neighbor Algorithm:**
  1. Start at `D0`.
  2. Closest unvisited node: `C1` ($dist = 5.0$ km).
  3. From `C1`, closest unvisited: `C4` ($dist = 7.0$ km via `C2`).
  4. From `C4`, closest unvisited: `C5` ($dist = 5.0$ km).
  5. Return to `D0` from `C5` ($dist = 14.0$ km).
* **Final Tour:**
  $$\text{D0} \longrightarrow \text{C1} \longrightarrow \text{C4} \longrightarrow \text{C5} \longrightarrow \text{D0}$$
* **Total Round-Trip Distance:** $5.0 + 7.0 + 5.0 + 14.0 = \mathbf{31.00\text{ km}}$
* **Turn-by-turn road trajectory:**
  * Leg 1: `D0 -> C1` (5.0 km)
  * Leg 2: `C1 -> C2 -> C4` (7.0 km)
  * Leg 3: `C4 -> C5` (5.0 km)
  * Leg 4: `C5 -> D0` (14.0 km)

---

## Phase 4: Performance Testing & Asymptotic Analysis (20 Marks)

### 4.1 Theoretical Complexity Summary

| Component | Algorithm Employed | Paradigm | Time Complexity (Best / Avg / Worst) | Space Complexity |
|---|---|---|---|---|
| **Prioritization** | Merge Sort | Divide & Conquer | $\Theta(n \log n) \;/\; \Theta(n \log n) \;/\; \Theta(n \log n)$ | $O(n)$ |
| **Prioritization** | Quick Sort | Divide & Conquer | $O(n \log n) \;/\; O(n \log n) \;/\; O(n^2)$ | $O(\log n)$ |
| **Vehicle Packing** | 0/1 Knapsack DP | Dynamic Programming | $\Theta(n \cdot W) \;/\; \Theta(n \cdot W) \;/\; \Theta(n \cdot W)$ | $O(n \cdot W)$ |
| **Shortest Paths** | Dijkstra (Min-Heap) | Greedy Graph | $O((V+E)\log V)$ | $O(V + E)$ |
| **Tour Construction** | Nearest-Neighbor TSP | Greedy Approximation | $\Theta(k^2)$ | $O(k)$ |
| **Tour Refinement** | 2-Opt Local Search | Local Search Heuristic| $O(k^2)$ per pass | $O(k)$ |

*Note: $n$ = parcels, $W$ = vehicle capacity, $V$ = graph vertices, $E$ = edges, $k$ = unique delivery stops.*

### 4.2 Empirical Benchmarking Results
Benchmarks executed on Python 3.14 on Windows across scaling input sizes:

#### 1. Sorting Runtimes (ms):
| Input Size ($N$) | Merge Sort (ms) | Quick Sort (ms) | Python Timsort (ms) |
|---|---|---|---|
| 10 | 0.0184 | 0.0147 | 0.0020 |
| 50 | 0.0668 | 0.0463 | 0.0154 |
| 100 | 0.1443 | 0.1049 | 0.0150 |
| 500 | 0.8849 | 0.7786 | 0.1093 |
| 1000 | 2.0000 | 1.4254 | 0.1976 |
| 2000 | 5.9549 | 2.9135 | 0.4213 |

#### 2. Knapsack Runtimes (ms) ($W = 2N$):
| Number of Items ($N$) | Capacity ($W$) | 0/1 Knapsack DP (ms) | Greedy Heuristic (ms) |
|---|---|---|---|
| 10 | 20 | 0.0292 | 0.0049 |
| 50 | 100 | 0.3460 | 0.0140 |
| 100 | 200 | 1.5104 | 0.0538 |
| 250 | 500 | 9.9780 | 0.2789 |
| 400 | 800 | 27.4189 | 1.0033 |

#### 3. Dijkstra & TSP Runtimes (ms):
* Graph Vertices $V=10$: 0.0255 ms $\rightarrow$ $V=800$: 0.9077 ms.
* TSP Delivery Stops $k=5$: 0.0264 ms $\rightarrow$ $k=500$: 33.3520 ms.

*All graphical runtime plots are compiled in `performance_charts.png`.*

### 4.3 Proposed Future Optimizations
1. **Space Optimization for 0/1 Knapsack:** If only the optimal value is needed, space can be reduced from $O(n \cdot W)$ to $O(W)$ using a 1D array traversed backwards.
2. **Multi-Vehicle VRP (Vehicle Routing Problem):** Extend single-vehicle TSP to a fleet of heterogeneous vehicles using Clarke-Wright Savings heuristic.
3. **A* Search for Target Routing:** In large sparse graphs with Euclidean coordinates, replacing Dijkstra with $A^*$ and Euclidean heuristic reduces explored search states.

---

## Phase 5: Verification and Conclusion (20 Marks)

The Mini-Courier Planner completely fulfills all evaluation parameters:
* **Correctness:** 11/11 automated unit tests passing covering corner cases (0 capacity, disconnected nodes, identical keys, single-element arrays).
* **Modular Codebase:** Clean segregation into `src/models.py`, `src/sorting.py`, `src/knapsack.py`, `src/shortest_path.py`, and `src/tsp_route.py`.
* **Execution Options:** Provides interactive menu CLI as well as one-command automated evaluation scripts.
