create table adminusers(f_name varchar not null,
						l_name varchar,
						user_id integer primary key not null,
						user_password varchar not null,
						e_mail varchar not null,
						phone_number numeric (14) not null,
						branch_code integer not null,
						user_type varchar not null);
CREATE FUNCTION CHECK_PASS(U_ID INT, PASS VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE 
	CHECK_PASS BOOLEAN;
BEGIN
	SELECT (user_password = $2) into CHECK_PASS
	FROM adminusers
	where user_id = $1;
	return CHECK_PASS;
END;
$$  LANGUAGE plpgsql

select * from adminusers

CREATE FUNCTION create_Adminuser(f_name,l_name,user_id,user_password,e_mail,phone_number,branch_code,user_type)
BEGIN
	insert into adminusers values ($1,$2,$3,$4,$5,$6,$7,$8)
END;
select * from adminusers
