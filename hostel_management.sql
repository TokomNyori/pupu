DROP DATABASE IF EXISTS hostel_management2;
CREATE DATABASE hostel_management2;
USE hostel_management2;

-- 1. students Table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL
);

-- 2. hostels Table  
CREATE TABLE hostels (
    hostel_id INT PRIMARY KEY AUTO_INCREMENT,
    hostel_name VARCHAR(100) NOT NULL,
    hostel_type ENUM('Boys', 'Girls') NOT NULL,
    total_rooms INT NOT NULL
);

-- 3. rooms Table
CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    hostel_id INT NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    capacity INT NOT NULL,
    monthly_rent DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (hostel_id) REFERENCES hostels(hostel_id)
);

-- 4. accommodations ttable
CREATE TABLE accommodations (
    accommodation_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    status ENUM('Active', 'Checked Out') DEFAULT 'Active',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- 5. payments Table
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_type ENUM('Rent', 'Deposit') NOT NULL,
    status ENUM('Paid', 'Pending') DEFAULT 'Paid',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);



INSERT INTO hostels (hostel_name, hostel_type, total_rooms) VALUES
('Sunrise Boys Hostel', 'Boys', 20),
('Moonlight Girls Hostel', 'Girls', 18);

-- insert rooms
INSERT INTO rooms (hostel_id, room_number, capacity, monthly_rent) VALUES
-- boys hostel rooms
(1, '101', 2, 5000.00),
(1, '102', 2, 5000.00),
(1, '103', 1, 7000.00),
(1, '201', 3, 4000.00),
-- Girls hostel rooms  
(2, '201', 2, 4500.00),
(2, '202', 2, 4500.00),
(2, '203', 1, 6500.00),
(2, '301', 3, 3800.00);

-- insert Students
INSERT INTO students (name, email, phone, gender) VALUES
('Arjun Sharma', 'arjun@email.com', '9876543001', 'Male'),
('Priya Patel', 'priya@email.com', '9876543002', 'Female'),
('Rohit Kumar', 'rohit@email.com', '9876543003', 'Male'),
('Sneha Singh', 'sneha@email.com', '9876543004', 'Female'),
('Vikram Gupta', 'vikram@email.com', '9876543005', 'Male'),
('Ananya Reddy', 'ananya@email.com', '9876543006', 'Female');


INSERT INTO accommodations (student_id, room_id, check_in_date, status) VALUES
(1, 1, '2024-01-01', 'Active'),  
(3, 1, '2024-01-01', 'Active'),  
(5, 3, '2024-01-01', 'Active'),  
(4, 5, '2024-01-01', 'Active'),  
(6, 7, '2024-01-01', 'Active');  

-- insert Payments
INSERT INTO payments (student_id, amount, payment_date, payment_type, status) VALUES
-- January payments (all   Paid)
(1, 5000.00, '2024-01-01', 'Rent', 'Paid'),
(2, 4500.00, '2024-01-01', 'Rent', 'Paid'),
(3, 5000.00, '2024-01-01', 'Rent', 'Paid'),
(4, 4500.00, '2024-01-01', 'Rent', 'Paid'),
(5, 7000.00, '2024-01-01', 'Rent', 'Paid'),
(6, 6500.00, '2024-01-01', 'Rent', 'Paid'),
-- February payments (some pending)
(1, 5000.00, '2024-02-01', 'Rent', 'Paid'),
(2, 4500.00, '2024-02-01', 'Rent', 'Paid'),
(3, 5000.00, '2024-02-01', 'Rent', 'Pending'),
(4, 4500.00, '2024-02-01', 'Rent', 'Pending'),
(5, 7000.00, '2024-02-01', 'Rent', 'Paid'),
(6, 6500.00, '2024-02-01', 'Rent', 'Paid');


SELECT 
    students.name AS student_name,
    hostels.hostel_name,
    rooms.room_number,
    rooms.monthly_rent,
    students.phone
FROM students
JOIN accommodations ON students.student_id = accommodations.student_id
JOIN rooms ON accommodations.room_id = rooms.room_id
JOIN hostels ON rooms.hostel_id = hostels.hostel_id
WHERE accommodations.status = 'Active'
ORDER BY hostels.hostel_name, rooms.room_number;


SELECT 
    students.name AS student_name,
    students.email,
    payments.amount,
    payments.payment_date,
    payments.payment_type
FROM students
JOIN payments ON students.student_id = payments.student_id
WHERE payments.status = 'Pending'
ORDER BY payments.payment_date;


SELECT 
    hostels.hostel_name,
    hostels.hostel_type,
    COUNT(accommodations.student_id) AS students_count,
    hostels.total_rooms,
    (hostels.total_rooms - COUNT(DISTINCT rooms.room_id)) AS available_rooms
FROM hostels
LEFT JOIN rooms ON hostels.hostel_id = rooms.hostel_id
LEFT JOIN accommodations ON rooms.room_id = accommodations.room_id AND accommodations.status = 'Active'
GROUP BY hostels.hostel_id, hostels.hostel_name, hostels.hostel_type, hostels.total_rooms;


SELECT 
    payments.payment_type,
    payments.status,
    COUNT(*) AS payment_count,
    SUM(payments.amount) AS total_amount
FROM payments
GROUP BY payments.payment_type, payments.status
ORDER BY payments.payment_type, payments.status;


SELECT 
    hostels.hostel_name,
    rooms.room_number,
    rooms.capacity,
    rooms.monthly_rent,
    'Available' AS room_status
FROM rooms
JOIN hostels ON rooms.hostel_id = hostels.hostel_id
LEFT JOIN accommodations ON rooms.room_id = accommodations.room_id AND accommodations.status = 'Active'
WHERE accommodations.room_id IS NULL
ORDER BY hostels.hostel_name, rooms.room_number;


SELECT 
    students.student_id, 
    students.name, 
    students.email, 
    students.phone, 
    students.gender 
FROM students 
WHERE students.email = 'tokom@email.com';


SELECT 
    students.student_id, 
    students.name, 
    students.email, 
    students.phone, 
    students.gender 
FROM students 
WHERE LOWER(students.name) LIKE LOWER('%Pupu%');



-- Success message
SELECT 'Database created successfully!' AS status;

-- Count each table separately  
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_hostels FROM hostels;
SELECT COUNT(*) AS total_rooms FROM rooms;
SELECT COUNT(*) AS total_accommodations FROM accommodations;
SELECT COUNT(*) AS total_payments FROM payments;
