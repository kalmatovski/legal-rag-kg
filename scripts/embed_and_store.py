import json
import time

from app.vectorstore.chroma_store import add_article, collection
from app.embeddings.embedder import embed_text

with open("data/processed/articles.json", encoding="utf-8") as f:
    articles = json.load(f)

for i, article in enumerate(articles, start=1):
    vector = embed_text(article["text"])
    add_article(article=article, vector=vector)
    print(f"[{i}/{len(articles)}] Добавлена статья {article['number']}")
    time.sleep(1)

print("Готово. Всего в коллекции:", collection.count())