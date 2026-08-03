from app.embeddings.embedder import embed_text

vector = embed_text("Гражданское законодательство определяет правовое положение участников гражданского оборота.")
print("Длина вектора:", len(vector))
print("Первые 5 чисел:", vector[:5])