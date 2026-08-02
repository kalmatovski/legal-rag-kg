import re
from bs4 import BeautifulSoup

ARTICLE_PATTERN = re.compile(
    r'Статья\s+\d+(?:-\d+|\s*<sup>\s*\d+\s*</sup>)?\s*\.'
)
CHAPTER_PATTERN = re.compile(
    r'Глава\s+(\d+(?:-\d+)?)\s*<br>\s*(?:&nbsp;)*\s*([^<]*)'
)
REPEALED_PATTERN = re.compile(r'[Уу]трати[а-я]* силу')


def extract_number(header_text: str) -> str:
    digits = re.findall(r'\d+', header_text)
    return "-".join(digits)


def extract_title(text_after_header: str) -> str:
    match = re.match(r'([^<]*)', text_after_header)
    return match.group(1).strip()


def has_repealed_clauses(raw_html: str) -> bool:
    return bool(REPEALED_PATTERN.search(raw_html))


def strip_amendments(html: str) -> str:
    return re.sub(r'<i>.*?</i>', '', html, flags=re.DOTALL)


def clean_text(raw_html: str) -> str:
    without_amendments = strip_amendments(raw_html)
    text = BeautifulSoup(without_amendments, 'lxml').get_text(separator=' ', strip=True)
    return re.sub(r'\s+', ' ', text).strip()


def find_chapters(html: str) -> list[tuple[int, str, str]]:
    return [
        (m.start(), m.group(1), m.group(2).strip())
        for m in CHAPTER_PATTERN.finditer(html)
    ]


def chapter_for_position(chapters: list[tuple[int, str, str]], position: int):
    current_number, current_title = None, None
    for chap_pos, number, title in chapters:
        if chap_pos > position:
            break
        current_number, current_title = number, title
    return current_number, current_title


def split_into_articles(html: str) -> list[dict]:
    matches = list(ARTICLE_PATTERN.finditer(html))
    chapters = find_chapters(html)
    articles = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        raw_html = html[start:end]
        header_length = match.end() - match.start()
        chapter_number, chapter_title = chapter_for_position(chapters, start)

        articles.append({
            "number": extract_number(match.group()),
            "title": extract_title(raw_html[header_length:]),
            "text": clean_text(raw_html),
            "has_repealed_clauses": has_repealed_clauses(raw_html),
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
        })

    return articles

if __name__ == "__main__":
    with open("edition_content.html", encoding="utf-8") as f:
        html = f.read()

    articles = split_into_articles(html)

    print("Всего статей:", len(articles))
    print()

    # первые 3 статьи целиком
    for a in articles[:3]:
        print(a["number"], "|", a["title"], "| Глава", a["chapter_number"])
        print(a["text"][:200])
        print("---")

    # статьи с отменёнными пунктами
    repealed = [a for a in articles if a["has_repealed_clauses"]]
    print("Статей с отменёнными пунктами:", len(repealed))