import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are an expert Knowledge Graph extraction system.

The text contains a department heading followed by a list of schemes.

Infer relationships even if they are implied.

Rules:

1. Department --MANAGES--> Scheme

2. Scheme --BENEFITS--> Farmers

Return ONLY valid JSON.

Example:

[
  {{
    "source": "Agriculture - Farmers Welfare Department",
    "relationship": "MANAGES",
    "target": "Training to Farmers"
  }},
  {{
    "source": "Training to Farmers",
    "relationship": "BENEFITS",
    "target": "Farmers"
  }}
]

Text:

{text}
""")

chain = prompt | llm


def extract_relationships(text: str):
    response = chain.invoke({"text": text})

    try:
        return json.loads(response.content)
    except json.JSONDecodeError as e:
        print("JSON Error:", e)
        return []