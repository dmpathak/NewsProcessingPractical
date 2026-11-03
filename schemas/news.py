from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from models import ArticleStatus


class CategoryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1, max_length=100)


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ArticleCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    company_name: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=500)
    url: HttpUrl = Field(max_length=2048)
    content: str = Field(min_length=1)


class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company_name: str
    title: str
    url: str
    content: str
    status: ArticleStatus
    category: CategoryRead | None
    summary: str | None
    created_at: datetime
