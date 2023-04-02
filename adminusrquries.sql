-------------------BY Danish Javed-------------------
-- create table branch(branch_code integer primary key, city varchar);

-- create table adminusers(f_name varchar not null,
-- 						l_name varchar,
-- 						user_id integer primary key not null,
-- 						user_password varchar not null,
-- 						e_mail varchar not null,
-- 						phone_number numeric (14) not null,
-- 						branch_code integer not null references branch(branch_code),
-- 						user_type varchar not null);
-- CREATE FUNCTION CHECK_PASS(U_ID INT, PASS VARCHAR)
-- RETURNS BOOLEAN AS $$
-- DECLARE 
-- 	CHECK_PASS BOOLEAN;
-- BEGIN
-- 	SELECT (user_password = $2) into CHECK_PASS
-- 	FROM adminusers
-- 	where user_id = $1;
-- 	return CHECK_PASS;
-- END;
-- $$  LANGUAGE plpgsql

-- select * from adminusers

-- CREATE FUNCTION create_Adminuser(f_name,l_name,user_id,user_password,e_mail,phone_number,branch_code,user_type)
-- BEGIN
-- 	insert into adminusers values ($1,$2,$3,$4,$5,$6,$7,$8)
-- END;
-- select * from adminusers

-- CREATE FUNCTION GET_PASS(U_ID INT)
-- RETURNS VARCHAR AS $$
-- DECLARE 
-- 	CHECK_PASS VARCHAR;
-- BEGIN
-- 	SELECT user_password into CHECK_PASS
-- 	FROM adminusers
-- 	where user_id = $1;
-- 	return CHECK_PASS;
-- END;
-- $$  LANGUAGE plpgsql

-- CREATE FUNCTION GET_type(U_ID INT)
-- RETURNS VARCHAR AS $$
-- DECLARE 
-- 	user_t VARCHAR;
-- BEGIN
-- 	SELECT user_type into user_t
-- 	FROM adminusers
-- 	where user_id = $1;
-- 	return user_t;
-- END;
-- $$  LANGUAGE plpgsql



------------------by Ali -------------------
-- create table products
-- (
-- 	catogary varchar not null,
-- 	prod_id int not null,
-- 	price int not null,
-- 	pro_type varchar not null,
-- 	pro_location varchar not null,
-- 	address varchar not null,
-- 	p_size int not null,
--  primary key(prod_id)
-- );


--create table description 
--(
--	prod_id int,
--	constraint fk_prod_id foreign key(prod_id) references products(prod_id),
--	descrip varchar
--)


-- create table customers
-- (
-- 	username varchar not null,
-- 	f_name varchar not null,
-- 	l_name varchar not null,
-- 	contact numeric(14) not null,
-- 	email varchar not null,
-- 	primary key(username)
-- )


------------------BY DANISH----------------

-- drop table customers

--create table customers
-- (
-- 	user_id varchar not null primary key,
-- 	f_name varchar not null,
-- 	l_name varchar,
-- 	contact numeric(14) not null,
-- 	email varchar not null,
-- 	pass varchar not null
-- )


-- CREATE FUNCTION GET_customers_PASS(U_ID varchar)
-- RETURNS VARCHAR AS $$
-- DECLARE 
-- 	CHECK_PASS VARCHAR;
-- BEGIN
-- 	SELECT pass into CHECK_PASS
-- 	FROM customers
-- 	where user_id = $1;
-- 	return CHECK_PASS;
-- END;
-- $$  LANGUAGE plpgsql


-- create table products
-- (
-- 	prod_id int not null primary key,
-- 	catogary varchar not null,
-- 	price int not null,
-- 	pro_type varchar not null,
-- 	pro_location varchar not null,
-- 	address varchar not null,
-- 	p_size int not null,
--  description varchar,
-- 	upload_from integer,
-- 	constraint fk_prod_id foreign key(upload_from) references adminusers(user_id)
-- );


-- CREATE or REPLACE FUNCTION add_products(cat varchar, price integer, p_type varchar, p_loc varchar, address varchar, p_size integer, p_decription varchar)
-- RETURNS integer AS $$
-- DECLARE 
-- 	p_id integer;
-- 	cur_user integer;
-- BEGIN
-- 	select count(prod_id) into p_id from products;
-- 	select user_id into cur_user from current_login_user where c_id=1;
-- 	insert into products values (p_id+1, cat, price, p_type, p_loc, address, p_size, p_decription, cur_user);
-- 	return p_id;
-- END;
-- $$  LANGUAGE plpgsql


-- create table invoice
-- (
-- 	branch_code integer not null references branch(branch_code),
-- 	income integer,
-- 	expences integer,
-- 	upload_date DATE
-- );


