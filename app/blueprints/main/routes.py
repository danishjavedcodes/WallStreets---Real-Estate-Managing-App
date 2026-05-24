from flask import render_template

from app.blueprints.main import bp
from app.models import Product
from app.services import dashboard_stats


@bp.route("/")
def index():
    stats = dashboard_stats()
    featured = Product.query.order_by(Product.prod_id.desc()).limit(6).all()
    return render_template("main/index.html", stats=stats, featured=featured)


@bp.route("/about")
def about():
    return render_template("main/about.html")
