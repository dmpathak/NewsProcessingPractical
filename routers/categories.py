from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Category
from schemas.news import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    name = payload.name.casefold()
    if db.query(Category).filter(Category.name == name).first():
        raise HTTPException(status_code=409, detail="Category already exists")
    category = Category(name=name)
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        if db.query(Category).filter(Category.name == name).first():
            raise HTTPException(status_code=409, detail="Category already exists")
        raise
    db.refresh(category)
    return category


@router.get("", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()
