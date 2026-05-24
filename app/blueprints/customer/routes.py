from flask import render_template
from flask_login import current_user

from app.blueprints.customer import bp
from app.decorators import customer_required
from app.forms import PropertySearchForm
from app.services import search_properties


@bp.route("/dashboard")
@customer_required
def dashboard():
    form = PropertySearchForm()
    properties = search_properties()
    return render_template(
        "customer/dashboard.html",
        user=current_user,
        form=form,
        properties=properties,
    )


@bp.route("/properties")
@customer_required
def properties():
    form = PropertySearchForm()
    if form.validate_on_submit() or any(
        request_arg in form.data
        for request_arg in ("q", "category", "pro_type", "city")
    ):
        pass
    from flask import request

    form = PropertySearchForm(request.args, meta={"csrf": False})
    properties = search_properties(
        query=form.q.data,
        category=form.category.data or None,
        listing_type=form.pro_type.data or None,
        city=form.city.data or None,
    )
    return render_template(
        "customer/properties.html",
        user=current_user,
        form=form,
        properties=properties,
    )
