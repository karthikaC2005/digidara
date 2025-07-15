use feedback_db;
drop table admins;
CREATE TABLE admins (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(100),
  password TEXT NOT NULL
);
CREATE TABLE student (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password TEXT NOT NULL
);
select *from students;
CREATE TABLE feedbacks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  staff_name VARCHAR(100) NOT NULL,
  department VARCHAR(50) DEFAULT 'CSE',
  rating_teaching INT NOT NULL,
  rating_communication INT NOT NULL,
  rating_punctuality INT NOT NULL,
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
insert into admins('admin','\'123');

CREATE TABLE admins (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password TEXT NOT NULL
);
INSERT INTO admins (username, password) 
VALUES ('admin', 'admin123');
