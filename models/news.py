import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from database import Base


class ArticleStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(200), nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(2048), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    status = Column(Enum(ArticleStatus, native_enum=False, create_constraint=True),
                    nullable=False, default=ArticleStatus.pending)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category")
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
