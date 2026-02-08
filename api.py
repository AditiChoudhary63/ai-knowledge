from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from graph import get_graph
from pydantic import BaseModel
from rag import rag_instance
import logging

logger = logging.getLogger(__name__)
app = FastAPI()
load_dotenv()

class AskRequest(BaseModel):
    question: str
class AskResponse(BaseModel):
    answer: str
    messages:list=[]

class DocumentRequest(BaseModel):
    text: str
class DocumentResponse(BaseModel):
    filepath: str
    message: str

@app.post("/document", response_model=DocumentResponse)
def document(request: DocumentRequest):
    try:
        result = rag_instance.save_text_to_file(request.text)
        logger.info(result)
        return DocumentResponse(filepath=result, message="Document saved successfully")
    except Exception as e:
        return DocumentResponse(filepath="", message=f"Error: {str(e)}")

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    try:
        compiled_graph = await get_graph()
        result = await compiled_graph.ainvoke({"input": request.question})
        return AskResponse(answer=result["answer"], messages=result["messages"])
    except Exception as e:
        return AskResponse(answer=f"Error: {str(e)}", messages=[])