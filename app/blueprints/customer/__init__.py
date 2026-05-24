from flask import Blueprint

bp = Blueprint("customer", __name__)

from app.blueprints.customer import routes  # noqa: E402, F401
