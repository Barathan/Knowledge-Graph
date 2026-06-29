import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from loaders.document_loader import load_html_document
from loaders.text_splitter import split_document
from extraction.relationship_extractor import extract_relationships
from graph.networkx_store import NetworkXStore
from query.graph_query import GraphQuery
from query.llm_graph_agent import LLMGraphAgent


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Tamil Nadu Scheme AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LANGUAGE SUPPORT
# =========================
LANG = {
    "English": {
        "title": "🏛️ Tamil Nadu Scheme Assistant",
        "subtitle": "Graph RAG AI Assistant",
        "chat_placeholder": "Ask about schemes...",
        "welcome": "Ask anything about Tamil Nadu Government Schemes.",
        "thinking": "Thinking...",
        "input": "Type your question",
        "chat": "Chat Assistant"
    },
    "தமிழ்": {
        "title": "🏛️ தமிழ்நாடு திட்ட உதவியாளர்",
        "subtitle": "Graph RAG AI உதவியாளர்",
        "chat_placeholder": "திட்டங்களை பற்றி கேளுங்கள்...",
        "welcome": "தமிழ்நாடு அரசு திட்டங்களைப் பற்றி கேளுங்கள்.",
        "thinking": "சிந்திக்கிறது...",
        "input": "கேள்வியை எழுதுங்கள்",
        "chat": "உதவியாளர்"
    }
}

# =========================
# SIDEBAR
# =========================
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/8/81/TamilNadu_Logo.png",
    width=100
)

language = st.sidebar.radio("🌐 Language", ["English", "தமிழ்"])
T = LANG[language]

st.sidebar.markdown("---")
st.sidebar.success("Graph RAG Active 🚀")

# =========================
# CSS (Chat UI FIX)
# =========================
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

/* chat bubbles */
.user-bubble {
    background: #DCF8C6;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 5px 0;
    max-width: 80%;
    margin-left: auto;
}

.bot-bubble {
    background: #F1F0F0;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 5px 0;
    max-width: 80%;
}

.chat-box {
    height: 65vh;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #eee;
    border-radius: 10px;
    background: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GRAPH BUILD (FIXED)
# =========================
@st.cache_resource
def build_graph():

    graph = NetworkXStore()

    document = load_html_document(
        "data/tn_schemes.html",
        "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="
    )

    chunks = split_document(document)

    for chunk in chunks:

        # FIX: chunk already object → no indexing
        text = getattr(chunk, "page_content", str(chunk))

        relations = extract_relationships(text)

        for rel in relations:

            if rel["relationship"] == "MANAGES":
                graph.add_relationship(
                    rel["source"],
                    "Department",
                    "MANAGES",
                    rel["target"],
                    "Scheme"
                )

            elif rel["relationship"] == "BENEFITS":
                graph.add_relationship(
                    rel["source"],
                    "Scheme",
                    "BENEFITS",
                    rel["target"],
                    "Beneficiary"
                )

    return graph


with st.spinner("Building Knowledge Graph..."):
    graph = build_graph()

query = GraphQuery(graph)
agent = LLMGraphAgent(query)

# =========================
# HEADER
# =========================
st.title(T["title"])
st.caption(T["subtitle"])
st.write(T["welcome"])

# =========================
# STATS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Departments", len(graph.get_nodes_by_type("Department")))

with col2:
    st.metric("Schemes", len(graph.get_nodes_by_type("Scheme")))

with col3:
    st.metric("Beneficiaries", len(graph.get_nodes_by_type("Beneficiary")))

st.divider()

# =========================
# LAYOUT FIX (CHAT RIGHT TOP)
# =========================
left, right = st.columns([1, 1])

# GRAPH
with left:
    st.subheader("🕸 Knowledge Graph")

    if os.path.exists("knowledge_graph.png"):
        st.image("knowledge_graph.png")
    else:
        st.info("Graph not generated")

# =========================
# CHAT UI FIX (NO BOTTOM SHIFT ISSUE)
# =========================
with right:
    st.subheader("🤖 " + T["chat"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # CHAT BOX
    chat_container = st.container()

    with chat_container:
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)

        for role, msg in st.session_state.messages:
            if role == "user":
                st.markdown(f"<div class='user-bubble'>🧑 {msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-bubble'>🤖 {msg}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # INPUT FIX (always stays bottom of column)
    user_input = st.chat_input(T["input"])

    if user_input:

        st.session_state.messages.append(("user", user_input))

        with st.spinner(T["thinking"]):
            response = agent.ask(user_input)

            # FIX: fallback clean response handling
            if not response or "I don't know" in str(response):
                response = query.build_context_for_scheme(user_input)

        st.session_state.messages.append(("assistant", response))

        st.rerun()