#!/usr/bin/env python3

import os

from flask import request
from flask_restful import Resource

# db is not used here, but testing/pagination_test.py imports it from app
from config import create_app, db, api
from models import Book, BookSchema

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 5
MAX_PER_PAGE = 100


class Books(Resource):
    def get(self):
        # Read query params. Non-integer values fall back to the defaults.
        page = request.args.get("page", DEFAULT_PAGE, type=int)
        per_page = request.args.get("per_page", DEFAULT_PER_PAGE, type=int)

        # Keep values in a sane range
        page = max(page, 1)
        per_page = min(max(per_page, 1), MAX_PER_PAGE)

        # Order by id so pages are stable. error_out=False returns an
        # empty list for a page past the end instead of raising a 404.
        pagination = Book.query.order_by(Book.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": BookSchema(many=True).dump(pagination.items),
        }, 200


# Register the resource before creating the app so every app made by
# create_app (dev and test) gets the route.
api.add_resource(Books, "/books", endpoint="books")

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
