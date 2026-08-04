import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="civil_code_kg")

def add_article(article:dict, vector:list[float]) -> None:
    collection.add(
        ids=[article["number"]],
        embeddings=[vector],
        documents=[article["text"]],
        metadatas=[{
            "number": article["number"],
            "title": article["title"],
            "chapter_number": article["chapter_number"] or "",
            "chapter_title": article["chapter_title"] or "",
            "has_repealed_clauses": article["has_repealed_clauses"],
        }],
    )