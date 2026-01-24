from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from graph import compiled_graph
from pydantic import BaseModel
from rag import save_text_to_file
app = FastAPI()
load_dotenv()

class AskRequest(BaseModel):
    question: str
class AskResponse(BaseModel):
    answer: str

class DocumentRequest(BaseModel):
    text: str
class DocumentResponse(BaseModel):
    filepath: str
    message: str

@app.post("/document", response_model=DocumentResponse)
def document(request: DocumentRequest):
    try:
        result = save_text_to_file(request.text)
        print(result)
        return DocumentResponse(filepath=result, message="Document saved successfully")
    except Exception as e:
        return DocumentResponse(filepath="", message=f"Error: {str(e)}")

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    result = compiled_graph.invoke({"input": request.question})
    return AskResponse(answer=result["answer"])