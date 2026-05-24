from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.blueprints.admin import bp
from app.decorators import admin_required
from app.extensions import db
from app.forms import (
    BranchForm,
    DeleteHodForm,
    EmployeeForm,
    HodForm,
    InvoiceForm,
    PropertyForm,
)
from app.models import AdminUser, Branch, Employee, Invoice, Product
from app.services import (
    add_invoice_entry,
    create_property,
    dashboard_stats,
    delete_hod,
    pay_branch_salaries,
)


@bp.route("/dashboard")
@login_required
@admin_required("CEO", "HOD")
def dashboard():
    branch_code = None if current_user.is_ceo else current_user.branch_code
    stats = dashboard_stats(branch_code=branch_code)
    recent_properties = (
        Product.query.join(AdminUser)
        .filter(AdminUser.branch_code == current_user.branch_code)
        .order_by(Product.prod_id.desc())
        .limit(5)
        .all()
        if current_user.is_hod
        else Product.query.order_by(Product.prod_id.desc()).limit(5).all()
    )
    invoice_q = Invoice.query
    if current_user.is_hod:
        invoice_q = invoice_q.filter_by(branch_code=current_user.branch_code)
    recent_invoices = invoice_q.order_by(Invoice.upload_date.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_properties=recent_properties,
        recent_invoices=recent_invoices,
    )


@bp.route("/properties", methods=["GET", "POST"])
@login_required
@admin_required("CEO", "HOD")
def properties():
    form = PropertyForm()
    if form.validate_on_submit():
        create_property(
            current_user,
            {
                "category": form.category.data,
                "price": form.price.data,
                "pro_type": form.pro_type.data,
                "pro_location": form.pro_location.data,
                "address": form.address.data,
                "p_size": form.p_size.data,
                "description": form.description.data,
            },
        )
        flash("Property published successfully.", "success")
        return redirect(url_for("admin.properties"))

    listings = (
        Product.query.join(AdminUser)
        .filter(AdminUser.branch_code == current_user.branch_code)
        .order_by(Product.prod_id.desc())
        .all()
        if current_user.is_hod
        else Product.query.order_by(Product.prod_id.desc()).all()
    )
    return render_template("admin/properties.html", form=form, listings=listings)


@bp.route("/branches", methods=["GET", "POST"])
@login_required
@admin_required("CEO")
def branches():
    form = BranchForm()
    if form.validate_on_submit():
        if Branch.query.get(form.branch_code.data):
            flash("Branch code already exists.", "warning")
        else:
            db.session.add(Branch(branch_code=form.branch_code.data, city=form.city.data.strip()))
            db.session.commit()
            flash("Branch opened successfully.", "success")
            return redirect(url_for("admin.branches"))
    branches_list = Branch.query.order_by(Branch.branch_code).all()
    return render_template("admin/branches.html", form=form, branches=branches_list)


@bp.route("/hods", methods=["GET", "POST"])
@login_required
@admin_required("CEO")
def hods():
    hod_form = HodForm()
    delete_form = DeleteHodForm()
    hod_form.branch_code.choices = [
        (b.branch_code, f"{b.city} (#{b.branch_code})") for b in Branch.query.order_by(Branch.city)
    ]

    if request.form.get("form_type") == "register" and hod_form.validate_on_submit():
        if AdminUser.query.get(hod_form.user_id.data):
            flash("User ID already in use.", "warning")
        else:
            hod = AdminUser(
                user_id=hod_form.user_id.data,
                f_name=hod_form.f_name.data.strip(),
                l_name=(hod_form.l_name.data or "").strip(),
                e_mail=hod_form.email.data.lower(),
                phone_number=hod_form.phone_number.data,
                branch_code=hod_form.branch_code.data,
                user_type="HOD",
            )
            hod.set_password(hod_form.password.data)
            db.session.add(hod)
            db.session.commit()
            flash("HOD registered successfully.", "success")
            return redirect(url_for("admin.hods"))

    if request.form.get("form_type") == "delete" and delete_form.validate_on_submit():
        ok, message = delete_hod(delete_form.user_id.data)
        flash(message, "success" if ok else "danger")
        return redirect(url_for("admin.hods"))

    hods_list = AdminUser.query.filter_by(user_type="HOD").order_by(AdminUser.user_id).all()
    return render_template(
        "admin/hods.html",
        hod_form=hod_form,
        delete_form=delete_form,
        hods=hods_list,
    )


@bp.route("/employees", methods=["GET", "POST"])
@login_required
@admin_required("CEO", "HOD")
def employees():
    form = EmployeeForm()
    branches = Branch.query.order_by(Branch.city).all()
    if current_user.is_hod:
        form.brcode.choices = [(current_user.branch_code, current_user.branch.city)]
    else:
        form.brcode.choices = [(b.branch_code, b.city) for b in branches]

    if form.validate_on_submit():
        if Employee.query.get(form.eid.data):
            flash("Employee ID already exists.", "warning")
        else:
            db.session.add(
                Employee(
                    eid=form.eid.data,
                    ename=form.ename.data.strip(),
                    brcode=form.brcode.data,
                    salary=form.salary.data,
                )
            )
            db.session.commit()
            flash("Employee added successfully.", "success")
            return redirect(url_for("admin.employees"))

    q = Employee.query
    if current_user.is_hod:
        q = q.filter_by(brcode=current_user.branch_code)
    employees_list = q.order_by(Employee.eid).all()
    return render_template("admin/employees.html", form=form, employees=employees_list)


@bp.route("/invoices", methods=["GET", "POST"])
@login_required
@admin_required("CEO", "HOD")
def invoices():
    form = InvoiceForm()
    branch_code = current_user.branch_code

    if form.validate_on_submit():
        add_invoice_entry(branch_code, form.income.data, form.expences.data)
        flash("Invoice entry recorded.", "success")
        return redirect(url_for("admin.invoices"))

    invoice_q = Invoice.query.filter_by(branch_code=branch_code)
    if current_user.is_ceo:
        invoice_q = Invoice.query
    invoices_list = invoice_q.order_by(Invoice.upload_date.desc()).all()
    return render_template("admin/invoices.html", form=form, invoices=invoices_list)


@bp.route("/payroll", methods=["POST"])
@login_required
@admin_required("CEO", "HOD")
def payroll():
    total = pay_branch_salaries(current_user.branch_code)
    if total:
        flash(f"Salary payout recorded: PKR {total:,} expensed for your branch.", "success")
    else:
        flash("No employees found for this branch.", "info")
    return redirect(url_for("admin.invoices"))
