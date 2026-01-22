import os
import sys
import math

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p8.p8 import P8

output_dir = "./productions/p8/outputs"
os.makedirs(output_dir, exist_ok=True)

production = P8()


def regular_pentagon(radius=1.0, center=(0, 0)):
    cx, cy = center
    return [
        (
            cx + radius * math.cos(2 * math.pi * i / 5),
            cy + radius * math.sin(2 * math.pi * i / 5)
        )
        for i in range(5)
    ]


# ============================================================
# Test 1: Simple regular pentagon
# ============================================================
graph1 = HyperGraph()

coords = regular_pentagon(radius=2.0)
nodes = [graph1.add_node(x, y) for x, y in coords]

mid_nodes = []
for i in range(5):
    a = nodes[i]
    b = nodes[(i + 1) % 5]
    m = graph1.add_node((a.x + b.x) / 2, (a.y + b.y) / 2)
    mid_nodes.append(m)

    graph1.add_edge(a, m, is_border=True)
    graph1.add_edge(m, b, is_border=True)

pent = graph1.add_hyperedge(nodes, label="P")
pent.R = 1

graph1.visualize(os.path.join(output_dir, "example_p8_pentagon_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)
else:
    print("[Simple pentagon] Production P8 cannot be applied.")

graph1.visualize(os.path.join(output_dir, "example_p8_pentagon_after.png"))


# ============================================================
# Test 2: Pentagon embedded in larger structure
# ============================================================
graph2 = HyperGraph()

coords = regular_pentagon(radius=2.0)
nodes = [graph2.add_node(x, y) for x, y in coords]

mid_nodes = []
for i in range(5):
    a = nodes[i]
    b = nodes[(i + 1) % 5]
    m = graph2.add_node((a.x + b.x) / 2, (a.y + b.y) / 2)
    mid_nodes.append(m)

    graph2.add_edge(a, m, is_border=True)
    graph2.add_edge(m, b, is_border=True)

pent2 = graph2.add_hyperedge(nodes, label="P")
pent2.R = 1

# Extra quadrilateral
nq1 = graph2.add_node(3, 0)
nq2 = graph2.add_node(3.5, -0.5)
graph2.add_edge(mid_nodes[0], nq1, is_border=True)
graph2.add_edge(nq1, nq2, is_border=True)
graph2.add_edge(nq2, nodes[0], is_border=True)
graph2.add_hyperedge([mid_nodes[0], nq1, nq2, nodes[0]], label="Q")

graph2.visualize(os.path.join(output_dir, "example_p8_embedded_before.png"))

can_apply, matched = production.can_apply(graph2)
if can_apply:
    production.apply(graph2, matched)
else:
    print("[Embedded pentagon] Production P8 cannot be applied.")

graph2.visualize(os.path.join(output_dir, "example_p8_embedded_after.png"))


# ============================================================
# Test 3: Two pentagons marked for refinement
# ============================================================
graph3 = HyperGraph()

coords1 = regular_pentagon(radius=2.0, center=(0, 0))
nodes1 = [graph3.add_node(x, y) for x, y in coords1]

mid1 = []
for i in range(5):
    a = nodes1[i]
    b = nodes1[(i + 1) % 5]
    m = graph3.add_node((a.x + b.x) / 2, (a.y + b.y) / 2)
    mid1.append(m)
    graph3.add_edge(a, m)
    graph3.add_edge(m, b)

h1 = graph3.add_hyperedge(nodes1, label="P")
h1.R = 1

coords2 = regular_pentagon(radius=2.0, center=(5, 0))
nodes2 = [graph3.add_node(x, y) for x, y in coords2]

mid2 = []
for i in range(5):
    a = nodes2[i]
    b = nodes2[(i + 1) % 5]
    m = graph3.add_node((a.x + b.x) / 2, (a.y + b.y) / 2)
    mid2.append(m)
    graph3.add_edge(a, m)
    graph3.add_edge(m, b)

h2 = graph3.add_hyperedge(nodes2, label="P")
h2.R = 1

graph3.visualize(os.path.join(output_dir, "example_p8_two_pentagons_before.png"))

for i in range(2):
    can_apply, matched = production.can_apply(graph3)
    if can_apply:
        production.apply(graph3, matched)
    else:
        print("[Two pentagons] Production P8 cannot be applied.")

    graph3.visualize(
        os.path.join(output_dir, f"example_p8_two_pentagons_after_{i+1}.png")
    )


# ============================================================
# Test 4: Irregular (ugly) pentagon
# ============================================================
graph4 = HyperGraph()

coords = [
    (0, 0),
    (2, 0.5),
    (1.5, 3),
    (-0.5, 4),
    (-1.5, 1.5)
]

nodes = [graph4.add_node(x, y) for x, y in coords]

mid = []
for i in range(5):
    a = nodes[i]
    b = nodes[(i + 1) % 5]
    m = graph4.add_node((a.x + b.x) / 2, (a.y + b.y) / 2)
    mid.append(m)

    graph4.add_edge(a, m, is_border=True)
    graph4.add_edge(m, b, is_border=True)

pent4 = graph4.add_hyperedge(nodes, label="P")
pent4.R = 1

graph4.visualize(os.path.join(output_dir, "example_p8_ugly_pentagon_before.png"))

can_apply, matched = production.can_apply(graph4)
if can_apply:
    production.apply(graph4, matched)
else:
    print("[Ugly pentagon] Production P8 cannot be applied.")

graph4.visualize(os.path.join(output_dir, "example_p8_ugly_pentagon_after.png"))
