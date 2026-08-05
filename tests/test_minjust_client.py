from unittest.mock import patch, Mock

from app.ingestion.minjust_client import fetch_edition, MinjustAPIError


@patch("app.ingestion.minjust_client.requests.get")
def test_fetch_edition_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 52160, "contentRu": "<html>...</html>"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_edition(52160)

    assert result["id"] == 52160
    mock_get.assert_called_once()


@patch("app.ingestion.minjust_client.requests.get")
def test_fetch_edition_timeout_raises_minjust_error(mock_get):
    import requests
    mock_get.side_effect = requests.exceptions.Timeout()

    try:
        fetch_edition(52160)
        assert False, "Ожидалась ошибка MinjustAPIError"
    except MinjustAPIError:
        pass