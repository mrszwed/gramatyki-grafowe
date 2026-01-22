import os
import sys

from productions.p0.p0 import P0
from productions.p1.p1 import P1
from productions.p2.p2 import P2
from productions.p3.p3 import P3
from productions.p4.p4 import P4
from productions.p5.p5 import P5
from productions.p6.p6 import P6
from productions.p7.p7 import P7

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p8.p8 import P8

output_dir = "./wywod7_examples"
os.makedirs(output_dir, exist_ok=True)

graph = HyperGraph()
# ============================================================
# CENTRAL RECTANGLE
# ============================================================
q1 = graph.add_node(0, 0)
q2 = graph.add_node(2, 0)
q3 = graph.add_node(2, 1)
q4 = graph.add_node(0, 1)


graph.add_edge(q1, q2, is_border=False)
graph.add_edge(q2, q3, is_border=False)
graph.add_edge(q3, q4, is_border=False)
graph.add_edge(q4, q1, is_border=False)

center_quad = graph.add_hyperedge([q1, q2, q3, q4], label="Q")

# graph.visualize(os.path.join(output_dir, "center_quad.png"))


# # ============================================================
# # LEFT: HEXAGON
# # ============================================================
h2 = q4
h1 = q1
h3 = graph.add_node(-1.0, 2.0)
h4 = graph.add_node(-2.0, 1.0)
h5 = graph.add_node(-2.0, 0.0)
h6 = graph.add_node(-1.0, -1.0)


hex_nodes = [h1, h2, h3, h4, h5, h6]

graph.add_edge(h1, h2, is_border=False)
graph.add_edge(h2, h3, is_border=False)
graph.add_edge(h3, h4, is_border=True)
graph.add_edge(h4, h5, is_border=True)
graph.add_edge(h5, h6, is_border=True)
graph.add_edge(h6, h1, is_border=False)

hexagon = graph.add_hyperedge(hex_nodes, label="S")
# graph.visualize(os.path.join(output_dir, "left_hexagon.png"))

# # ============================================================
# # TOP: QUADLITERAL RHOMBUS
# # ============================================================
t1 = q4
t2 = q3
t3 = graph.add_node(3.0, 2.0)
t4 = h3

graph.add_edge(t2, t3, is_border=False)
graph.add_edge(t3, t4, is_border=True)

top_rhombus = graph.add_hyperedge([t1, t2, t3, t4], label="Q")
# graph.visualize(os.path.join(output_dir, "top_rhombus.png"))

# # ============================================================
# # BOTTOM: QUADLITERAL RHOMBUS
# # ============================================================
b1 = q1
b2 = q2
b3 = graph.add_node(3.0, -1.0)
b4 = h6

graph.add_edge(b2, b3, is_border=False)
graph.add_edge(b3, b4, is_border=True)

bottom_rhombus = graph.add_hyperedge([b1, b2, b3, b4], label="Q")
# graph.visualize(os.path.join(output_dir, "bottom_rhombus.png"))

# # ============================================================
# # RIGHT: PENTAGON
# # ============================================================
p1 = q2
p2 = q3
p3 = t3 #góra
p4 = graph.add_node(5.0, 0.5) #prawo
p5 = b3 # dół

pent_nodes = [p1, p2, p3, p4, p5]

graph.add_edge(p3, p4, is_border=True)
graph.add_edge(p4, p5, is_border=True)

pentagon = graph.add_hyperedge(pent_nodes, label="P")


# graph.visualize(os.path.join(output_dir, "whole_graph_before.png"))

# # ============================================================
# PRODUCTIONS
# # ============================================================

def apply_productions(productions):
    for prod in productions:
        can_apply, matched = prod.can_apply(graph)
        if can_apply:
            prod.apply(graph, matched)
        else:
            print(f"[Whole graph] Production {prod.__class__.__name__} cannot be applied.")


# productions1=[P6(), P7(), P4(), P4(), P4(), P4(), P4()]
# apply_productions(productions1)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_1.png"))
#
# productions2=[P8()]
# apply_productions(productions2)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_2.png"))
#
# productions3=[P0(),P1(),P1(), P4(), P4(), P4(), P4()]
# apply_productions(productions3)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_3.png"))

graph.visualize(os.path.join(output_dir, "whole_graph_0.png"))

productions1=[P6(), P0()]
apply_productions(productions1)
graph.visualize(os.path.join(output_dir, "whole_graph_after_1.png"))

productions2=[P7()]
apply_productions(productions2)
graph.visualize(os.path.join(output_dir, "whole_graph_after_2.png"))

productions3=[P4(), P4()]
apply_productions(productions3)
graph.visualize(os.path.join(output_dir, "whole_graph_after_3.png"))

productions4=[P3(), P3(), P3()]
apply_productions(productions4)
graph.visualize(os.path.join(output_dir, "whole_graph_after_4.png"))

productions5=[P8()]
apply_productions(productions5)
graph.visualize(os.path.join(output_dir, "whole_graph_after_5.png"))

productions6=[P1()]
apply_productions(productions6)
graph.visualize(os.path.join(output_dir, "whole_graph_after_6.png"))

productions7=[P2()]
apply_productions(productions7)
graph.visualize(os.path.join(output_dir, "whole_graph_after_7.png"))

productions8=[P3(), P3(), P3()]
apply_productions(productions8)
graph.visualize(os.path.join(output_dir, "whole_graph_after_8.png"))

productions9=[P5()]
apply_productions(productions9)
graph.visualize(os.path.join(output_dir, "whole_graph_after_9.png"))

#==================

# productions6=[P0(), P1()]
# apply_productions(productions6)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_10.png"))
#
# productions7=[P2()]
# apply_productions(productions7)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_11.png"))
#
# productions8=[P3(), P3(), P3()]
# apply_productions(productions8)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_12.png"))
#
# productions9=[P5()]
# apply_productions(productions9)
# graph.visualize(os.path.join(output_dir, "whole_graph_after_13.png"))