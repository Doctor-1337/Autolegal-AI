import requests
from bs4 import BeautifulSoup, NavigableString

BASE_URL = "https://indiankanoon.org"

def search_cases(query: str, num_results: int = 3):
    """Search Indian Kanoon for cases related to the query."""
    search_url = f"{BASE_URL}/search/?formInput={query}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for link in soup.select("a[href^='/doc']")[:num_results]:
        case_url = BASE_URL + link['href']
        case_title = link.text.strip()
        results.append({"title": case_title, "url": case_url})

    return results


def fetch_case_text(url):
    """Fetch full legal content from Indian Kanoon, handling both Akoma and fallback .content."""
    import requests
    from bs4 import BeautifulSoup, NavigableString

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try Akoma Ntoso first
    content_div = soup.find("div", class_="akn-akomaNtoso")

    # Fallback to generic div with class='content'
    if not content_div:
        content_div = soup.find("div", class_="content")

    if not content_div:
        return "❌ Could not find legal content block."

    def extract_text_recursive(tag):
        lines = []
        for elem in tag.descendants:
            if isinstance(elem, NavigableString):
                text = str(elem).strip()
                if text:
                    lines.append(text)
        return "\n".join(lines)

    full_text = extract_text_recursive(content_div)
    return full_text.strip() or "❌ No meaningful text found."

