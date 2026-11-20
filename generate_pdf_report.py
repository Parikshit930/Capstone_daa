"""
generate_pdf_report.py
Generates a publication-grade, professional PDF report for the Capstone Assignment.
Course: Design & Analysis of Algorithms (ETCCDA302)
Institution: K.R. Mangalam University
"""

import os
import pymupdf


def create_capstone_pdf():
    pdf_filename = "Mini_Courier_Planner_Capstone_Report.pdf"
    img_path = os.path.abspath("performance_charts.png").replace("\\", "/")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
        }}
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            color: #2c3e50;
            line-height: 1.45;
            font-size: 10pt;
        }}
        .header-box {{
            background-color: #1a365d;
            color: #ffffff;
            padding: 18px 20px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        .univ-title {{
            font-size: 16pt;
            font-weight: bold;
            letter-spacing: 0.5px;
            margin: 0 0 4px 0;
            text-transform: uppercase;
        }}
        .sub-title {{
            font-size: 11pt;
            color: #cbd5e0;
            margin: 0 0 10px 0;
        }}
        .report-title {{
            font-size: 14pt;
            font-weight: bold;
            color: #f6ad55;
            margin: 10px 0 0 0;
            border-top: 1px solid #4a5568;
            padding-top: 8px;
        }}
        .meta-grid {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 18px;
            font-size: 9pt;
        }}
        .meta-grid td {{
            padding: 5px 8px;
            border: 1px solid #e2e8f0;
        }}
        .meta-lbl {{
            background-color: #edf2f7;
            font-weight: bold;
            width: 25%;
            color: #2d3748;
        }}
        .meta-val {{
            width: 25%;
            color: #4a5568;
        }}
        h2 {{
            color: #1a365d;
            font-size: 12pt;
            border-bottom: 2px solid #2b6cb0;
            padding-bottom: 4px;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        h3 {{
            color: #2b6cb0;
            font-size: 10.5pt;
            margin-top: 12px;
            margin-bottom: 6px;
        }}
        p {{
            margin: 0 0 8px 0;
            text-align: justify;
        }}
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 14px 0;
            font-size: 8.5pt;
        }}
        table.data-table th {{
            background-color: #2b6cb0;
            color: #ffffff;
            font-weight: bold;
            padding: 6px 6px;
            border: 1px solid #cbd5e0;
            text-align: left;
        }}
        table.data-table td {{
            padding: 5px 6px;
            border: 1px solid #e2e8f0;
        }}
        table.data-table tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        .dp-matrix {{
            font-family: 'Courier New', monospace;
            font-size: 7.5pt;
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 8px;
            white-space: pre;
            line-height: 1.25;
            margin: 8px 0;
            border-radius: 4px;
            overflow-x: auto;
        }}
        .highlight-box {{
            background-color: #ebf8ff;
            border-left: 4px solid #3182ce;
            padding: 8px 12px;
            margin: 10px 0;
            font-size: 9pt;
        }}
        .success-badge {{
            color: #22543d;
            background-color: #c6f6d5;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 8.5pt;
        }}
        .page-break {{
            page-break-before: always;
        }}
        .chart-container {{
            text-align: center;
            margin: 12px 0;
        }}
        .chart-img {{
            width: 95%;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
        }}
    </style>
    </head>
    <body>

    <div class="header-box">
        <div class="univ-title">K.R. Mangalam University, Gurugram</div>
        <div class="sub-title">School of Engineering & Technology | Department of Computer Science & Engineering</div>
        <div class="report-title">CAPSTONE ASSIGNMENT REPORT: MINI-COURIER PLANNER</div>
    </div>

    <table class="meta-grid">
        <tr>
            <td class="meta-lbl">Student Name</td>
            <td class="meta-val"><b>Parikshit Chauhan</b></td>
            <td class="meta-lbl">Roll Number</td>
            <td class="meta-val"><b>2501730398</b></td>
        </tr>
        <tr>
            <td class="meta-lbl">Course Title & Code</td>
            <td class="meta-val">Design & Analysis of Algorithms (ETCCDA302)</td>
            <td class="meta-lbl">Faculty Evaluator</td>
            <td class="meta-val">Dr. Shweta Agarwal</td>
        </tr>
        <tr>
            <td class="meta-lbl">Programme & Semester</td>
            <td class="meta-val">B.Tech CSE & Specializations (Semester III)</td>
            <td class="meta-lbl">Type of Assessment</td>
            <td class="meta-val">Coding-Based Capstone Project</td>
        </tr>
        <tr>
            <td class="meta-lbl">Maximum Marks</td>
            <td class="meta-val">100 Marks (Scaled to 10 Marks)</td>
            <td class="meta-lbl">COs & Blooms Level</td>
            <td class="meta-val">CO1, CO2, CO3, CO4 | Level L5 (Evaluate/Create)</td>
        </tr>
        <tr>
            <td class="meta-lbl">Submission Mode</td>
            <td class="meta-val">Zosima & GitHub Repository</td>
            <td class="meta-lbl">Repository URL</td>
            <td class="meta-val"><a href="https://github.com/Parikshit930/Capstone_daa">github.com/Parikshit930/Capstone_daa</a></td>
        </tr>
    </table>

    <h2>1. Executive Summary & Problem Formulation</h2>
    <p>
        The <b>Mini-Courier Planner</b> is an integrated algorithmic dispatch and route-optimization system engineered in Python. It resolves the dual challenges of courier logistics: <i>optimal parcel packing under vehicle payload restrictions</i> and <i>minimal-distance route ordering across a metropolitan road network</i>.
    </p>
    <p>
        The system unites four foundational algorithmic paradigms covered in the course laboratories:
        <b>Divide-and-Conquer</b> (Merge Sort & Quick Sort), <b>Dynamic Programming</b> (0/1 Knapsack), <b>Greedy Graph Traversal</b> (Dijkstra's Algorithm with Min-Heap), and <b>Approximation Techniques</b> (Nearest Neighbor TSP with 2-Opt Local Search).
    </p>

    <h2>2. Phase 1: Courier Problem Design and Planning (20 Marks)</h2>
    <p>
        <b>Parcel Schema:</b> Each parcel <i>p<sub>i</sub></i> is modeled with six distinct attributes: unique ID, consignee name, destination graph vertex, integer payload weight (kg), priority score (1-20), and deadline SLA (hours).
    </p>
    <table class="data-table">
        <tr>
            <th>Parcel ID</th>
            <th>Customer Name</th>
            <th>Destination Hub</th>
            <th>Weight (kg)</th>
            <th>Priority Score</th>
            <th>Deadline (Hours)</th>
        </tr>
        <tr><td>P101</td><td>Aarav Sharma</td><td>Sector 14 (C1)</td><td>3</td><td>7</td><td>2.5</td></tr>
        <tr><td>P102</td><td>Diya Verma</td><td>Cyber Hub (C2)</td><td>5</td><td>10</td><td>1.5</td></tr>
        <tr><td>P103</td><td>Rohan Gupta</td><td>Sohna Road (C3)</td><td>4</td><td>6</td><td>4.0</td></tr>
        <tr><td>P104</td><td>Ananya Rao</td><td>Golf Course (C4)</td><td>6</td><td>12</td><td>2.0</td></tr>
        <tr><td>P105</td><td>Kabir Mehta</td><td>Old Railway (C5)</td><td>2</td><td>5</td><td>1.0</td></tr>
        <tr><td>P106</td><td>Isha Kapoor</td><td>Sector 14 (C1)</td><td>4</td><td>8</td><td>3.0</td></tr>
        <tr><td>P107</td><td>Vikram Singh</td><td>Cyber Hub (C2)</td><td>7</td><td>11</td><td>5.0</td></tr>
        <tr><td>P108</td><td>Neha Joshi</td><td>Golf Course (C4)</td><td>3</td><td>6</td><td>3.5</td></tr>
    </table>
    <p>
        <b>Road Network Model:</b> Represented as an undirected, non-negatively weighted Adjacency List graph <i>G = (V, E)</i> comprising Central Depot <code>D0</code> and customer nodes <code>C1</code> to <code>C5</code> with physical distances in kilometers.
    </p>

    <div class="page-break"></div>

    <h2>3. Phase 2: Package Prioritization & Box Filling (20 Marks)</h2>
    <h3>3.1 Package Prioritization (Divide-and-Conquer)</h3>
    <p>
        Parcels are prioritized via <b>Merge Sort</b> (guaranteed <i>O(n log n)</i>, stable) using the multi-criteria key <code>(deadline_hours, -priority)</code> (Earliest Deadline First with priority tie-breaker):
    </p>
    <p><b>Priority Sequence:</b> P105 (1.0h) &rarr; P102 (1.5h) &rarr; P104 (2.0h) &rarr; P101 (2.5h) &rarr; P106 (3.0h) &rarr; P108 (3.5h) &rarr; P103 (4.0h) &rarr; P107 (5.0h).</p>

    <h3>3.2 Dynamic Programming (0/1 Knapsack Vehicle Packing)</h3>
    <p>
        Because parcel units cannot be fractionally divided, 0/1 Knapsack Dynamic Programming guarantees mathematical optimality for vehicle capacity <i>W = 15 kg</i>:
    </p>
    <div class="dp-matrix">
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
    </div>
    <div class="highlight-box">
        <b>Packing Optimization Results:</b><br>
        &bull; Selected Parcels: <b>P105, P104, P101, P106</b> (4 parcels)<br>
        &bull; Total Weight Loaded: <b>15 kg / 15 kg (100.0% Payload Utilization)</b><br>
        &bull; Total Priority Score: <b>32 Points</b><br>
        &bull; Algorithm Insight: DP achieved <b>32 points</b> vs Greedy's <b>30 points</b> (a <b>6.7% improvement</b> proving greedy sub-optimality).
    </div>

    <h2>4. Phase 3: Route Maker & Graph Processing (20 Marks)</h2>
    <h3>4.1 Dijkstra's Shortest Path Algorithm (Min-Heap)</h3>
    <table class="data-table">
        <tr>
            <th>Source Vertex</th>
            <th>Target Location</th>
            <th>Shortest Distance</th>
            <th>Optimal Road Path Trajectory</th>
        </tr>
        <tr><td>D0 (Depot)</td><td>Sector 14 (C1)</td><td>5.0 km</td><td>D0 &rarr; C1</td></tr>
        <tr><td>D0 (Depot)</td><td>Cyber Hub (C2)</td><td>9.0 km</td><td>D0 &rarr; C1 &rarr; C2</td></tr>
        <tr><td>D0 (Depot)</td><td>Sohna Road (C3)</td><td>8.0 km</td><td>D0 &rarr; C3</td></tr>
        <tr><td>D0 (Depot)</td><td>Golf Course (C4)</td><td>12.0 km</td><td>D0 &rarr; C1 &rarr; C2 &rarr; C4</td></tr>
        <tr><td>D0 (Depot)</td><td>Old Railway (C5)</td><td>14.0 km</td><td>D0 &rarr; C5</td></tr>
    </table>

    <h3>4.2 Nearest Neighbor TSP Tour & Turn-by-Turn Route</h3>
    <p>
        The delivery vehicle must service destinations &#123;C1, C4, C5&#125; and return to Depot <code>D0</code>:
    </p>
    <div class="highlight-box">
        <b>Final Ordered Delivery Route:</b><br>
        <b>D0 &rarr; C1 &rarr; C4 &rarr; C5 &rarr; D0</b> &nbsp;|&nbsp; <b>Total Route Distance: 31.00 km</b><br><br>
        &bull; <b>Leg 1:</b> D0 &rarr; C1 (5.0 km) via [D0 &rarr; C1]<br>
        &bull; <b>Leg 2:</b> C1 &rarr; C4 (7.0 km) via [C1 &rarr; C2 &rarr; C4]<br>
        &bull; <b>Leg 3:</b> C4 &rarr; C5 (5.0 km) via [C4 &rarr; C5]<br>
        &bull; <b>Leg 4:</b> C5 &rarr; D0 (14.0 km) via [C5 &rarr; D0]
    </div>

    <div class="page-break"></div>

    <h2>5. Phase 4: Performance Testing & Optimization (20 Marks)</h2>
    <h3>5.1 Asymptotic Time & Space Complexity Analysis</h3>
    <table class="data-table">
        <tr>
            <th>Algorithmic Component</th>
            <th>Algorithm Name</th>
            <th>Design Paradigm</th>
            <th>Time Complexity</th>
            <th>Space Complexity</th>
        </tr>
        <tr>
            <td>Parcel Prioritization</td>
            <td>Merge Sort</td>
            <td>Divide & Conquer</td>
            <td>&Theta;(n log n)</td>
            <td>O(n)</td>
        </tr>
        <tr>
            <td>Parcel Prioritization</td>
            <td>Quick Sort</td>
            <td>Divide & Conquer</td>
            <td>O(n log n) avg, O(n&sup2;) worst</td>
            <td>O(log n)</td>
        </tr>
        <tr>
            <td>Box / Vehicle Packing</td>
            <td>0/1 Knapsack DP</td>
            <td>Dynamic Programming</td>
            <td>&Theta;(n &middot; W)</td>
            <td>O(n &middot; W)</td>
        </tr>
        <tr>
            <td>Shortest Path Engine</td>
            <td>Dijkstra (Min-Heap)</td>
            <td>Greedy Graph Traversal</td>
            <td>O((V + E) log V)</td>
            <td>O(V + E)</td>
        </tr>
        <tr>
            <td>Tour Generation</td>
            <td>Nearest-Neighbor TSP</td>
            <td>Approximation Heuristic</td>
            <td>&Theta;(k&sup2;)</td>
            <td>O(k)</td>
        </tr>
        <tr>
            <td>Tour Optimization</td>
            <td>2-Opt Local Search</td>
            <td>Local Improvement</td>
            <td>O(k&sup2;) per pass</td>
            <td>O(k)</td>
        </tr>
    </table>

    <h3>5.2 Empirical Runtime Benchmarks</h3>
    <div class="chart-container">
        <img class="chart-img" src="{img_path}" alt="Algorithm Performance Charts" />
        <p style="font-size: 8pt; color: #718096; margin-top: 4px;">Figure 1: Comparative runtime scalability curves across Sorting, Knapsack, Dijkstra, and TSP.</p>
    </div>

    <h2>6. Phase 5: Verification & Conclusion (20 Marks)</h2>
    <p>
        The complete project has been verified using a comprehensive automated test suite (<code>tests/test_planner.py</code>) with <b>11/11 passing unit tests</b> <span class="success-badge">ALL TESTS PASSED (100%)</span>.
    </p>
    <p>
        The codebase is published openly on GitHub under:
        <br><b>GitHub Repository:</b> <a href="https://github.com/Parikshit930/Capstone_daa">https://github.com/Parikshit930/Capstone_daa</a>
    </p>
    <p>
        <b>Submitted by:</b> Parikshit Chauhan (Roll No: 2501730398) &nbsp;|&nbsp; <b>B.Tech CSE (ETCCDA302)</b> &nbsp;|&nbsp; <b>Evaluator:</b> Dr. Shweta Agarwal &nbsp;|&nbsp; <b>Platform:</b> Zosima
    </p>

    </body>
    </html>
    """

    doc = pymupdf.open()
    story = pymupdf.Story(html=html_content)
    writer = pymupdf.DocumentWriter(pdf_filename)
    rect = pymupdf.paper_rect("a4")

    more = True
    while more:
        device = writer.begin_page(rect)
        more, _ = story.place(rect)
        story.draw(device)
        writer.end_page()

    writer.close()
    print(f"Report PDF successfully generated: {pdf_filename}")


if __name__ == "__main__":
    create_capstone_pdf()
