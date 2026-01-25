from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
import os
from dotenv import load_dotenv
from rag import rag_instance
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import logging

logger = logging.getLogger(__name__)

load_dotenv()

# Check for API keys and initialize LLM
if os.getenv("GROQ_API_KEY"):
    llm = ChatGroq(model="openai/gpt-oss-120b")
    logger.info("Using Groq API")
elif os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-4o-mini")
    logger.info("Using OpenAI API")
else:
    raise ValueError(
        "Missing required environment variable: Either OPENAI_API_KEY or GROQ_API_KEY must be set. "
        "Please set at least one in your .env file or environment."
    )
class GraphState(dict):
    input: str
    answer: str
    context: str
def retrieve(state: GraphState) -> GraphState:
    context = rag_instance.retrieve_docs(state["input"])
    logger.info(f"CONTEXT: {context}")
    state["context"] = context
    return state
def answer(state: GraphState) -> GraphState:
    """
    Generates answer using retrieved context
    """
    prompt = f"""
    Answer the question using ONLY the context below.
    Context:
    {state['context']}

    Question:
    {state['input']}
    """
    response = llm.invoke(prompt)
    logger.info(f"RESPONSE: {response}")
    state["answer"]: response.content
    return {"answer": response.content}


graph = StateGraph(GraphState)
graph.add_node("retrieve", retrieve)
graph.add_node("answer", answer)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)
compiled_graph = graph.compile()
# result =compiled_graph.invoke({"input": "What is the capital of France?"})
# print(result)
print(compiled_graph.get_graph().print_ascii())


