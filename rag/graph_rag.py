from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are an expert assistant.

Answer ONLY using the provided graph context.

If the answer is unavailable, say:

"I couldn't find this information in the knowledge graph."

Question:
{question}

Knowledge Graph Context:
{context}

Answer:
""")

chain = prompt | llm


def answer_question(question, context):

    response = chain.invoke({
        "question": question,
        "context": context
    })

    return response.content