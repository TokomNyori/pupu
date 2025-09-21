## understanding the SELECT_ACTIVE_STUDENTS query

```python
SELECT_ACTIVE_STUDENTS = """
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
ORDER BY hostels.hostel_name, rooms.room_number
"""
```

### what this is doing in simple words

- we start from the `students` table... but room number, hostel name, rent are not there... so we join other tables to show full info about the student

- `JOIN accommodations ON students.student_id = accommodations.student_id`  
  this connects `students` with `accommodations` using a unique id that exists in both... that id is `student_id`... if arjun nyori has `student_id = 1` in `students table`, it will also be `1` in `accommodations table` because when we inserted accommodation data we stored arjun’s id there with his room info

- `JOIN rooms ON accommodations.room_id = rooms.room_id`  
  connects the accommodation to the exact room

- `JOIN hostels ON rooms.hostel_id = hostels.hostel_id`  
  connects the room to its hostel

### what we select from those tables and why

- `students.name` — the student’s name  
- `hostels.hostel_name` — which hostel the room belongs to  
- `rooms.room_number` — which room the student is in  
- `rooms.monthly_rent` — how much the room costs per month  
- `students.phone` — contact number

### why `hostels.hostel_name` and `students.name`?

- because we joined multiple tables, some column names can be similar... so we must say exactly which table a column comes from  
- in `hostels.hostel_name`, `hostels` is the table, `hostel_name` is the column we need

### filter and sort

- `WHERE accommodations.status = 'Active'` — only show students who are currently staying  
- `ORDER BY hostels.hostel_name, rooms.room_number` — sort by hostel, then room... looks clean and easy to read