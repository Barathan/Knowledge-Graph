from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_document(document):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents([document])

    return chunks