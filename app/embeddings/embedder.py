from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={"task_type": task_type},
    )
    return response.embeddings[0].values