from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(documents):

    # SPLIT DOCUMENTS INTO SMALL CHUNKS
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=80
    )

    split_docs = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(split_docs)}")

    vector_store = FAISS.from_documents(
        split_docs,
        embedding_model
    )

    vector_store.save_local("vectorstore")

    return vector_store