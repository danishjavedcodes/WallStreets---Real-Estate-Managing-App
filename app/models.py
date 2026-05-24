from datetime import date, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class Branch(db.Model):
    __tablename__ = "branch"

    branch_code = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)

    admins = db.relationship("AdminUser", back_populates="branch", lazy="dynamic")
    employees = db.relationship("Employee", back_populates="branch", lazy="dynamic")
    invoices = db.relationship("Invoice", back_populates="branch", lazy="dynamic")

    def __repr__(self):
        return f"<Branch {self.branch_code} {self.city}>"


class AdminUser(UserMixin, db.Model):
    __tablename__ = "adminusers"

    user_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(80), nullable=False)
    l_name = db.Column(db.String(80))
    user_password = db.Column(db.String(255), nullable=False)
    e_mail = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.Numeric(14), nullable=False)
    branch_code = db.Column(db.Integer, db.ForeignKey("branch.branch_code"), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # CEO | HOD

    branch = db.relationship("Branch", back_populates="admins")
    products = db.relationship("Product", back_populates="uploader", lazy="dynamic")

    def get_id(self):
        return f"admin:{self.user_id}"

    @property
    def full_name(self):
        return f"{self.f_name} {self.l_name or ''}".strip()

    @property
    def is_ceo(self):
        return self.user_type == "CEO"

    @property
    def is_hod(self):
        return self.user_type == "HOD"

    def set_password(self, password: str) -> None:
        self.user_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if password is None:
            return False
        stored = self.user_password or ""
        if stored.startswith(("pbkdf2:", "scrypt:")):
            return check_password_hash(stored, password)
        return stored == password


class Customer(UserMixin, db.Model):
    __tablename__ = "customers"

    user_id = db.Column(db.String(64), primary_key=True)
    f_name = db.Column(db.String(80), nullable=False)
    l_name = db.Column(db.String(80))
    contact = db.Column(db.Numeric(14), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    pass_field = db.Column("pass", db.String(255), nullable=False)

    def get_id(self):
        return f"customer:{self.user_id}"

    @property
    def full_name(self):
        return f"{self.f_name} {self.l_name or ''}".strip()

    def set_password(self, password: str) -> None:
        self.pass_field = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if password is None:
            return False
        stored = self.pass_field or ""
        if stored.startswith(("pbkdf2:", "scrypt:")):
            return check_password_hash(stored, password)
        return stored == password


class Product(db.Model):
    __tablename__ = "products"

    prod_id = db.Column(db.Integer, primary_key=True)
    catogary = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    pro_type = db.Column(db.String(20), nullable=False)
    pro_location = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    p_size = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    upload_from = db.Column(db.Integer, db.ForeignKey("adminusers.user_id"))

    uploader = db.relationship("AdminUser", back_populates="products")

    @property
    def formatted_price(self):
        return f"PKR {float(self.price):,.0f}"


class Invoice(db.Model):
    __tablename__ = "invoice"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_code = db.Column(db.Integer, db.ForeignKey("branch.branch_code"), nullable=False)
    income = db.Column(db.Integer, default=0)
    expences = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.Date, default=date.today)

    branch = db.relationship("Branch", back_populates="invoices")

    @property
    def net(self):
        return (self.income or 0) - (self.expences or 0)


class Employee(db.Model):
    __tablename__ = "employees"

    eid = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(120), nullable=False)
    brcode = db.Column(db.Integer, db.ForeignKey("branch.branch_code"), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    branch = db.relationship("Branch", back_populates="employees")


class BackupAdmin(db.Model):
    __tablename__ = "backupadmin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(160))
    user_id = db.Column(db.Integer)
    e_mail = db.Column(db.String(120))
    phone = db.Column(db.Numeric(14))
    branch_code = db.Column(db.Integer)
