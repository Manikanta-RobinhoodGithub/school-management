drop database SchoolManagementSystem;
create database SchoolManagementSystem;
use SchoolManagementSystem;


create table department(
department_id int auto_increment primary key,
department_name varchar(255) not null unique
);

create table instructor(
instructor_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
experience varchar(255) not null,
department_id int,
foreign key (department_id) references department(department_id)
);



create table salaries(
salary_id int auto_increment primary key,
salary varchar(255) not null,
year varchar(255) not null,
month varchar(255) not null,
instructor_id int,
foreign key (instructor_id) references instructor(instructor_id)
);

create table subjects(
subject_id int auto_increment primary key,
subject_name varchar(255) not null,
subject_code varchar(255) not null,
department_id int,
foreign key (department_id) references department(department_id)
);

create table student(
student_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
roll_number varchar(255) not null,
status varchar(255) not null default 'unauthorized',
department_id int,
foreign key (department_id) references department(department_id)
);



create table section(
section_id int auto_increment primary key,
room_number varchar(255) not null unique,
weekday varchar(255) not null,
crn_number varchar(255) not null unique,
class_time varchar(255) not null,
number_of_students varchar(255) not null,
section_fee varchar(255) not null,
subject_id int,
instructor_id int,
foreign key (subject_id) references subjects(subject_id),
foreign key (instructor_id) references instructor(instructor_id)
);


create table enrollments(
enrollment_id int auto_increment primary key,
fee_paid varchar(255) not null default '0',
status varchar(255) not null default 'enrolled',
grade varchar(255),
attendance varchar(255),
section_id int,
student_id int,
foreign key (section_id) references section(section_id),
foreign key (student_id) references student(student_id)
);


create table transactions(
transaction_id int auto_increment primary key,
paid_amount varchar(255) not null,
date datetime not null default current_timestamp,
enrollment_id int,
foreign key (enrollment_id) references enrollments(enrollment_id)
);




