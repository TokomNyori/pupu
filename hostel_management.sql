DROP DATABASE IF EXISTS hostel_management;
CREATE DATABASE hostel_management;
USE hostel_management;

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
    FOREIGN KEY (student_id) REFERENCES students(student_id),
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
    FOREIGN KEY (student_id) REFERENCES students(student_id)
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
    s.name AS student_name,
    h.hostel_name,
    r.room_number,
    r.monthly_rent,
    s.phone
FROM students s
JOIN accommodations a ON s.student_id = a.student_id
JOIN rooms r ON a.room_id = r.room_id
JOIN hostels h ON r.hostel_id = h.hostel_id
WHERE a.status = 'Active'
ORDER BY h.hostel_name, r.room_number;


SELECT 
    s.name AS student_name,
    s.email,
    p.amount,
    p.payment_date,
    p.payment_type
FROM students s
JOIN payments p ON s.student_id = p.student_id
WHERE p.status = 'Pending'
ORDER BY p.payment_date;


SELECT 
    h.hostel_name,
    h.hostel_type,
    COUNT(a.student_id) AS students_count,
    h.total_rooms,
    (h.total_rooms - COUNT(DISTINCT r.room_id)) AS available_rooms
FROM hostels h
LEFT JOIN rooms r ON h.hostel_id = r.hostel_id
LEFT JOIN accommodations a ON r.room_id = a.room_id AND a.status = 'Active'
GROUP BY h.hostel_id, h.hostel_name, h.hostel_type, h.total_rooms;


SELECT 
    payment_type,
    status,
    COUNT(*) AS payment_count,
    SUM(amount) AS total_amount
FROM payments
GROUP BY payment_type, status
ORDER BY payment_type, status;


SELECT 
    h.hostel_name,
    r.room_number,
    r.capacity,
    r.monthly_rent,
    'Available' AS room_status
FROM rooms r
JOIN hostels h ON r.hostel_id = h.hostel_id
LEFT JOIN accommodations a ON r.room_id = a.room_id AND a.status = 'Active'
WHERE a.room_id IS NULL
ORDER BY h.hostel_name, r.room_number;



SELECT 'Database created successfully!' AS status;

SELECT 'TABLE COUNTS:' AS info;
SELECT 'Students' AS table_name, COUNT(*) AS records FROM students
UNION ALL
SELECT 'Hostels', COUNT(*) FROM hostels
UNION ALL
SELECT 'Rooms', COUNT(*) FROM rooms
UNION ALL
SELECT 'Accommodations', COUNT(*) FROM accommodations
UNION ALL
SELECT 'Payments', COUNT(*) FROM payments;
