# Mini-Courier Planner: Viva Voce & Demonstration Guide
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Evaluator:** Dr. Shweta Agarwal | Department of CSE, K.R. Mangalam University

This guide prepares you for any question asked during your Capstone demonstration and viva.

---

## 1. Core Algorithm Explanations (How Each Algorithm Works)

### Q1. Explain the working of Merge Sort and why it was selected.
* **Explanation:** Merge Sort uses the **Divide-and-Conquer** paradigm:
  1. **Divide:** Recursively split the array of parcels into two halves until subarrays contain $\le 1$ element.
  2. **Conquer:** Subarrays of size 1 are trivially sorted.
  3. **Combine (Merge):** Two sorted subarrays are systematically merged by comparing elements and picking the smaller one.
* **Why Selected:** It provides a strict **guarantee of $O(n \log n)$ time complexity** in all cases (best, average, worst) and is **stable** (preserves relative arrival order of parcels with identical deadlines and priorities).

### Q2. Explain the working of 0/1 Knapsack Dynamic Programming.
* **Explanation:**
  * Uses a 2D matrix `dp[i][w]` where $i$ is the number of parcels considered ($0 \dots n$) and $w$ is the vehicle carrying weight ($0 \dots W$).
  * For parcel $i-1$ with weight $w_i$ and priority $v_i$:
    * If $w_i > w$, the item cannot fit: `dp[i][w] = dp[i-1][w]`.
    * If $w_i \le w$, choose the maximum of:
      1. Excluding the parcel: `dp[i-1][w]`
      2. Including the parcel: `dp[i-1][w - w_i] + v_i`
  * Backtracking: Starting at `dp[n][W]`, if `dp[i][w] != dp[i-1][w]`, parcel $i-1$ was included; subtract $w_i$ from $w$ and step to row $i-1$.

### Q3. Explain Dijkstra’s Algorithm and how the Min-Heap optimizes it.
* **Explanation:**
  * Solves Single-Source Shortest Path (SSSP) on weighted graphs with non-negative edge weights.
  * Maintains a distance array initialized to $\infty$, except $dist[source] = 0$.
  * Uses a **Min-Heap (Priority Queue)** to always extract the vertex $u$ with the minimum tentative distance in $O(\log V)$ time.
  * For each neighbor $v$ of $u$, **relaxation** is performed:
    $$\text{if } dist[u] + weight(u, v) < dist[v] \implies dist[v] = dist[u] + weight(u, v)$$
  * Overall time complexity is $O((V + E) \log V)$ instead of $O(V^2)$ with an un-indexed array.

### Q4. Explain the Nearest Neighbor TSP heuristic.
* **Explanation:**
  * TSP is NP-Hard. For delivery routing, we use a greedy Nearest Neighbor approximation.
  * Start at Depot `D0`. At every step, look at the set of unvisited delivery stops and pick the stop with the smallest shortest-path distance (from Dijkstra).
  * Mark it visited, append to route, and repeat until all customer stops are visited.
  * Finally, connect the last stop back to `D0` to complete the round-trip cycle.
  * Time complexity: $O(k^2)$ where $k$ is the number of delivery stops.

---

## 2. Algorithm Tracing (Walkthrough on Sample Dataset)

### Tracing 0/1 Knapsack on Whiteboard / Viva
Given vehicle capacity $W = 15\text{ kg}$ and prioritized parcels:
* $P105$: $w=2, v=5$
* $P102$: $w=5, v=10$
* $P104$: $w=6, v=12$
* $P101$: $w=3, v=7$
* $P106$: $w=4, v=8$

