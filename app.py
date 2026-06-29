import os
from dotenv import load_dotenv

load_dotenv()

from loaders.document_loader import load_html_document
from loaders.text_splitter import split_document

from extraction.entity_extractor import extract_entities
from extraction.relationship_extractor import extract_relationships

from graph.networkx_store import NetworkXStore

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------
from extraction.entity_extractor import extract_entities

print("API Key Exists:", os.getenv("OPENAI_API_KEY") is not None)

# ----------------------------------------------------
# Load Document
# ----------------------------------------------------

document = load_html_document(
    "data/tn_schemes.html",
    "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="
)

# ----------------------------------------------------
# Split into Chunks
# ----------------------------------------------------

chunks = split_document(document)

chunk = chunks[1].page_content

# ----------------------------------------------------
# Entity Extraction
# ----------------------------------------------------

entities = extract_entities(chunk)

# ----------------------------------------------------
# Relationship Extraction
# ----------------------------------------------------

relationships = extract_relationships(chunk)

# ----------------------------------------------------
# Build NetworkX Graph
# ----------------------------------------------------

graph = NetworkXStore()
for relation in relationships:

    if relation["relationship"] == "MANAGES":

        graph.add_relationship(
            relation["source"],
            "Department",

            relation["relationship"],

            relation["target"],
            "Scheme"
        )

    elif relation["relationship"] == "BENEFITS":

        graph.add_relationship(
            relation["source"],
            "Scheme",

            relation["relationship"],

            relation["target"],
            "Beneficiary"
        )
#graph.print_graph()
graph.visualize_graph()

from query.graph_query import GraphQuery
from rag.graph_rag import answer_question

query = GraphQuery(graph)

context = query.build_context_for_scheme(
    "Distribution of Gypsum"
)
from query.graph_query import GraphQuery
from query.llm_graph_agent import LLMGraphAgent

query = GraphQuery(graph)
agent = LLMGraphAgent(query)

print("\n===== GRAPH RAG CHAT =====")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = agent.ask(question)

    print("\nAssistant:")
    print(answer)
    print()