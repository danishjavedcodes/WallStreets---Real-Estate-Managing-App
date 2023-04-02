from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
app = Flask(__name__)


@app.route('/', methods=['GET', "POST"])
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template('index.html')


conn = psycopg2.connect(
    database="Wall-Street-Admin",
    user="postgres",
    password="sys",
    host="localhost",
    port="5432"
)


@app.route('/signupuser', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        user_id = request.form['user_id']
        user_password = request.form['user_password']
        e_mail = request.form['e_mail']
        contact = request.form['contact']
        query = "'" + f_name + "'" + "," + "'" + l_name + "'" + "," + str(user_id) + "," + "'" + user_password + "'" + "," + "'" + e_mail + "'" + "," + str(
            contact)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (f_name,l_name,user_id,pass,email,contact) values (" + query + ")")
        conn.commit()
        msg = "Account created successfully"
        return render_template('index.html', msg=msg)
    return render_template('index.html')


@app.route('/registerHOD')
def registerHOD():
    return render_template('register_hod.html')


@app.route('/signup_hod', methods=['GET', 'POST'])
def signup_hod():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        user_id = request.form['user_id']
        user_password = request.form['user_password']
        e_mail = request.form['e_mail']
        phone_number = request.form['phone_number']
        branch_code = request.form['branch_code']

        query = "'" + f_name + "'" + "," + "'" + l_name + "'" + "," + str(user_id) + "," + "'" + user_password + "'" + "," + "'" + e_mail + "'" + "," + str(
            phone_number) + "," + str(branch_code) + "," + "'HOD'"
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO adminusers (f_name,l_name,user_id,user_password,e_mail,phone_number,branch_code,user_type) values (" + query + ")")
        conn.commit()
        msg = "HOD Successfully Added"
        return render_template('register_hod.html', msg=msg)
    return render_template('ceo.html')


@app.route('/registerbranch')
def registerbranch():
    return render_template('open_branch.html')


@app.route('/open_branch', methods=['GET', 'POST'])
def open_branch():
    if request.method == 'POST':
        branch_code = request.form['branch_code']
        city = request.form['city']

        query = "INSERT INTO branch Values (" + \
            str(branch_code) + "," + "'" + city + "'" + ")"
        try:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            msg = "Branch Opened Successfully"
            return render_template('open_branch.html', msg=msg)
        except:
            self.connection.rollback()

    return render_template('ceo.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    # getting password match of user_id
    cur = conn.cursor()
    cur.execute("select GET_customers_PASS("+"'" + str(user_id)+"'"+")")
    result = cur.fetchall()
    conn.commit()
    query = "select * from products;"
    cur = conn.cursor()
    cur.execute(query)
    print(cur.fetchall())
    conn.commit()

    if (user_password == result[0][0]):
        return render_template('custumer.html')
    else:
        error = "invalid password or user id"
    return render_template('index.html', error=error)


@app.route('/display_products', methods=['GET'])
def display_products():
    cursor = conn.cursor()
    cursor.execute("select * from products")
    result = cursor.fetchall()
    return render_template('display_products.html', data=result)


@app.route('/invoices', methods=['GET'])
def invoices():

    cursor = conn.cursor()
    cursor.execute("select * from current_invoice")
    result = cursor.fetchall()
    # print(result[0][0])
    return render_template('invoices.html', result=result)


@app.route("/signinadminpg")
def signinadminpg():
    admins = 'signinadmin'
    return render_template('index.html', admins=admins)


@app.route('/signinadmin', methods=['GET', 'POST'])
def signinadmin():
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    # getting password match of user_id
    cur = conn.cursor()
    cur.execute("select Get_PASS("+str(user_id)+")")
    result = cur.fetchall()
    cur.execute("CALL update_current_user("+str(user_id)+")")
    conn.commit()
    cur = conn.cursor()
    cur.execute(
        "select user_name from current_login_user where user_id = ("+str(user_id)+")")
    u_name = cur.fetchone()[0]
    print(u_name)

    cur = conn.cursor()
    cur.execute("select GET_type("+str(user_id)+")")
    u_type = cur.fetchall()
    u_types = [('CEO', 'HOD')]
    if (user_password == result[0][0] and u_type[0][0] == u_types[0][0]):
        return render_template('ceo.html', u_name=u_name)
    elif (user_password == result[0][0] and u_type[0][0] == u_types[0][1]):
        return render_template('hod.html', u_name=u_name)
    else:
        error = "invalid password or user id"
        return render_template('index.html', error=error)
    return render_template('ceo.html')


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    if (request.method == 'POST'):
        category = request.form['category']
        price = request.form['price']
        pro_type = request.form['pro_type']
        pro_location = request.form['pro_location']
        address = request.form['address']
        p_size = request.form['p_size']
        details = request.form['description']
        query = "select add_products('" + category + "', " + str(price) + ", '" + pro_type + \
            "', '" + pro_location + "', '" + address + \
                "', " + str(p_size) + ", '" + details + "')"
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        msg = "Product Addedd Successfully"
        return render_template('upload_products.html', msg=msg)
    return render_template('upload_products.html')


@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        income = request.form['income']
        expences = request.form['expences']

        query = "select branch_code from adminusers where user_id = (select user_id from current_login_user) ;"
        cur = conn.cursor()
        cur.execute(query)
        branch = cur.fetchone()[0]
        cur.execute("call add_invoice(" + str(branch) + "," +
                    str(income) + "," + str(expences) + ");")
        print(branch)
        conn.commit()
        message1 = "Invoice addedd Successfully"
        return render_template('manage_invoices.html', message1=message1)
    return render_template('manage_invoices.html')


@app.route('/PaySal', methods=['POST', 'GET'])
def PaySal():

    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("select user_id from current_login_user where c_id=1")
        current_user_id = cur.fetchall()[0][0]
        print(current_user_id)
        cur.execute(
            "select branch_code from adminusers where user_id = " + str(current_user_id) + ";")
        b_id = cur.fetchall()
        conn.commit()
        id = b_id[0][0]
        print('branch', id)
        cur = conn.cursor()
        cur.execute("CALL paysal("+str(id)+");")
        conn.commit()
        message = "Sallary is Successfully Paid to all employees"
        return render_template('manage_invoices.html', message=message)
    return render_template('manage_invoices.html')


@app.route('/delete_hod', methods=['POST'])
def delete_hod():
    if methods == 'POST':
        user_id = request.form['user_id']
        if user_id == 1:
            error = "CEO Cannot be deleted"
            return render_template('register_hod.html', error=error)
        else:
            cur = conn.cursor()
            cur.execute(
                "delete from adminusers where user_id = " + user_id + ";")
            conn.commit()
            message = "Successfully Deleted"
            return render_template('register_hod.html', message=message)
    return render_template('register_hod.html')


@app.route('/add_emp', methods=['POST', 'GET'])
def add_emp():
    if request.method == 'POST':
        name = request.form['ename']
        eid = request.form['eid']
        br = request.form['brcode']
        sal = request.form['salary']
        query = "insert into employees values ('" + name + \
            "'," + eid + "," + br + "," + sal + ");"
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        message = "Employee Addedd Successfully"
        return render_template('register_employee.html', message=message)
    return render_template('register_employee.html')


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