**Trace Row by Row:**
1. **Row 1 ($P105, w=2, v=5$):** For $w < 2$, value is 0. For $w \ge 2$, value is 5.
2. **Row 2 ($P102, w=5, v=10$):** At $w=7$, $\max(dp[1][7], dp[1][7-5] + 10) = \max(5, 5 + 10) = 15$.
3. **Row 3 ($P104, w=6, v=12$):** At $w=13$, $\max(dp[2][13], dp[2][13-6] + 12) = \max(15, 15 + 12) = 27$.
4. **Row 5 ($P106, w=4, v=8$):** At $w=15$, $\max(dp[4][15], dp[4][15-4] + 8) = \max(29, 24 + 8) = 32$.
* **Backtracking from `dp[5][15] = 32`:**
  * Row 5 ($P106$): $dp[5][15] (32) \ne dp[4][15] (29) \implies$ **Include P106** ($w=4$). Remaining weight = $15 - 4 = 11$.
  * Row 4 ($P101$): $dp[4][11] (24) \ne dp[3][11] (22) \implies$ **Include P101** ($w=3$). Remaining weight = $11 - 3 = 8$.
  * Row 3 ($P104$): $dp[3][8] (17) \ne dp[2][8] (15) \implies$ **Include P104** ($w=6$). Remaining weight = $8 - 6 = 2$.
  * Row 2 ($P102$): $dp[2][2] (5) == dp[1][2] (5) \implies$ **Exclude P102**.
  * Row 1 ($P105$): $dp[1][2] (5) \ne dp[0][2] (0) \implies$ **Include P105** ($w=2$). Remaining weight = $2 - 2 = 0$.
* **Resulting Items:** `P105, P104, P101, P106`. Total Weight = 15kg, Total Priority = 32.

---

## 3. Comparative Analysis & Blooms L5 Questions

### Q5. Why does Greedy (Value/Weight ratio) fail for 0/1 Knapsack?
* **Answer:** Greedy works for **Fractional Knapsack** (where items can be split), but fails for **0/1 Knapsack** because leaving unused capacity can result in lower total value.
* **Counterexample in our tests:**
  * Item A: $w=10, v=60$ (ratio 6.0)
  * Item B: $w=20, v=100$ (ratio 5.0)
  * Item C: $w=30, v=120$ (ratio 4.0)
  * Capacity = 50.
  * **Greedy** picks Item A (10kg) and Item B (20kg) = total wt 30kg, **value = 160**.
  * **DP** picks Item B (20kg) and Item C (30kg) = total wt 50kg, **value = 220**.

### Q6. Compare Merge Sort vs Quick Sort in this project.
* **Merge Sort:**
  * Guaranteed $O(n \log n)$ worst-case.
  * Stable (preserves order of tied deadlines).
  * Requires $O(n)$ extra memory for merging.
* **Quick Sort:**
  * Average $O(n \log n)$, but worst-case $O(n^2)$ if pivot choice is poor.
  * Not inherently stable.
  * Faster in practice due to cache locality and minimal memory overhead ($O(\log n)$ recursion stack).

### Q7. Why can't we use Dijkstra for graphs with negative edge weights?
* **Answer:** Dijkstra is a greedy algorithm that assumes that once a vertex is extracted from the priority queue, its shortest distance is finalized. A negative edge could later reduce the distance of an already finalized vertex, breaking the greedy invariant. (For negative edge weights, Bellman-Ford must be used). In road networks, distance is always non-negative ($w \ge 0$).

---

## 4. Live Code Modifications You May Be Asked to Perform

### Modification 1: "Change priority policy to sort by highest priority first, and deadline only as tie-breaker."
* **Where to modify:** `src/sorting.py` in `prioritize_parcels()`:
  ```python
  # Change from:
  key = lambda p: (p.deadline_hours, -p.priority)
  # To:
  key = lambda p: (-p.priority, p.deadline_hours)
  ```

### Modification 2: "Reduce vehicle capacity from 15 to 10 kg."
* **In CLI:** Run `python main.py` and choose the small dataset, or open `data/sample_small.json` and change `"vehicle_capacity_kg": 10`.

### Modification 3: "Add a new road or customer location."
* Open `data/sample_small.json`, add node `{ "id": "C6", "label": "New Market" }` to `nodes`, and add edges to `edges`.

---

## 5. Quick Demonstration Commands

```bash
# 1. Run unit tests to prove correctness (11/11 tests)
python -m unittest discover tests

# 2. Run automated demo on small dataset (with DP table output)
python main.py --demo small

# 3. Run interactive menu
python main.py

# 4. Run benchmarks and re-generate runtime charts
python benchmark.py
```
