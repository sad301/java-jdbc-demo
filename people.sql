drop database if exists people;
create database people;
use people;

create table person (
    id int not null,
    user_id varchar(16) not null,
    first_name varchar(64) not null,
    last_name varchar(16) not null,
    sex enum('Male', 'Female') not null,
    email varchar(32) not null,
    phone varchar(32) not null,
    birth_date date not null,
    job_title varchar(128) not null,
    primary key (id),
    unique (user_id)
);

-- import csv file

load data infile '/var/lib/mysql-files/people-100.csv'
into table person
fields terminated by ','
optionally enclosed by '"'
lines terminated by '\r\n'
ignore 1 rows;
