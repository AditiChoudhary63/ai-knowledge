import time
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Any, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv() 


if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "Missing required environment variable: OPENAI_API_KEY. "
        "Please set it in your .env file or environment."
    )


class RAG:
    """RAG (Retrieval-Augmented Generation) class for document management and retrieval."""
    
    def __init__(
        self,
        documents_dir: str = "./documents",
        persist_directory: str = "./chroma_db",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        """
        Initialize the RAG class.
        
        Args:
            documents_dir: Directory to store document files
            persist_directory: Directory to persist the vectorstore
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.documents_dir = documents_dir
        self.persist_directory = persist_directory
        
        self.embeddings = OpenAIEmbeddings()
        
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        logger.info("RAG class initialized successfully")
    
    def save_text_to_file(self, text: str) -> str:
        """
        Save text to a file and ingest it into the vectorstore.
        
        Args:
            text: The text content to save
            
        Returns:
            str: Path to the saved file
            
        Raises:
            ValueError: If text is not a non-empty string
            OSError, IOError: If file I/O operations fail
        """
        try:
            if not text or not isinstance(text, str):
                raise ValueError("Text must be a non-empty string")
            
            filename = f"doc_{time.time()}.txt"
            filepath = os.path.join(self.documents_dir, filename)
            os.makedirs(self.documents_dir, exist_ok=True)
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
            
            self.ingest_documents(filepath)
            logger.info(f"Successfully saved text to file: {filepath}")
            return filepath
        except (OSError, IOError) as e:
            logger.error(f"File I/O error while saving text to file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in save_text_to_file: {str(e)}")
            raise
    def add_note(self, text: str) -> str:
        """
        Save text to a file.
        
        Args:
            text: The text content to save
            
        Returns:
            str: Path to the saved file
            
        """
        try:
            print("ttt",text)
            if not text or not isinstance(text, str):
                raise ValueError("Text must be a non-empty string")
            
            filename = f"doc_{time.time()}.txt"
            filepath = os.path.join(self.documents_dir, filename)
            os.makedirs(self.documents_dir, exist_ok=True)
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
            logger.info(f"Successfully saved text to file: {filepath}")
            return filepath
        except (OSError, IOError) as e:
            logger.error(f"File I/O error while saving text to file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in save_text_to_file: {str(e)}")
            raise

    def chunk_file(self, filepath: str) -> List[Document]:
        """
        Chunk a file into documents.
        
        Args:
            filepath: Path to the file to chunk
            
        Returns:
            List[Document]: List of document chunks
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty
            OSError, IOError: If file I/O operations fail
        """
        try:
            if not filepath or not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
            
            if not text.strip():
                raise ValueError(f"File is empty: {filepath}")
            
            documents = self.splitter.split_documents([
                Document(
                    page_content=text,
                    metadata={"source": filepath}
                )
            ])
            logger.info(f"DOCUMENTS -> {documents}")
            return documents
        except (OSError, IOError) as e:
            logger.error(f"File I/O error while chunking file {filepath}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in chunk_file for {filepath}: {str(e)}")
            raise

    def create_embeddings(self, documents: list[Document]) -> None:
        """
        Create embeddings for documents and add them to the vectorstore.
        
        Args:
            documents: List of documents to create embeddings for
            
        Raises:
            ValueError: If documents list is empty
        """
        try:
            if not documents or len(documents) == 0:
                raise ValueError("Documents list is empty, cannot create embeddings")
            
            self.vectorstore.add_documents(documents)
            count = self.vectorstore._collection.count()
            logger.info(f"vectorstore collection count: {count}")
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    def ingest_documents(self, filepath: str) -> None:
        """
        Ingest documents from a file into the vectorstore.
        
        Args:
            filepath: Path to the file to ingest
            
        Raises:
            Exception: If ingestion fails
        """
        try:
            documents = self.chunk_file(filepath)
            self.create_embeddings(documents)
            logger.info(f"Successfully ingested documents from {filepath}")
        except Exception as e:
            logger.error(f"Error ingesting documents from {filepath}: {str(e)}")
            raise
    
    def retrieve_docs(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents from the vectorstore based on a query.
        
        Args:
            query: Search query string
            
        Returns:
            List[Document]: List of retrieved documents
            
        Raises:
            ValueError: If query is not a non-empty string
        """
        try:
            if not query or not isinstance(query, str) or not query.strip():
                raise ValueError("Query must be a non-empty string")
            
            docs = self.vectorstore.similarity_search(query, k=3)
            logger.info(f"Retrieved {len(docs)} documents for query: {query[:50]}...")
            return docs
        except Exception as e:
            logger.error(f"Error retrieving documents for query '{query}': {str(e)}")
            raise


rag_instance = RAG()
