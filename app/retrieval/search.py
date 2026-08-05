from app.embeddings.embedder import embed_text
from app.vectorstore.chroma_store import collection

def search_articles(query:str, top_k:int = 5) -> list[dict]:
    query_vector = embed_text(query, task_type="RETRIEVAL_QUERY")

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    articles = []
    for i in range(len(results["ids"][0])):
        articles.append({
            "number": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return articles
