-- WallStreets local database bootstrap (run once)

CREATE TABLE IF NOT EXISTS branch (
    branch_code INTEGER PRIMARY KEY,
    city VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS adminusers (
    f_name VARCHAR NOT NULL,
    l_name VARCHAR,
    user_id INTEGER PRIMARY KEY NOT NULL,
    user_password VARCHAR NOT NULL,
    e_mail VARCHAR NOT NULL,
    phone_number NUMERIC(14) NOT NULL,
    branch_code INTEGER NOT NULL REFERENCES branch(branch_code),
    user_type VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    user_id VARCHAR NOT NULL PRIMARY KEY,
    f_name VARCHAR NOT NULL,
    l_name VARCHAR,
    contact NUMERIC(14) NOT NULL,
    email VARCHAR NOT NULL,
    pass VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    prod_id INT NOT NULL PRIMARY KEY,
    catogary VARCHAR NOT NULL,
    price NUMERIC NOT NULL,
    pro_type VARCHAR NOT NULL,
    pro_location VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    p_size INT NOT NULL,
    description VARCHAR,
    upload_from INTEGER REFERENCES adminusers(user_id)
);

CREATE TABLE IF NOT EXISTS invoice (
    branch_code INTEGER NOT NULL REFERENCES branch(branch_code),
    income INTEGER,
    expences INTEGER,
    upload_date DATE
);

CREATE TABLE IF NOT EXISTS employees (
    ename VARCHAR,
    eid INTEGER PRIMARY KEY,
    brcode INTEGER REFERENCES branch(branch_code),
    salary INTEGER
);

CREATE TABLE IF NOT EXISTS backupadmin (
    fname VARCHAR,
    user_id INTEGER,
    e_mail VARCHAR,
    phone NUMERIC(14),
    branch_code INTEGER REFERENCES branch(branch_code)
);

CREATE TABLE IF NOT EXISTS current_login_user (
    c_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES adminusers(user_id),
    user_name VARCHAR,
    branch_code INTEGER REFERENCES branch(branch_code)
);

CREATE OR REPLACE FUNCTION GET_PASS(U_ID INT)
RETURNS VARCHAR AS $$
DECLARE
    CHECK_PASS VARCHAR;
BEGIN
    SELECT user_password INTO CHECK_PASS FROM adminusers WHERE user_id = $1;
    RETURN CHECK_PASS;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GET_type(U_ID INT)
RETURNS VARCHAR AS $$
DECLARE
    user_t VARCHAR;
BEGIN
    SELECT user_type INTO user_t FROM adminusers WHERE user_id = $1;
    RETURN user_t;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GET_customers_PASS(U_ID VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    CHECK_PASS VARCHAR;
BEGIN
    SELECT pass INTO CHECK_PASS FROM customers WHERE user_id = $1;
    RETURN CHECK_PASS;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_products(
    cat VARCHAR,
    price INTEGER,
    p_type VARCHAR,
    p_loc VARCHAR,
    address VARCHAR,
    p_size INTEGER,
    p_decription VARCHAR
)
RETURNS INTEGER AS $$
DECLARE
    p_id INTEGER;
    cur_user INTEGER;
BEGIN
    SELECT COUNT(prod_id) INTO p_id FROM products;
    SELECT user_id INTO cur_user FROM current_login_user WHERE c_id = 1;
    INSERT INTO products VALUES (p_id + 1, cat, price, p_type, p_loc, address, p_size, p_decription, cur_user);
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE add_invoice(branch_code INTEGER, income INTEGER, expences INTEGER)
LANGUAGE SQL
AS $$
    INSERT INTO invoice VALUES (branch_code, income, expences, CURRENT_DATE);
$$;

CREATE OR REPLACE PROCEDURE update_current_user(u_id INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    b_code INTEGER;
    u_name VARCHAR;
BEGIN
    SELECT branch_code INTO b_code FROM adminusers WHERE user_id = u_id;
    SELECT CONCAT(f_name, ' ', l_name) INTO u_name FROM adminusers WHERE user_id = u_id;
    UPDATE current_login_user
    SET user_id = u_id, user_name = u_name, branch_code = b_code
    WHERE c_id = 1;
END;
$$;

CREATE OR REPLACE PROCEDURE paysal(b_id INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    sum_sal INTEGER;
BEGIN
    SELECT COALESCE(SUM(salary), 0) INTO sum_sal FROM employees WHERE brcode = b_id;
    CALL add_invoice(b_id, sum_sal, 0);
END;
$$;

CREATE OR REPLACE VIEW current_invoice AS
SELECT * FROM invoice
WHERE branch_code = (SELECT branch_code FROM current_login_user WHERE c_id = 1);

-- Seed data (idempotent inserts)
INSERT INTO branch (branch_code, city) VALUES (1, 'Islamabad'), (2, 'Lahore')
ON CONFLICT (branch_code) DO NOTHING;

INSERT INTO adminusers (f_name, l_name, user_id, user_password, e_mail, phone_number, branch_code, user_type)
VALUES ('Admin', 'CEO', 1, 'ceo123', 'ceo@wallstreets.com', 923001234567, 1, 'CEO')
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO current_login_user (c_id, user_id, user_name, branch_code)
VALUES (1, 1, 'Admin CEO', 1)
ON CONFLICT (c_id) DO NOTHING;

INSERT INTO products (prod_id, catogary, price, pro_type, pro_location, address, p_size, description, upload_from)
VALUES
    (1, 'Shop', 10000, 'Rent', 'Islamabad', '456 Avenue Main Boulevard', 120, 'A 120 ft square shop available for rent', 1),
    (2, 'Plot', 250000, 'Sale', 'Lahore', 'DHA Phase V Sector J', 5500, 'A 1 Kanal Plot available in Prime Location', 1)
ON CONFLICT (prod_id) DO NOTHING;

INSERT INTO customers (user_id, f_name, l_name, contact, email, pass)
VALUES ('1', 'Ahmed', 'Ali', 321543678, 'ahmed@gmail.com', '12347')
ON CONFLICT (user_id) DO NOTHING;
