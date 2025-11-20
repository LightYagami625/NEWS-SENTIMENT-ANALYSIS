#419f0308d1a14c66a90978c3bdeeb3ee
import requests
from datetime import date
from .config import API_KEY, NEWS_URL


def fetch_headlines():
    params = {
        "language": "en",
        "pageSize": 100,
        "apiKey": API_KEY,
        # "category": "technology",
        # "country": "in"
    }
    resp = requests.get(NEWS_URL, params=params)
    data = resp.json()
    headlines = []
    for article in data.get("articles", []):
        headlines.append({
            "source": article.get("source", {}).get("name"),
            "title": article.get("title"),
        })
    return headlines

def headlines_for_db():
    params = {
        "language": "en",
        "pageSize": 100,
        "apiKey": API_KEY,
        # "category": "technology",
        # "country": "in"
    }
    resp = requests.get(NEWS_URL, params=params)
    data = resp.json()
    headlines = []
    for article in data.get("articles", []):
        headlines.append({
            "source": article.get("source", {}).get("name"),
            "title": article.get("title"),
            "date": date.today().isoformat(),
        })
    return headlines

if __name__ == '__main__':
    # simple smoke test when running this module directly
    articles = fetch_headlines()
    print(f"Fetched {len(articles)} articles")
    for a in articles[:5]:
        print(a)