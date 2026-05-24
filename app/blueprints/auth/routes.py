from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from app.blueprints.auth import bp
from app.extensions import db
from app.forms import CustomerRegisterForm, LoginForm
from app.models import AdminUser, Customer


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data.strip()
        password = form.password.data

        admin = AdminUser.query.get(int(user_id)) if user_id.isdigit() else None
        if admin and admin.check_password(password):
            login_user(admin, remember=True)
            flash(f"Welcome back, {admin.full_name}.", "success")
            return redirect(url_for("admin.dashboard"))

        customer = Customer.query.get(user_id)
        if customer and customer.check_password(password):
            login_user(customer, remember=True)
            flash(f"Welcome, {customer.full_name}.", "success")
            return redirect(url_for("customer.dashboard"))

        flash("Invalid user ID or password.", "danger")

    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        if Customer.query.get(form.user_id.data.strip()):
            flash("This user ID is already taken.", "warning")
        elif Customer.query.filter_by(email=form.email.data.lower()).first():
            flash("An account with this email already exists.", "warning")
        else:
            customer = Customer(
                user_id=form.user_id.data.strip(),
                f_name=form.f_name.data.strip(),
                l_name=(form.l_name.data or "").strip(),
                email=form.email.data.lower().strip(),
                contact=form.contact.data.strip(),
            )
            customer.set_password(form.password.data)
            db.session.add(customer)
            db.session.commit()
            flash("Account created. You can sign in now.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))
