from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Article, ArticleStatus
from schemas.news import ArticleCreate, ArticleRead
from utils.articles import summarize_classify_and_article

router = APIRouter(prefix="/articles", tags=["articles"])

# from Phase 1
@router.post("", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    url = str(payload.url)
    if db.query(Article).filter(Article.url == url).first():
        raise HTTPException(status_code=409, detail="Article URL already exists")
    article = Article(**payload.model_dump(exclude={"url"}), url=url)
    db.add(article)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # The unique constraint also protects simultaneous requests.
        if db.query(Article).filter(Article.url == url).first():
            raise HTTPException(status_code=409, detail="Article URL already exists")
        raise
    db.refresh(article)
    return article


@router.get("", response_model=list[ArticleRead])
def list_articles(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    company_name: str | None = Query(default=None, min_length=1, max_length=200),
    status: ArticleStatus | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Article).options(joinedload(Article.category))
    if company_name is not None:
        query = query.filter(Article.company_name == company_name.strip())
    if status is not None:
        query = query.filter(Article.status == status)
    return query.order_by(Article.id.desc()).offset(offset).limit(limit).all()


# from Phase 2
@router.post("/articles/{article_id}/process")
def classify_and_summarize_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=409, detail="Article not found.")
    if article.status == ArticleStatus.processing:
        raise HTTPException(status_code=409, detail="Article already Proceed")
    # call background function
    try:
        task = summarize_classify_and_article.delay(db, article)
        article.status = ArticleStatus.processing
        db.add(article)
        db.commit()
        return {"job_id": task.id, "message" : "Article classification and summary generation started in background"}
    except:
        article.status = ArticleStatus.failed
        db.add(article)
        db.commit()
        raise HTTPException(status_code=400, detail="Something went wrong into celery processing")


