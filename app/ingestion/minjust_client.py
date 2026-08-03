import requests
from app.config import MINJUST_BASE_URL, MINJUST_HEADERS


class MinjustAPIError(Exception):
    pass


def _get(endpoint: str, params: dict, timeout: int, context: str) -> dict:
    url = f"{MINJUST_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=MINJUST_HEADERS, params=params, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise MinjustAPIError(f"Минюст не ответил за {timeout} сек ({context})")
    except requests.exceptions.ConnectionError:
        raise MinjustAPIError(f"Не удалось подключиться к минюсту ({context})")
    except requests.exceptions.HTTPError:
        raise MinjustAPIError(f"Минюст вернул ошибку {response.status_code} ({context})")

    try:
        return response.json()
    except ValueError:
        raise MinjustAPIError(f"Ответ минюста — не валидный JSON ({context})")


def fetch_edition(edition_id: int, lang: str = "ru", timeout: int = 10) -> dict:
    params = {"editionId": edition_id, "lang": lang}
    return _get("GetEdition", params, timeout, f"editionId={edition_id}")


def fetch_document(document_code, timeout: int = 10) -> dict:
    params = {"DocumentCode": document_code}
    return _get("GetDocument", params, timeout, f"DocumentCode={document_code}")


def extract_document_metadata(document_data: dict) -> dict:
    keywords = [kw["nameRus"] for kw in document_data.get("kluchSlov") or []]
    editions = [
        {"id": e["id"], "date": e["nameRus"]}
        for e in document_data.get("editions") or []
    ]

    return {
        "document_code": document_data["documentCode"],
        "name": document_data["nameRus"],
        "status_code": document_data["status"]["code"],
        "status_name": document_data["status"]["nameRus"],
        "keywords": keywords,
        "editions": editions,
    }