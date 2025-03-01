import requests
from config import NEWS_API_KEY

BASE_URL = "https://newsapi.org/v2/everything"
CATEGORIES = [
    "роботы", "исследования", "наука", "игры", "криптовалюта", "техника", "мировые новости", "технологии"
]

def get_news():
    news_data = []
    for category in CATEGORIES:
        params = {
            "q": category,
            "apiKey": NEWS_API_KEY,
            "language": "ru",
            "pageSize": 1,  # Берём только одну статью
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if articles:
                article = articles[0]
                news_data.append({
                    "title": article["title"],
                    "url": article["url"],
                    "category": category
                })
    return news_data