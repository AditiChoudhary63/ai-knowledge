from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
from rag import retrieve_docs
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")
class GraphState(dict):
    input: str
    answer: str
    context: str
def retrieve(state: GraphState) -> GraphState:
    context = retrieve_docs(state["input"])
    print("CONTEXT", context)
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
    print("RESPONSE", response)
    state["answer"]: response.content
    print(state,"State")
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


