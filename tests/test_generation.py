from unittest.mock import patch, Mock

from app.retrieval.generation import ask


@patch("app.retrieval.generation.client")
@patch("app.retrieval.generation.search_articles")
def test_ask_builds_context_and_calls_gemini(mock_search, mock_client):
    mock_search.return_value = [
        {
            "number": "212",
            "text": "Статья 212. Общий срок исковой давности. Общий срок устанавливается в три года.",
            "metadata": {"title": "Общий срок исковой давности", "chapter_title": "Сроки. Исковая давность"},
            "distance": 0.1,
        }
    ]

    mock_response = Mock()
    mock_response.text = "Общий срок исковой давности — три года (Статья 212)."
    mock_client.models.generate_content.return_value = mock_response

    result = ask("Какой срок исковой давности?")

    assert result["answer"] == "Общий срок исковой давности — три года (Статья 212)."
    assert result["articles"] == mock_search.return_value
    mock_search.assert_called_once_with("Какой срок исковой давности?", top_k=5)