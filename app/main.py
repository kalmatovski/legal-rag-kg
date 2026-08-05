from fastapi import FastAPI

from app.models.schemas import AskRequest, AskResponse, SourceArticle
from app.retrieval.generation import ask as generate_answer

app = FastAPI(title="Legal RAG - Kyrgyz Civil Code")

@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request:AskRequest)->AskResponse:
    result = generate_answer(request.question, top_k=request.top_k)

    sources = [
        SourceArticle(
            number=a["number"],
            title=a["metadata"]["title"],
            chapter_title=a["metadata"]["chapter_title"]
        )
        for a in result["articles"]
    ]

    return AskResponse(answer=result["answer"], sources=sources)