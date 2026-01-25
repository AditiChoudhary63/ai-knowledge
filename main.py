from openai import OpenAI
import os
from dotenv import load_dotenv
import uvicorn
from api import app
import logging
from logger import setup_logger
# from groq import Groq
# client = Groq()
load_dotenv()

# Check that at least one API key is present
has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
has_groq_key = bool(os.getenv("GROQ_API_KEY"))

if not has_openai_key and not has_groq_key:
    raise ValueError(
        "Missing required environment variable: Either OPENAI_API_KEY or GROQ_API_KEY must be set. "
        "Please set at least one in your .env file or environment."
    )
# client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
# client = OpenAI(api_key = os.getenv("GROQ_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"),)
# response = client.responses.create(
#     model="gpt-4o-mini",
#     input="What is the capital of France?")
# print(response.output_text)
# response = client.chat.completions.create(
#     model="openai/gpt-oss-120b",
#     messages=[
#       {
#         "role": "user",
#         "content": "What is the capital of France?"
#       }
#     ],

# )
# print("response", response.choices[0].message.content)

setup_logger()
if __name__ == "__main__":
    # logger = logging.getLogger(__name__)
    # logger.info("FastAPI application started")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


