from app.extensions import db
from app.models import AdminUser, Branch, Customer, Employee, Invoice, Product


def hash_legacy_passwords():
    updated = 0
    for admin in AdminUser.query.all():
        if admin.user_password and not admin.user_password.startswith(("pbkdf2:", "scrypt:")):
            plain = admin.user_password
            admin.set_password(plain)
            updated += 1
    for customer in Customer.query.all():
        if customer.pass_field and not customer.pass_field.startswith(("pbkdf2:", "scrypt:")):
            plain = customer.pass_field
            customer.set_password(plain)
            updated += 1
    if updated:
        db.session.commit()
    return updated


def ensure_invoice_id_column():
    from sqlalchemy import inspect, text

    insp = inspect(db.engine)
    if "invoice" not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns("invoice")}
    if "id" not in cols:
        db.session.execute(
            text("ALTER TABLE invoice ADD COLUMN id SERIAL PRIMARY KEY")
        )
        db.session.commit()


def run_seed():
    ensure_invoice_id_column()
    hash_legacy_passwords()

    if not Branch.query.first():
        db.session.add_all(
            [
                Branch(branch_code=1, city="Islamabad"),
                Branch(branch_code=2, city="Lahore"),
                Branch(branch_code=3, city="Karachi"),
            ]
        )
        db.session.commit()

    if not AdminUser.query.filter_by(user_id=1).first():
        ceo = AdminUser(
            user_id=1,
            f_name="Admin",
            l_name="CEO",
            e_mail="ceo@wallstreets.com",
            phone_number=923001234567,
            branch_code=1,
            user_type="CEO",
        )
        ceo.set_password("ceo123")
        db.session.add(ceo)

    if not AdminUser.query.filter_by(user_id=2).first():
        hod = AdminUser(
            user_id=2,
            f_name="Sara",
            l_name="Khan",
            e_mail="hod.lahore@wallstreets.com",
            phone_number=923009876543,
            branch_code=2,
            user_type="HOD",
        )
        hod.set_password("hod123")
        db.session.add(hod)

    if not Customer.query.filter_by(user_id="1").first():
        customer = Customer(
            user_id="1",
            f_name="Ahmed",
            l_name="Ali",
            contact=3215436789,
            email="ahmed@gmail.com",
        )
        customer.set_password("12347")
        db.session.add(customer)

    if not Product.query.first():
        db.session.add_all(
            [
                Product(
                    prod_id=1,
                    catogary="Shop",
                    price=10000,
                    pro_type="Rent",
                    pro_location="Islamabad",
                    address="456 Avenue Main Boulevard",
                    p_size=120,
                    description="Premium retail shop in a high-footfall commercial zone.",
                    upload_from=1,
                ),
                Product(
                    prod_id=2,
                    catogary="Plot",
                    price=250000,
                    pro_type="Sale",
                    pro_location="Lahore",
                    address="DHA Phase V Sector J",
                    p_size=5500,
                    description="1 Kanal plot in a prime residential community.",
                    upload_from=1,
                ),
                Product(
                    prod_id=3,
                    catogary="House",
                    price=40000,
                    pro_type="Sale",
                    pro_location="Lahore",
                    address="Johar Town Block G",
                    p_size=11000,
                    description="Spacious 2 Kanal house with modern finishes.",
                    upload_from=2,
                ),
            ]
        )

    if not Employee.query.first():
        db.session.add_all(
            [
                Employee(eid=1, ename="Hassan Raza", brcode=1, salary=20000),
                Employee(eid=2, ename="Ahmad Ali", brcode=2, salary=40000),
                Employee(eid=3, ename="Yousaf Malik", brcode=1, salary=55000),
            ]
        )

    if not Invoice.query.first():
        db.session.add_all(
            [
                Invoice(branch_code=1, income=15000, expences=2100),
                Invoice(branch_code=2, income=10000, expences=8000),
            ]
        )

    db.session.commit()
