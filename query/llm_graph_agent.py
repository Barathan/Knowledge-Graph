from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class LLMGraphAgent:

    def __init__(self, graph_query):

        self.graph_query = graph_query

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template("""
You are a Knowledge Graph assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:

"I don't know from the available knowledge graph."

Context:

{context}

Question:

{question}
""")

        self.chain = self.prompt | self.llm

    def ask(self, question):

        question_lower = question.lower()

        context = ""

        # Department query
        if "department" in question_lower and "manages" in question_lower:

            scheme = question.split("manages")[-1].replace("?", "").strip()

            context = self.graph_query.build_context_for_scheme(
                scheme
            )

        # Beneficiary query
        elif "benefit" in question_lower or "benefits" in question_lower:

            if "from" in question_lower:
                scheme = question.split("from")[-1].replace("?", "").strip()
            else:
                scheme = question.replace("?", "").strip()

            context = self.graph_query.build_context_for_scheme(
                scheme
            )

        # Complete information
        elif "complete information" in question_lower:

            scheme = question.replace(
                "Give me complete information about",
                ""
            ).replace("?", "").strip()

            context = self.graph_query.build_context_for_scheme(
                scheme
            )

        else:

            context = "No matching graph query."

        response = self.chain.invoke({
            "context": context,
            "question": question
        })

        return response.content