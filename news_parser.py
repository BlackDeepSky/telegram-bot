import requests
from config import NEWS_API_KEY
from transformers import pipeline

# Инициализация модели для суммаризации
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

BASE_URL = "https://newsapi.org/v2/everything"
CATEGORIES = [
    "роботы", "исследования", "наука", "игры", "криптовалюта", "техника", "мировые новости", "технологии"
]

def summarize_text(text):
    """Создаёт краткий пересказ текста с помощью Hugging Face."""
    try:
        # Ограничение длины входного текста для экономии ресурсов
        truncated_text = text[:1000]  # Берём первые 1000 символов
        summary = summarizer(truncated_text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text'].strip()
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Ошибка при создании выжимки."

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
                # Создаём выжимку
                description = article.get("description", "")
                content = article.get("content", "")
                if description:
                    summary = summarize_text(description)
                elif content:
                    summary = summarize_text(content)
                else:
                    summary = "Краткое описание недоступно."
                news_data.append({
                    "title": article["title"],
                    "url": article["url"],
                    "image_url": article.get("urlToImage", ""),
                    "category": category,
                    "summary": summary
                })
    return news_data