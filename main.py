from openai import OpenAI
import os
from dotenv import load_dotenv
import uvicorn
from api import app
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
# response = client.responses.create(
#     model="gpt-4o-mini",
#     input="What is the capital of France?")
# print(response.output_text)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


