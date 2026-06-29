import networkx as nx
import matplotlib.pyplot as plt


class NetworkXStore:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, name, node_type):
        """
        Add a node only if it doesn't already exist.
        """
        if not self.graph.has_node(name):
            self.graph.add_node(
                name,
                type=node_type
            )

    def add_relationship(
        self,
        source,
        source_type,
        relationship,
        target,
        target_type
    ):
        """
        Add a relationship between two nodes.
        """

        self.add_node(source, source_type)
        self.add_node(target, target_type)

        self.graph.add_edge(
            source,
            target,
            relationship=relationship
        )

    def print_graph(self):
        """
        Print all nodes and relationships.
        """

        print("\n===== NODES =====\n")

        for node, data in self.graph.nodes(data=True):
            print(f"{node} -> {data}")

        print("\n===== RELATIONSHIPS =====\n")

        for source, target, data in self.graph.edges(data=True):
            print(
                f"{source} --[{data['relationship']}]--> {target}"
            )

    def visualize_graph(self):
        """
        Save graph as PNG.
        """

        plt.figure(figsize=(18, 12))

        pos = nx.spring_layout(
            self.graph,
            seed=42
        )

        nx.draw_networkx_nodes(
            self.graph,
            pos,
            node_size=3000
        )

        nx.draw_networkx_labels(
            self.graph,
            pos,
            font_size=8
        )

        nx.draw_networkx_edges(
            self.graph,
            pos,
            arrows=True
        )

        edge_labels = nx.get_edge_attributes(
            self.graph,
            "relationship"
        )

        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels
        )

        plt.axis("off")

        plt.savefig("knowledge_graph.png")

        print("\n✅ knowledge_graph.png saved")

        plt.show()

    # -------------------------------------------------------
    # Query Helpers
    # -------------------------------------------------------

    def get_nodes_by_type(self, node_type):
        """
        Return all nodes of a given type.
        """

        return [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("type") == node_type
        ]

    def get_neighbors(self, node_name, relationship=None):
        """
        Return outgoing neighbors.
        """

        results = []

        if not self.graph.has_node(node_name):
            return results

        for _, target, data in self.graph.out_edges(node_name, data=True):

            if relationship is None or data.get("relationship") == relationship:
                results.append(target)

        return results

    def get_predecessors(self, node_name, relationship=None):
        """
        Return incoming neighbors.
        """

        results = []

        if not self.graph.has_node(node_name):
            return results

        for source, _, data in self.graph.in_edges(node_name, data=True):

            if relationship is None or data.get("relationship") == relationship:
                results.append(source)

        return results

    def get_targets(self, source, relationship):
        """
        Return:
        source --[relationship]--> target
        """

        targets = []

        if not self.graph.has_node(source):
            return targets

        for _, target, data in self.graph.out_edges(source, data=True):

            if data.get("relationship") == relationship:
                targets.append(target)

        return targets

    def get_sources(self, target, relationship):
        """
        Return:
        source --[relationship]--> target
        """

        sources = []

        if not self.graph.has_node(target):
            return sources

        for source, _, data in self.graph.in_edges(target, data=True):

            if data.get("relationship") == relationship:
                sources.append(source)

        return sources