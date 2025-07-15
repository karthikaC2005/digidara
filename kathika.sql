create schema feedback_db;
-- Create the database
CREATE DATABASE feedback_db;
USE feedback_db;

-- Create students table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password TEXT
);

-- Create admins table
CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(100)
);
drop table feedbacks;

-- Insert one admin login
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Create feedbacks table
CREATE TABLE feedbacks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    rating_teaching INT,
    rating_communication INT,
    rating_punctuality INT,
    comment TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
ALTER TABLE feedbacks
ADD staff_name VARCHAR(100),
ADD department VARCHAR(100);
CREATE TABLE feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    staff_name VARCHAR(100),
    department VARCHAR(100),
    rating_teaching INT,
    rating_communication INT,
    rating_punctuality INT,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
CREATE TABLE feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    staff_name VARCHAR(100),
    department VARCHAR(100),
    rating_teaching INT,
    rating_communication INT,
    rating_punctuality INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
CREATE TABLE feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    staff_name VARCHAR(100),
    department VARCHAR(100),
    rating_teaching INT,
    rating_communication INT,
    rating_punctuality INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
CREATE TABLE feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    staff_name VARCHAR(100),
    department VARCHAR(100),
    rating_teaching INT,
    rating_communication INT,
    rating_punctuality INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
