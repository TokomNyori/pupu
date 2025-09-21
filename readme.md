# hostel management system

hey pupu! here's the simple version... read it slowly and you'll get it

## what this is

this project is a tiny mysql-backed system for managing hostel data (students, hostels, rooms, payments)... you can run it, see how data is created, and try a few search functions  
we kept things simple so you can focus on understanding the flow... not memorizing fancy stuff

## files you'll see

- `app.py`: the main file you run... connects to mysql and calls the other functions
- `queries.py`: sql statements kept as strings... insert/select/etc...
- `helper_functions.py`: small helpers to print results, search students, etc...
- `main_functions.py`: setup database, create tables, insert sample data...
- `hostel_management.sql`: the full sql if you want to see everything in one place

## imports at the top

when you open `app.py`, you'll see these:

```python
import mysql.connector
from queries import *
from helper_functions import *
from main_functions import *
```

`mysql.connector` - lets python talk to mysql... like a translator between our code and the database  
`from queries import *` - brings all the sql strings so we don't write long queries in the main file  
`from helper_functions import *` - helpers we reuse... keeps things clean  
`from main_functions import *` - the setup/insert functions that do the heavy work

## how we connect to mysql

```python
def create_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tokom@0101",
        # no database here... we create/select it later
    )
```

this function opens a connection to mysql... we'll create the `hostel_management` database a bit later in the code  
if your mysql password is different, just change the `password` value above...

## connecting in the main flow

```python
try:
    conn = create_database_connection()

    if conn.is_connected():
        print("Connected to MySQL server")
        # do all the database work here...
    else:
        print("Failed to connect to MySQL server")

except mysql.connector.Error as e:
    print(f"Error: {e}")
```

we try to connect... if it's ok, we go ahead... if not, we tell you  
the try-except is a safety net... if mysql isn't running or the password is wrong, the program won't crash... it will show the error and stop gracefully

## what happens after connection

```python
cursor = conn.cursor()

# setup database and tables
setup_database(cursor)
create_tables(cursor)

# insert sample data
insert_sample_data(cursor)
```

`cursor = conn.cursor()` - think of this like a remote control for the database... we use it to send commands  
then we call these in order:

- **setup_database(cursor)** - creates the `hostel_management` database
- **create_tables(cursor)** - makes the tables (students, hostels, rooms, payments, etc.)
- **insert_sample_data(cursor)** - adds some example rows so you can see real output

## helper functions you can try

```python
display_query_results(cursor)
find_student_by_email(cursor, "sneha@email.com")
find_students_by_name(cursor, "Takar")
```

`display_query_results(cursor)` - shows the main info we inserted... active students, pending payments, available rooms... all printed neatly  
`find_student_by_email(cursor, "sneha@email.com")` - looks up one student by email... prints details if found, else says not found  
`find_students_by_name(cursor, "Takar")` - finds all students whose name contains "Takar"... case doesn't matter

### breaking down the `find_students_by_name` function

```python
def find_students_by_name(cursor, name):
    try:
        query = """
        SELECT student_id, name, email, phone, gender
        FROM students
        WHERE LOWER(name) LIKE LOWER(%s)
        """

        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()

        if results:
            print(f"\n👥 STUDENTS FOUND WITH NAME '{name}':")
            print("=" * 50)
            for student in results:
                student_id, name, email, phone, gender = student
                print(f"ID: {student_id} | Name: {name} | Email: {email} | Phone: {phone} | Gender: {gender}")
        else:
            print(f"No students found with name: {name}")

    except mysql.connector.Error as e:
        print(f"Error searching by name: {e}")
```

`WHERE LOWER(name) LIKE LOWER(%s)` - makes the search case-insensitive... we convert both sides to lowercase before comparing  
`cursor.execute(query, (f"%{name}%",))` - the `%` around the name means "contains"... so "takar" matches "Takar Singh", "Ram Takar", etc  
`%s` - this placeholder keeps the query safe... we pass the actual value separately instead of gluing strings  
`results = cursor.fetchall()` - gets all matching rows  
`for student in results:` - loops through and prints each student nicely  
the try-except catches any database errors so the program doesn't crash...

## quick run tips

- make sure mysql is running on your computer
- update the password in `app.py` if yours is different
- install the connector once:

```bash
pip install mysql-connector-python
```

- then run:

```bash
python app.py
```

- if you see "Connected to MySQL server", you're good... watch the printed output

## common hiccups

- access denied: password wrong... change it in `create_database_connection()`
- module not found: mysql... install the connector with the command above
- can't connect: start the mysql service first

that's it... message me if something looks confusing and we'll fix it together
