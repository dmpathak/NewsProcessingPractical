from fastapi import FastAPI
from routers import articles, categories

app = FastAPI()
app.include_router(categories.router)
app.include_router(articles.router)


