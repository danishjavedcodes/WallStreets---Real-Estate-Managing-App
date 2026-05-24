from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    user_id = StringField("User ID", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
    submit = SubmitField("Sign In")


class CustomerRegisterForm(FlaskForm):
    f_name = StringField("First Name", validators=[DataRequired(), Length(max=80)])
    l_name = StringField("Last Name", validators=[Optional(), Length(max=80)])
    user_id = StringField("User ID", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    contact = StringField("Phone", validators=[DataRequired(), Length(min=10, max=14)])
    submit = SubmitField("Create Account")


class PropertyForm(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            ("Plot", "Plot"),
            ("House", "House"),
            ("Shop", "Shop"),
            ("Mall", "Mall"),
            ("Apartment", "Apartment"),
            ("Commercial", "Commercial"),
        ],
        validators=[DataRequired()],
    )
    price = DecimalField("Price (PKR)", validators=[DataRequired(), NumberRange(min=1)])
    pro_type = SelectField(
        "Listing Type",
        choices=[("Sale", "For Sale"), ("Rent", "For Rent")],
        validators=[DataRequired()],
    )
    pro_location = StringField("City", validators=[DataRequired(), Length(max=120)])
    address = StringField("Address", validators=[DataRequired(), Length(max=255)])
    p_size = IntegerField("Size (sq ft)", validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Publish Listing")


class BranchForm(FlaskForm):
    branch_code = IntegerField("Branch Code", validators=[DataRequired(), NumberRange(min=1)])
    city = StringField("City", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Open Branch")


class HodForm(FlaskForm):
    f_name = StringField("First Name", validators=[DataRequired(), Length(max=80)])
    l_name = StringField("Last Name", validators=[Optional(), Length(max=80)])
    user_id = IntegerField("User ID", validators=[DataRequired(), NumberRange(min=2)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone", validators=[DataRequired(), Length(min=10, max=14)])
    branch_code = SelectField("Branch", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Register HOD")


class DeleteHodForm(FlaskForm):
    user_id = IntegerField("HOD User ID", validators=[DataRequired(), NumberRange(min=2)])
    submit = SubmitField("Remove HOD")


class EmployeeForm(FlaskForm):
    ename = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    eid = IntegerField("Employee ID", validators=[DataRequired(), NumberRange(min=1)])
    brcode = SelectField("Branch", coerce=int, validators=[DataRequired()])
    salary = IntegerField("Monthly Salary (PKR)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add Employee")


class InvoiceForm(FlaskForm):
    income = IntegerField("Income (PKR)", validators=[DataRequired(), NumberRange(min=0)])
    expences = IntegerField("Expenses (PKR)", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Record Entry")


class PropertySearchForm(FlaskForm):
    q = StringField("Search", validators=[Optional(), Length(max=120)])
    category = SelectField(
        "Category",
        choices=[
            ("", "All categories"),
            ("Plot", "Plot"),
            ("House", "House"),
            ("Shop", "Shop"),
            ("Mall", "Mall"),
            ("Apartment", "Apartment"),
            ("Commercial", "Commercial"),
        ],
        validators=[Optional()],
    )
    pro_type = SelectField(
        "Type",
        choices=[("", "All types"), ("Sale", "Sale"), ("Rent", "Rent")],
        validators=[Optional()],
    )
    city = StringField("City", validators=[Optional(), Length(max=120)])
    submit = SubmitField("Search")
