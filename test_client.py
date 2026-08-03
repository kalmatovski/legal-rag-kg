from app.ingestion.minjust_client import fetch_edition, MinjustAPIError

try:
    data = fetch_edition(edition_id=52160)
    print("Успех!")
    print("id:", data["id"])
    print("Дата редакции:", data["nameRus"])
    print("Длина contentRu:", len(data["contentRu"]))
except MinjustAPIError as e:
    print("Ошибка:", e)