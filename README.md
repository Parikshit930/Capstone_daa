# Mini-Courier Planner: Algorithmic Optimization Engine
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations | Semester III  
**Institution:** K.R. Mangalam University, Gurugram  
**Faculty Evaluator:** Dr. Shweta Agarwal  
**Assessment:** Coding-Based Capstone Assignment (100 Marks, Scaled to 10 Marks)  

---

## 🚀 Overview

The **Mini-Courier Planner** is an integrated Python application that simulates an intelligent logistics and dispatch system. Given a collection of packages with varying weights, urgency deadlines, and priority scores, along with a city road network graph, the system:
1. **Prioritizes Parcels** using **Merge Sort** and **Quick Sort** ($O(n \log n)$).
2. **Optimizes Vehicle Loading** using **0/1 Knapsack Dynamic Programming** ($O(n \cdot W)$).
3. **Calculates True Shortest Paths** on road graphs using **Dijkstra's Algorithm** with a Min-Heap ($O((V+E)\log V)$).
4. **Sequences Delivery Stops** into a minimal-cost round trip using **Nearest-Neighbor TSP Heuristic** & **2-Opt Local Search** ($O(k^2)$).
5. **Benchmarks Empirical Runtimes** and renders graphical performance curves across varying dataset sizes.

---

## 📁 Project Structure

```
Capstone/
├── data/
│   ├── sample_small.json       # 6 nodes, 8 parcels (ideal for viva manual tracing)
│   ├── sample_medium.json      # 15 nodes, 25 parcels (intermediate dataset)
│   └── sample_large.json       # 50 nodes, 100 parcels (stress-test dataset)
├── src/
│   ├── __init__.py             # Package exports
│   ├── models.py               # Parcel and DeliveryGraph data models
│   ├── sorting.py              # Divide-and-Conquer Merge Sort & Quick Sort
│   ├── knapsack.py             # 0/1 Knapsack DP + Table visualization + Greedy baseline
│   ├── shortest_path.py        # Dijkstra's Algorithm with Min-Heap & Path Reconstruction
│   └── tsp_route.py            # Nearest-Neighbor TSP approximation & 2-Opt Optimizer
├── tests/
│   ├── __init__.py
│   └── test_planner.py         # 11 automated unit tests verifying algorithm correctness
├── benchmark.py                # Benchmarking suite & Matplotlib chart generator
├── main.py                     # Interactive CLI & Automated Demo runner
├── performance_charts.png      # High-resolution runtime comparison charts
├── REPORT.md                   # Full academic report meeting Phase 1-5 rubric criteria
├── VIVA_PREP.md                # Complete Viva Voce Q&A and code tracing guide
└── README.md                   # Project documentation
```

---

## 🛠️ Installation & Setup

Ensure Python 3.9+ is installed.

```bash
# Clone the repository (or extract the zip file)
git clone <repo-link>
cd Capstone

# Install required dependencies for charts (only matplotlib is needed)
pip install matplotlib
```

---

## 🚦 How to Run

### 1. Automated Demonstration (Recommended for Viva)
Runs the entire pipeline start-to-finish on the small dataset, printing the full Dynamic Programming table, selected parcels, Dijkstra distances, and turn-by-turn route:
```bash
python main.py --demo small
```
*(You can also use `--demo medium` or `--demo large`)*.

### 2. Interactive CLI Menu
Launches an interactive menu to test individual phases, switch datasets, or inspect data structures:
```bash
python main.py
```

### 3. Run Automated Unit Tests (11/11 Correctness Verification)
```bash
python -m unittest discover tests
```

### 4. Run Benchmarks & Generate Runtime Charts
Executes tests across input sizes ($N = 10$ to $N = 2000$) and generates `performance_charts.png`:
```bash
python benchmark.py
```

---

## 📊 Sample Execution Trace

```
================================================================================
  RUNNING END-TO-END PIPELINE ON: data/sample_small.json
================================================================================

[PHASE 1] COURIER PROBLEM DESIGN & DATA MODELING
• Central Dispatch Depot : D0
• Vehicle Max Payload    : 15 kg
• Road Network Vertices  : 6 locations
• Total Parcels Received : 8 parcels

[PHASE 2] PACKAGE PRIORITIZATION & BOX FILLING
1. Sorting Parcels by Earliest Deadline First...
   Rank 1: P105 (Deadline 1.0h, Priority 5, 2kg) -> C5
   Rank 2: P102 (Deadline 1.5h, Priority 10, 5kg) -> C2
   ...
2. Dynamic Programming Table:
   Item / W        0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
   --------------------------------------------------------------------------------------------
   Base (0)        0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0
   P105(w=2,v=5)   0    0    5    5    5    5    5    5    5    5    5    5    5    5    5    5
   ...
   P107(w=7,v=11)  0    0    5    7    8   12   13   15   18   20   22   24   26   28   30   32

   Optimal Packing Plan: 4 parcels loaded | 15 kg / 15 kg (100% capacity) | Total Priority: 32
   (DP achieved 6.7% higher payoff than Greedy heuristic)

[PHASE 3] ROUTE MAKER & GRAPH PROCESSING
1. Dijkstra Shortest Distances from Depot D0:
   D0 -> C1: 5.0 km | D0 -> C4: 12.0 km | D0 -> C5: 14.0 km
2. Final Delivery Tour Sequence (Round Trip):
   D0 -> C1 -> C4 -> C5 -> D0
   Total Distance: 31.00 km
   Leg 1: D0 -> C1 (5.0 km) via [D0 -> C1]
   Leg 2: C1 -> C4 (7.0 km) via [C1 -> C2 -> C4]
   Leg 3: C4 -> C5 (5.0 km) via [C4 -> C5]
   Leg 4: C5 -> D0 (14.0 km) via [C5 -> D0]
```

---

## 📈 Complexity Analysis

| Phase / Component | Algorithm | Time Complexity | Space Complexity |
|---|---|---|---|
| **Phase 2: Sorting** | Merge Sort / Quick Sort | $O(n \log n)$ | $O(n)$ / $O(\log n)$ |
| **Phase 2: Packing** | 0/1 Knapsack DP | $O(n \cdot W)$ | $O(n \cdot W)$ |
| **Phase 3: Shortest Path**| Dijkstra (Min-Heap) | $O((V+E)\log V)$ | $O(V)$ |
| **Phase 3: Route Sequence**| Nearest Neighbor TSP | $O(k^2)$ | $O(k)$ |
| **Phase 3: Tour Refinement**| 2-Opt Local Search | $O(k^2)$ per pass | $O(k)$ |

---

## 📚 Viva Voce & Demonstration Resources
Refer to [VIVA_PREP.md](file:///e:/SEMESTER-3/Design%20analysis/Capstone/VIVA_PREP.md) for expected viva questions, step-by-step mathematical tracing, code modifications, and complexity proofs.
Refer to [REPORT.md](file:///e:/SEMESTER-3/Design%20analysis/Capstone/REPORT.md) for the detailed capstone assignment submission report.
