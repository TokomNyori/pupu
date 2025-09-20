# Add hostels first (Boys and Girls hostels)
INSERT_HOSTELS = """
INSERT IGNORE INTO hostels (hostel_name, hostel_type, total_rooms) VALUES
('Sunrise Boys Hostel', 'Boys', 20),
('Moonlight Girls Hostel', 'Girls', 18)
"""

# Add rooms to hostels
INSERT_ROOMS = """
INSERT IGNORE INTO rooms (hostel_id, room_number, capacity, monthly_rent) VALUES
-- Boys hostel rooms (hostel_id = 1)
(1, '101', 2, 5000.00),
(1, '102', 2, 5000.00),
(1, '103', 1, 7000.00),
(1, '201', 3, 4000.00),
-- Girls hostel rooms (hostel_id = 2)  
(2, '201', 2, 4500.00),
(2, '202', 2, 4500.00),
(2, '203', 1, 6500.00),
(2, '301', 3, 3800.00)
"""

# Add students (email is unique, so use INSERT IGNORE)
INSERT_STUDENTS = """
INSERT IGNORE INTO students (name, email, phone, gender) VALUES
('Arjun Nyori', 'arjun@email.com', '9876543001', 'Male'),
('Priya Tame', 'priya@email.com', '9876543002', 'Female'),
('Rohit Kumar', 'rohit@email.com', '9876543003', 'Male'),
('Takar Singh', 'sneha@email.com', '9876543004', 'Female'),
('Moge Ete', 'vikram@email.com', '9876543005', 'Male'),
('Mari Reddy', 'ananya@email.com', '9876543006', 'Female')
"""

# Assign students to rooms (avoid duplicate room assignments)
INSERT_ACCOMMODATIONS = """
INSERT IGNORE INTO accommodations (student_id, room_id, check_in_date, status) VALUES
(1, 1, '2024-01-01', 'Active'), 
(3, 1, '2024-01-01', 'Active'), 
(5, 3, '2024-01-01', 'Active'),  
(4, 5, '2024-01-01', 'Active'),  
(6, 7, '2024-01-01', 'Active')   
"""

# Add some payments (avoid duplicate payments for same student/date/type)
INSERT_PAYMENTS = """
INSERT INTO payments (student_id, amount, payment_date, payment_type, status) 
SELECT * FROM (
    SELECT 1, 5000.00, '2024-01-01', 'Rent', 'Paid' UNION ALL
    SELECT 3, 5000.00, '2024-01-01', 'Rent', 'Paid' UNION ALL
    SELECT 4, 4500.00, '2024-01-01', 'Rent', 'Paid' UNION ALL
    SELECT 5, 7000.00, '2024-01-01', 'Rent', 'Paid' UNION ALL
    SELECT 6, 6500.00, '2024-01-01', 'Rent', 'Paid' UNION ALL
    SELECT 1, 5000.00, '2024-02-01', 'Rent', 'Paid' UNION ALL
    SELECT 3, 5000.00, '2024-02-01', 'Rent', 'Pending' UNION ALL
    SELECT 4, 4500.00, '2024-02-01', 'Rent', 'Pending' UNION ALL
    SELECT 5, 7000.00, '2024-02-01', 'Rent', 'Paid' UNION ALL
    SELECT 6, 6500.00, '2024-02-01', 'Rent', 'Paid'
) AS temp
WHERE NOT EXISTS (
    SELECT 1 FROM payments p 
    WHERE p.student_id = temp.student_id 
    AND p.payment_date = temp.payment_date 
    AND p.payment_type = temp.payment_type
)
"""

# Show all active students with their room details
SELECT_ACTIVE_STUDENTS = """
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
ORDER BY h.hostel_name, r.room_number
"""

# Show pending payments
SELECT_PENDING_PAYMENTS = """
SELECT 
    s.name AS student_name,
    s.email,
    p.amount,
    p.payment_date,
    p.payment_type
FROM students s
JOIN payments p ON s.student_id = p.student_id
WHERE p.status = 'Pending'
ORDER BY p.payment_date
"""

# Show available rooms
SELECT_AVAILABLE_ROOMS = """
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
ORDER BY h.hostel_name, r.room_number
"""
