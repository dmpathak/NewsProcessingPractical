import re

from sqlalchemy.orm import Session

from celery_worker import celery
from models import Category, Article

CATEGORY_KEYWORDS = {
    "automotive": ("automotive", "vehicle", "vehicles", "car", "cars", "ev"),
    "technology": ("software", "technology", "ai", "computer", "computers"),
    "healthcare": ("healthcare", "hospital", "medical", "medicine", "drug"),
    "finance": ("bank", "banking", "loan", "stock", "stocks", "insurance"),
    "business": ("investment", "invest", "company", "revenue", "acquisition"),
}


def classify_article(db: Session, title: str, content: str):
    """
    checking if title or content contains any above words or not. if has then give categories accordingly.
    :param title:
    :param content:
    :return:
    """
    words = set(re.findall(r"\b\w+\b", f"{title} {content}".casefold()))

    categories = set(db.query(Category).all())
    for category, keywords in CATEGORY_KEYWORDS.items():
        if words.intersection(keywords):
            return category
    return "Business"


def summarize_article(content: str):
    text = " ".join(content.split())
    if not text:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(sentences[:2])
    return summary if len(summary) <= 300 else summary[:297].rstrip() + "..."


@celery.task(bind=True, max_retries=3)
def summarize_classify_and_article(db: Session, article):
    """
    takes db session for saving summary and classified result into database we will be using transaction atomic to
    ensure atomicity in database operation if any error occured we can rollback in handled exception.

    1. classify article
    2. summarize article
    3. store values into db.
    """

    category = classify_article(db, article.title, article.content)
    summary = summarize_article(article.content)

    try:
        article.category = category
        article.summary = summary
        article.status = Article.completed

        db.add(article)
        db.commit()
    except:
        raise

