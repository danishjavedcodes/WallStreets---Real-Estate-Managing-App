from datetime import date

from sqlalchemy import func

from app.extensions import db
from app.models import AdminUser, BackupAdmin, Branch, Customer, Employee, Invoice, Product


def dashboard_stats(branch_code=None):
    product_q = Product.query
    invoice_q = Invoice.query
    employee_q = Employee.query

    if branch_code is not None:
        product_q = product_q.join(AdminUser).filter(AdminUser.branch_code == branch_code)
        invoice_q = invoice_q.filter(Invoice.branch_code == branch_code)
        employee_q = employee_q.filter(Employee.brcode == branch_code)

    total_income = db.session.query(func.coalesce(func.sum(Invoice.income), 0)).scalar() or 0
    total_expenses = db.session.query(func.coalesce(func.sum(Invoice.expences), 0)).scalar() or 0

    if branch_code is not None:
        total_income = (
            db.session.query(func.coalesce(func.sum(Invoice.income), 0))
            .filter(Invoice.branch_code == branch_code)
            .scalar()
            or 0
        )
        total_expenses = (
            db.session.query(func.coalesce(func.sum(Invoice.expences), 0))
            .filter(Invoice.branch_code == branch_code)
            .scalar()
            or 0
        )

    return {
        "properties": product_q.count(),
        "branches": Branch.query.count() if branch_code is None else 1,
        "employees": employee_q.count(),
        "customers": Customer.query.count(),
        "total_income": int(total_income),
        "total_expenses": int(total_expenses),
        "net_revenue": int(total_income) - int(total_expenses),
    }


def create_property(admin: AdminUser, data: dict) -> Product:
    next_id = (db.session.query(func.max(Product.prod_id)).scalar() or 0) + 1
    product = Product(
        prod_id=next_id,
        catogary=data["category"],
        price=data["price"],
        pro_type=data["pro_type"],
        pro_location=data["pro_location"],
        address=data["address"],
        p_size=data["p_size"],
        description=data.get("description"),
        upload_from=admin.user_id,
    )
    db.session.add(product)
    db.session.commit()
    return product


def add_invoice_entry(branch_code: int, income: int, expenses: int) -> Invoice:
    invoice = Invoice(
        branch_code=branch_code,
        income=income,
        expences=expenses,
        upload_date=date.today(),
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice


def pay_branch_salaries(branch_code: int) -> int:
    total = (
        db.session.query(func.coalesce(func.sum(Employee.salary), 0))
        .filter(Employee.brcode == branch_code)
        .scalar()
        or 0
    )
    if total > 0:
        add_invoice_entry(branch_code, income=0, expenses=int(total))
    return int(total)


def delete_hod(user_id: int) -> tuple[bool, str]:
    if user_id == 1:
        return False, "The CEO account cannot be deleted."
    admin = AdminUser.query.get(user_id)
    if not admin:
        return False, "User not found."
    if admin.user_type != "HOD":
        return False, "Only HOD accounts can be removed from this screen."
    backup = BackupAdmin(
        fname=admin.full_name,
        user_id=admin.user_id,
        e_mail=admin.e_mail,
        phone=admin.phone_number,
        branch_code=admin.branch_code,
    )
    db.session.add(backup)
    db.session.delete(admin)
    db.session.commit()
    return True, "HOD removed successfully."


def search_properties(query=None, category=None, listing_type=None, city=None):
    q = Product.query
    if query:
        like = f"%{query}%"
        q = q.filter(
            db.or_(
                Product.catogary.ilike(like),
                Product.pro_location.ilike(like),
                Product.address.ilike(like),
                Product.description.ilike(like),
            )
        )
    if category:
        q = q.filter(Product.catogary.ilike(f"%{category}%"))
    if listing_type:
        q = q.filter(Product.pro_type.ilike(listing_type))
    if city:
        q = q.filter(Product.pro_location.ilike(f"%{city}%"))
    return q.order_by(Product.prod_id.desc()).all()
