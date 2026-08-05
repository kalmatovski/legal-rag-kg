from google import genai

from app.config import GEMINI_API_KEY
from app.retrieval.search import search_articles

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """Ты — юридический ассистент по Гражданскому кодексу Кыргызской Республики.
Отвечай на вопрос пользователя ТОЛЬКО на основе текста статей, приведённых ниже.
Обязательно указывай номера статей, на которые опираешься.
Если в приведённых статьях нет ответа на вопрос — прямо скажи, что не нашёл релевантной информации, не выдумывай.
"""


def build_context(articles: list[dict]) -> str:
    parts = []
    for a in articles:
        parts.append(f"Статья {a['number']} ({a['metadata']['title']}):\n{a['text']}")
    return "\n\n".join(parts)


def ask(question: str, top_k: int = 5) -> str:
    articles = search_articles(question, top_k=top_k)
    context = build_context(articles)

    prompt = f"{SYSTEM_PROMPT}\n\nСтатьи:\n{context}\n\nВопрос: {question}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text