create database banking_app_sql;
use banking_app_sql;

create table acc_register(
account_number int primary key auto_increment,
user_name varchar(50),
date_of_birth varchar(10),
phone_number varchar(11),
native_place varchar(50),
state varchar(20),
pin varchar(4),
upi_pin varchar(6)
);
select*from acc_register;

alter table acc_register add column saving_amount int ;

