from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Create the LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are an expert information extraction system.

Extract all entities from the given text.

Entity Types:
- Department
- Scheme
- Beneficiary
- Benefit
- Eligibility
- Location

Return ONLY valid JSON.

Text:
{text}
""")

# Create chain
chain = prompt | llm


# Function to call from app.py
def extract_entities(text: str):
    response = chain.invoke({"text": text})
    return response.content