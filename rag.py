import time
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Any, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv() 
DOCUMENTS_DIR = "./documents"
embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

splitter = RecursiveCharacterTextSplitter(
chunk_size = 500,
chunk_overlap = 50
)

def save_text_to_file(text: str):
    filename = f"doc_{time.time()}.txt"
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    with open(filepath,"w", encoding="utf-8") as file:
        file.write(text)
    ingest_documents(filepath)
    return filepath

def chunk_file(filepath: str) -> List[Document]:
    with open(filepath, "r", encoding = "utf-8") as file: 
        text = file.read()
    documents = splitter.split_documents([
        Document(
            page_content=text,
            metadata={"source": filepath}
        )
    ])
    print("DOCUMENTS ->", documents)
    return documents

def create_embeddings(documents: list[Document]):
    vectorstore.add_documents(documents)
    print(vectorstore._collection.count())


def ingest_documents(filepath: str):
    documents = chunk_file(filepath)
    create_embeddings(documents)
    
def retrieve_docs(query: str)-> List[Document]:
    docs = vectorstore.similarity_search(query, k = 3)
    return docs
    
