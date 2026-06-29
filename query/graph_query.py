import difflib


class GraphQuery:

    def __init__(self, graph):
        self.graph = graph

    # =========================
    # SMART NODE MATCHING
    # =========================
    def _best_match(self, name):
        nodes = list(self.graph.graph.nodes())
        matches = difflib.get_close_matches(name, nodes, n=1, cutoff=0.5)
        return matches[0] if matches else name

    # =========================
    # DEPARTMENT LOOKUP
    # Department → MANAGES → Scheme
    # =========================
    def find_department(self, scheme):

        scheme = self._best_match(scheme)

        departments = []

        for source, target, data in self.graph.graph.in_edges(scheme, data=True):
            if data.get("relationship") == "MANAGES":
                departments.append(source)

        return list(set(departments))

    # =========================
    # BENEFICIARY LOOKUP
    # Scheme → BENEFITS → Beneficiary
    # =========================
    def find_beneficiaries(self, scheme):

        scheme = self._best_match(scheme)

        beneficiaries = []

        for _, target, data in self.graph.graph.out_edges(scheme, data=True):
            if data.get("relationship") == "BENEFITS":
                beneficiaries.append(target)

        return list(set(beneficiaries))

    # =========================
    # SCHEME CONTEXT BUILDER (IMPROVED)
    # =========================
    def build_context_for_scheme(self, scheme):

        scheme = self._best_match(scheme)

        departments = self.find_department(scheme)
        beneficiaries = self.find_beneficiaries(scheme)

        # also get direct connections for better LLM grounding
        outgoing = []
        incoming = []

        for _, tgt, data in self.graph.graph.out_edges(scheme, data=True):
            outgoing.append(f"{scheme} → {data['relationship']} → {tgt}")

        for src, _, data in self.graph.graph.in_edges(scheme, data=True):
            incoming.append(f"{src} → {data['relationship']} → {scheme}")

        context = f"""
SCHEME:
{scheme}

DEPARTMENTS:
{", ".join(departments) if departments else "Not found"}

BENEFICIARIES:
{", ".join(beneficiaries) if beneficiaries else "Not found"}

RELATIONSHIPS (OUTGOING):
{chr(10).join(outgoing) if outgoing else "None"}

RELATIONSHIPS (INCOMING):
{chr(10).join(incoming) if incoming else "None"}
"""

        return context.strip()

    # =========================
    # GENERIC QUERY ROUTER (OPTIONAL BUT USEFUL)
    # =========================
    def answer_question(self, question):

        q = question.lower()

        # detect scheme name from question
        nodes = list(self.graph.graph.nodes())

        matched = None
        for n in nodes:
            if n.lower() in q:
                matched = n
                break

        if not matched:
            matched = self._best_match(question)

        departments = self.find_department(matched)
        beneficiaries = self.find_beneficiaries(matched)

        return {
            "scheme": matched,
            "departments": departments,
            "beneficiaries": beneficiaries
        }