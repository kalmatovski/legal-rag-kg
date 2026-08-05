from app.ingestion.parser import extract_number, extract_title, split_into_articles


def test_extract_number_plain():
    assert extract_number("Статья 244.") == "244"


def test_extract_number_hyphenated():
    assert extract_number("Статья 82-1.") == "82-1"


def test_extract_number_superscript():
    assert extract_number("Статья 233<sup>1</sup>.") == "233-1"


def test_split_into_articles_basic():
    html = (
        "Статья 1. Первая статья<p>Текст первой статьи.</p>"
        "Статья 2. Вторая статья<p>Текст второй статьи.</p>"
    )
    articles = split_into_articles(html)

    assert len(articles) == 2
    assert articles[0]["number"] == "1"
    assert articles[0]["title"] == "Первая статья"
    assert "Текст первой статьи" in articles[0]["text"]


def test_split_into_articles_strips_amendments():
    html = (
        "Статья 1. Название<p>Основной текст.</p>"
        "<i>(В редакции Закона КР от 1 января 2020 года)</i>"
    )
    articles = split_into_articles(html)

    assert "В редакции" not in articles[0]["text"]
    assert "Основной текст" in articles[0]["text"]