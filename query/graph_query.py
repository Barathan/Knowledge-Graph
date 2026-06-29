class GraphQuery:

    def __init__(self, graph):
        self.graph = graph

    def find_department(self, scheme):

        return self.graph.get_sources(
            scheme,
            "MANAGES"
        )

    def find_beneficiaries(self, scheme):

        return self.graph.get_targets(
            scheme,
            "BENEFITS"
        )

    def build_context_for_scheme(self, scheme):

        departments = self.find_department(scheme)
        beneficiaries = self.find_beneficiaries(scheme)

        context = f"""
Scheme Name:
{scheme}

Department:
{", ".join(departments)}

Beneficiaries:
{", ".join(beneficiaries)}
"""

        return context.strip()
    
def get_targets(self, source, relationship):
    """
    Return all target nodes for:
    source --[relationship]--> target
    """

    targets = []

    for _, target, data in self.graph.out_edges(source, data=True):
        if data["relationship"] == relationship:
            targets.append(target)

    return targets


def get_sources(self, target, relationship):
    """
    Return all source nodes for:
    source --[relationship]--> target
    """

    sources = []

    for source, _, data in self.graph.in_edges(target, data=True):
        if data["relationship"] == relationship:
            sources.append(source)

    return sources

    def get_targets(self, source, relationship):
        """
        Return all target nodes:
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
        Return all source nodes:
        source --[relationship]--> target
        """

        sources = []

        if not self.graph.has_node(target):
            return sources

        for source, _, data in self.graph.in_edges(target, data=True):
            if data.get("relationship") == relationship:
                sources.append(source)

        return sources