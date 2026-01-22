from productions.production_base import Production


class P8(Production):
    """
    Production P8: Break the pentagonal element marked for refinement,
    if all its edges are broken.
    It sets value of attribute R of new hyperedges with label Q to 0.
    """

    def __init__(self):
        super().__init__(
            name="P8",
            description="Break the pentagonal element marked for refinement, if all its edges are broken."
        )

    def _get_node_between(self, graph, node1, node2, desired_R=None):
        """
        Find and return a node between node1 and node2 (hanging node).
        """
        for node in graph.nodes:
            if node == node1 or node == node2:
                continue

            edge1 = graph.get_edge_between(node1, node)
            edge2 = graph.get_edge_between(node, node2)

            if not edge1 or not edge2:
                continue

            if desired_R is None or (edge1.R == desired_R and edge2.R == desired_R):
                return node

        return None

    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """
        Check if P8 can be applied to the graph.
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        if hyperedge and not refinement_criterion:
            return False, None

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            # --- PENTAGON CHECK ---
            if edge.label != "P" or len(edge.nodes) != 5:
                continue

            if edge.R != 1:
                continue

            nodes = edge.nodes
            nodes_found = []
            edges_found = []

            for i in range(5):
                nodeA = nodes[i]
                nodeB = nodes[(i + 1) % 5]
                nodes_found.append(nodeA)

                # hanging node between A and B
                nodeC = self._get_node_between(graph, nodeA, nodeB, desired_R=0)
                if not nodeC:
                    break

                nodes_found.append(nodeC)

                edgeAC = graph.get_edge_between(nodeA, nodeC)
                edgeCB = graph.get_edge_between(nodeC, nodeB)

                if not edgeAC or not edgeCB:
                    break

                edges_found.append(edgeAC)
                edges_found.append(edgeCB)

            # 5 narożników + 5 wiszących = 10
            if len(nodes_found) == 10 and len(edges_found) == 10:
                return True, {
                    "hyperedge": edge,
                    "nodes": nodes_found,   # even = corners, odd = hanging
                    "edges": edges_found
                }

        return False, None

    def apply(self, graph, matched_elements):
        """
        Apply P8 to break the pentagonal element.
        """
        pent_hyperedge = matched_elements["hyperedge"]
        pent_nodes = matched_elements["nodes"]

        new_quadrilaterals = []

        # indices of original pentagon vertices
        convex_hull_indices = [i for i in range(0, len(pent_nodes), 2)]
        assert len(convex_hull_indices) == 5, "There should be 5 corner nodes."

        # I. Create central node
        new_node = graph.add_node(
            x=sum(pent_nodes[i].x for i in convex_hull_indices) / 5,
            y=sum(pent_nodes[i].y for i in convex_hull_indices) / 5,
            label="V"
        )

        # II. Create 5 quadrilateral hyperedges
        for i in range(5):
            corner_idx = i * 2

            n1 = new_node
            n2 = pent_nodes[(corner_idx - 1) % 10]   # previous hanging
            n3 = pent_nodes[corner_idx]              # corner
            n4 = pent_nodes[(corner_idx + 1) % 10]   # next hanging

            quad = graph.add_hyperedge(
                nodes=[n1, n2, n3, n4],
                label="Q"
            )
            quad.R = 0
            new_quadrilaterals.append(quad)

        # III. Connect central node with hanging nodes
        for i in range(5):
            hanging_idx = i * 2 + 1
            graph.add_edge(
                new_node,
                pent_nodes[hanging_idx],
                is_border=False,
                label="E"
            )

        # IV. Remove original pentagon
        graph.remove_edge(pent_hyperedge)

        print(f"[{self.name}] Broken pentagonal hyperedge into 5 quadrilateral hyperedges.")
        print(f"[{self.name}] Hyperedge {pent_hyperedge} removed.")

        return {
            "central_node": new_node,
            "quadrilaterals": new_quadrilaterals
        }
