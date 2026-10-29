# Flask Pagination Lab

A Flask API that returns books from a SQLAlchemy database in pages instead of all at once.

## Setup

```bash
pipenv install && pipenv shell
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
python seed.py
python app.py
```

The server runs at http://localhost:5555. The seed script creates 500 fake books.

## Endpoint

`GET /books`

| Query param | Default | Notes |
|-------------|---------|-------|
| `page`      | 1       | Values below 1 are treated as 1 |
| `per_page`  | 5       | Clamped between 1 and 100 |

Books are ordered by `id`. Invalid values fall back to the defaults. A page past the end returns an empty `items` list with a 200 status.

### Example

```
GET /books?page=2&per_page=3
```

```json
{
  "page": 2,
  "per_page": 3,
  "total": 500,
  "total_pages": 167,
  "items": [
    { "id": 4, "title": "...", "author": "...", "description": "..." },
    { "id": 5, "title": "...", "author": "...", "description": "..." },
    { "id": 6,