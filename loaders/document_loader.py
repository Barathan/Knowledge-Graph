from bs4 import BeautifulSoup
from langchain_core.documents import Document


def load_html_document(file_path: str, source_url: str):
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text
    text = soup.get_text(separator="\n")

    # Remove empty lines
    cleaned_text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    document = Document(
        page_content=cleaned_text,
        metadata={
            "source": source_url
        }
    )

    return document