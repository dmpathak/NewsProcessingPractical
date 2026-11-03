# Company news API

Install dependencies with `pip install -r requirements.txt` using Python 3.10+.
Run with `uvicorn main:app --reload`. API documentation: `/docs`.

Only model definitions have been added. No migrations, table creation, or
database configuration changes are included. The endpoints require the tables
to exist before use.

- `POST /categories`: `{"name": "automotive"}`. Names are trimmed and stored
  in lowercase; duplicates return 409.
- `GET /categories`: list categories.
- `POST /articles`: supply `company_name`, `title`, `url`, and `content`.
  Returns 201 with status `pending`, null category, and null summary.
  Only HTTP/HTTPS URLs are accepted. URLs are normalized by Pydantic before
  checking uniqueness; duplicate URLs return 409, including concurrent inserts
  once the declared unique constraint exists in the database.
- `GET /articles?offset=0&limit=20&company_name=Example&status=pending`:
  newest first, exact company-name filter, optional status filter.
  Limit must be 1–100. Invalid request fields return 422.

Each article optionally references one category through `category_id`.
Statuses are `pending`, `processing`, `completed`, and `failed`.

`utils.classify_article(title, content)` matches whole-word keywords in the
order automotive, technology, healthcare, finance, business, with `general`
as the fallback. It returns a category name without writing to the database.
`utils.summarize_article(content)` selects the first two sentences and limits
the result to 300 characters; empty content returns an empty string.
These functions can later be replaced with ML/LLM adapters preserving their
input/output contracts. They are intentionally not called by article creation;
asynchronous processing and Celery integration are outside this step.