-- create procedure add_invoice(branch_code integer, income integer, expences integer)
-- LANGUAGE SQL
-- as $$
--   insert into invoice values (branch_code, income, expences, CURRENT_DATE);
-- $$;


--BY SHURAHBEEL
-- create table backupadmin(fname varchar,user_id integer, e_mail varchar, phone numeric(14),branch_code integer);
-- create function move_del()
-- returns trigger
-- language plpgsql
-- as
-- $$
-- begin 
-- insert into backupadmin values (concat(old.f_name,' ',old.l_name),old.user_id,old.e_mail,old.phone_number,old.branch_code);
-- delete from adminusers
-- where old.user_id = new.user_id;
-- return new;
-- end;
-- $$

-- create table employees(ename varchar,eid integer primary key,brcode integer,salary integer);


--create trigger movedata
-- after delete
-- on adminusers
-- for each row
-- execute function move_del();

-- create procedure paysal(b_id integer)
-- language plpgsql
-- as
-- $$
-- declare 
-- sum_Sal integer;
-- begin
-- select sum(salary) into sum_sal from employees where brcode = b_id;
-- call add_invoice(bid, sum_sal , 0);
-- end;
-- $$

-- insert into
-- 	products(prod_id,catogary,price,pro_type,pro_location,address,p_size,description,upload_from)
-- values
--  (1,'Shop',10000,'Rent','Islamabad','456 Avenue Main Boulevard',120,'A 120 ft square shop available for rent',1),
--  (2,'Plot',250000,'Sale','Lahore','DHA Phase V Sector J',5500,'A 1 Kanal Plot available in Prime Location',1),
--  (3,'Mall',250000,'Rent','Karachi','Tariq Road',550000,'A luxury mall with shops available at Tariq Road',2),
--  (4,'House',40000,'Sale','Lahore','Johar Town',11000,'A 2 Kanal house available in Prime Location',2),
--  (5,'Shop',34500,'Rent','Islamabad','Centaurus',300,'A 300 sq feet shop at Centaurus Mall Available',1),
--  (6,'Plot',50000,'Sale','Kharian','Citi Housing',11000,'A 2 Kanal Plot available in Prime Location',1);

-- alter table products
-- alter column price type numeric;

-- ALTER TABLE employees 
-- ADD CONSTRAINT constraint_name 
-- FOREIGN KEY (brcode) 
-- REFERENCES branch (branch_code);

-- ALTER TABLE backupadmin 
-- ADD CONSTRAINT constraint_name 
-- FOREIGN KEY (branch_code) 
-- REFERENCES branch (branch_code);

-- insert into
-- invoice(branch_code,income,expences,upload_date)
-- values
-- (1,15000,2100,CURRENT_DATE),
-- (2,1000,12000,CURRENT_DATE),
-- (2,1500,1200,CURRENT_DATE),
-- (1,3500,4500,CURRENT_DATE),
-- (1,1400,1200,CURRENT_DATE);

-- insert into
-- employees(ename,eid,brcode,salary)
-- values
-- ('Hassan',1,1,20000),
-- ('Ahmad',2,2,40000),
-- ('Yousaf',3,1,55000),
-- ('Zain',4,1,76000),
-- ('Hussein',2,1,81000),
-- ('Ilyas',6,2,95000);

-- insert into
-- customers(user_id,f_name,l_name,contact,email,pass)
-- values
-- (1,'Ahmed','Ali',321543678,'ahmed@gmail.com','12347'),
-- (2,'Zain','Naufal',321213456,'zain@gmail.com','2343'),
-- (3,'Hassan','Ali',32154556565,'hassan@gmail.com','34322'),
-- (4,'Bilal','Qaiser',321544321,'bilal@gmail.com','12217'),
-- (5,'Farooq','Bajwa',321345556,'farooq@gmail.com','4567');
-------------------------BY Danish Javed---------------------



-- create table current_login_user(c_id integer, user_id integer REFERENCES adminusers(user_id), user_name varchar, branch_code integer REFERENCES branch(branch_code));


-- create procedure update_current_user(u_id integer)
-- language plpgsql
-- as
-- $$
-- declare 
-- b_code integer;
-- u_name varchar;
-- begin
-- select branch_code into b_code from adminusers where user_id = u_id;
-- select concat(f_name, ' ', l_name) into u_name from adminusers where user_id = u_id;
-- update current_login_user
-- set user_id = u_id,
-- 	user_name = u_name,
-- 	branch_code = b_code
-- where c_id = 1;
-- end;
-- $$


-- create view current_invoice as 
-- select * from invoice where branch_code = (select branch_code from current_login_user where c_id = 1);


