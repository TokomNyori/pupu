from helper_functions import *
from queries import *


def setup_database(cursor):
    # Create the database and use it....!!!!!
    cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_management")
    print("✅ Database 'hostel_management' created!")

    cursor.execute("USE hostel_management")
    print("✅ Now using 'hostel_management' database")


def create_tables(cursor):
    # Create all required tables for the hostel management system.

    # Step 1: create first table - students
    create_students_table = """
    CREATE TABLE IF NOT EXISTS students (
        student_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(15) NOT NULL,
        gender ENUM('Male', 'Female') NOT NULL
    )
    """
    cursor.execute(create_students_table)
    print("✅ 'students' table created!")

    # Step 2: create hostels table (boys/Girl hostels)
    create_hostels_table = """
    CREATE TABLE IF NOT EXISTS hostels (
        hostel_id INT PRIMARY KEY AUTO_INCREMENT,
        hostel_name VARCHAR(100) NOT NULL,
        hostel_type ENUM('Boys', 'Girls') NOT NULL,
        total_rooms INT NOT NULL
    )
    """
    cursor.execute(create_hostels_table)
    print("✅ 'hostels' table created!")

    # Step 3: create room table (rooms inside hostels)
    create_rooms_table = """
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INT PRIMARY KEY AUTO_INCREMENT,
        hostel_id INT NOT NULL,
        room_number VARCHAR(10) NOT NULL,
        capacity INT NOT NULL,
        monthly_rent DECIMAL(8,2) NOT NULL,
        FOREIGN KEY (hostel_id) REFERENCES hostels(hostel_id)
    )
    """
    cursor.execute(create_rooms_table)
    print("✅ 'rooms' table created!")

    # Step 4: create accommodations table (which student lives in which room)
    create_accommodations_table = """
    CREATE TABLE IF NOT EXISTS accommodations (
        accommodation_id INT PRIMARY KEY AUTO_INCREMENT,
        student_id INT NOT NULL,
        room_id INT NOT NULL,
        check_in_date DATE NOT NULL,
        status ENUM('Active', 'Checked Out') DEFAULT 'Active',
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    )
    """
    cursor.execute(create_accommodations_table)
    print("✅ 'accommodations' table created!")

    # Step 5: create payments table (rent payments)
    create_payments_table = """
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INT PRIMARY KEY AUTO_INCREMENT,
        student_id INT NOT NULL,
        amount DECIMAL(8,2) NOT NULL,
        payment_date DATE NOT NULL,
        payment_type ENUM('Rent', 'Deposit') NOT NULL,
        status ENUM('Paid', 'Pending') DEFAULT 'Paid',
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    """
    cursor.execute(create_payments_table)
    print("✅ 'payments' table created!")

    print("\n🎉 ALL TABLES CREATED SUCCESSFULLY!")


def insert_sample_data(cursor):
    # Insert sample data into all tables....!!!!!!!!!
    print("\n🔄 Adding sample data...")
    insert_query(cursor, INSERT_HOSTELS, "Hostels added")
    insert_query(cursor, INSERT_ROOMS, "Rooms added")
    insert_query(cursor, INSERT_STUDENTS, "Students added")
    insert_query(cursor, INSERT_ACCOMMODATIONS, "Room assignments added")
    insert_query(cursor, INSERT_PAYMENTS, "Payment records added")


def display_query_results(cursor):
    # Display results from various queries....!!!!!!!!!
    print("\n" + "=" * 70)
    print("🔍 QUERYING DATA - LET'S SEE WHAT WE HAVE!")
    print("=" * 70)

    select_and_display_query(cursor, SELECT_ACTIVE_STUDENTS, "ACTIVE STUDENTS WITH ROOM INFO")
    select_and_display_query(cursor, SELECT_PENDING_PAYMENTS, "PENDING RENT PAYMENTS")
    select_and_display_query(cursor, SELECT_AVAILABLE_ROOMS, "AVAILABLE ROOMS FOR RENT")
