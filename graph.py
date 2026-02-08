from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import Dict, Any
import os
from dotenv import load_dotenv
from rag import rag_instance
from common_functions import get_llm
import logging
import mcp_client
import asyncio
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import StructuredTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
logger = logging.getLogger(__name__)

load_dotenv()


# Check for API keys and initialize LLM
if os.getenv("GROQ_API_KEY"):
    llm = get_llm(provider="groq", model="openai/gpt-oss-120b", temperature=0.2)
    logger.info("Using Groq API")
elif os.getenv("OPENAI_API_KEY"):
    llm = get_llm(provider="openai", model="gpt-4o-mini", temperature=0.2)
    logger.info("Using OpenAI API")
else:
    raise ValueError(
        "Missing required environment variable: Either OPENAI_API_KEY or GROQ_API_KEY must be set. "
        "Please set at least one in your .env file or environment."
    )
client = MultiServerMCPClient(
        {
            "mcp_server": {
                "transport": "stdio",
                "command": "uv",
                "args": ["--directory","C:\\code\\ai_knowledge\\ai-knowledge","run","mcp_server.py"],
            }
        }
    )
class GraphState(dict):
    input: str
    answer: str
    context: str
    messages:list=[]
def retrieve(state: GraphState) -> GraphState:
    context = rag_instance.retrieve_docs(state["input"])
    logger.info(f"CONTEXT: {context}")
    state["context"] = context
    return state



async def get_graph():
    async with client.session("mcp_server") as session:
        tools = await load_mcp_tools(session)
        logger.info(f"TOOLS: {tools}")
        async def answer(state: GraphState) -> GraphState:
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
            try:
                llm_with_tools = llm.bind_tools(tools)
                response = await llm_with_tools.ainvoke(prompt)
                logger.info(f"RESPONSE: {response}")
                logger.info(f"TOOL_CALLS: {response.tool_calls}") 
                from langchain_core.messages import AIMessage
                ai_message = AIMessage(content=response.content, tool_calls=response.tool_calls)
                
                # Update both answer and messages
                return {
                    "answer": response.content,
                    "messages": [ai_message] 
                }
                # state["answer"] = response.content
                # return {"answer": response.content}
            except Exception as err:
                logger.error(f"ERROR: {err}")
                return {"answer": "Error: " + str(err)}
    
        tool_node = ToolNode(tools)
        graph = StateGraph(GraphState)
        graph.add_node("retrieve", retrieve)
        graph.add_node("answer", answer)
        graph.add_node("tool_node", tool_node)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_conditional_edges(
            "answer",
            tools_condition,
        )
        graph.add_edge("tool_node", "answer")
        compiled_graph = graph.compile()
        print(compiled_graph.get_graph().print_ascii())
        return compiled_graph

# if __name__ == "__main__":
#     asyncio.run(get_graph())
