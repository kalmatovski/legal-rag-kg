import json
from pathlib import Path

from app.ingestion.minjust_client import fetch_edition, fetch_document, extract_document_metadata, MinjustAPIError
from app.ingestion.parser import split_into_articles

EDITION_ID = 52160
DOCUMENT_CODE = 4
OUTPUT_DIR = Path("data/processed")

def main():
    print(f"Скачиваю редакцию {EDITION_ID}...")
    edition_data = fetch_edition(EDITION_ID)
    articles = split_into_articles(edition_data["contentRu"])
    print(f"Найдено статей: {len(articles)}")

    print(f"Скачиваю метаданные документа {DOCUMENT_CODE}...")
    document_data = fetch_document(DOCUMENT_CODE)
    document_metadata = extract_document_metadata(document_data)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    articles_path = OUTPUT_DIR / "articles.json"
    with open(articles_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Сохранено: {articles_path}")

    metadata_path = OUTPUT_DIR / "document_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(document_metadata, f, ensure_ascii=False, indent=2)
    print(f"Сохранено: {metadata_path}")


if __name__ == "__main__":
    try:
        main()
    except MinjustAPIError as e:
        print(f"Ошибка: {e}")