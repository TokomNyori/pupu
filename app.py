import mysql.connector
from queries import *


def execute_insert_query(cursor, query, description):
    """Helper function to execute INSERT queries"""
    try:
        cursor.execute(query)
        print(f"✅ {description}")
    except mysql.connector.Error as e:
        print(f"❌ eerror in {description}: {e}")


def show_query_results(cursor, query, title):
    """Helper function to run select queries and display results good way"""
    try:
        cursor.execute(query)
        results = cursor.fetchall()

        print(f"\n📊 {title}")
        print("=" * 60)

        if results:
            # Get column names
            column_names = [desc[0] for desc in cursor.description]

            # Print header
            header = " | ".join(column_names)
            print(header)
            print("-" * len(header))

            # Print data rows
            for row in results:
                print(" | ".join(str(item) for item in row))
        else:
            print("No data found.")

    except mysql.connector.Error as e:
        print(f"❌ Error in {title}: {e}")


try:
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tokom@0101",
        # No database parameter, we'll create it later....!!
    )

    if conn.is_connected():
        print("Connected to MySQL server")

        # Create a cursor to execute commands
        cursor = conn.cursor()

        # Step 1: Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_management")
        print("✅ Database 'hostel_management' created!")

        # Step 2: Using database
        cursor.execute("USE hostel_management")
        print("✅ Now using 'hostel_management' database")

        # Step 3: crreate  first table - students
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

        # Step 4: create hostels table (boys/Girl hostels)
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

        # Step 5: create room table (rooms inside hostels
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

        # Step 6: create accommodations table (which student lives in which room)
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

        # step 7: create payments table (rent payments)
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

        # step 8: insert sample data using queries from queries.py
        print("\n🔄 Adding sample data...")
        execute_insert_query(cursor, INSERT_HOSTELS, "Hostels added")
        execute_insert_query(cursor, INSERT_ROOMS, "Rooms added")
        execute_insert_query(cursor, INSERT_STUDENTS, "Students added")
        execute_insert_query(cursor, INSERT_ACCOMMODATIONS, "Room assignments added")
        execute_insert_query(cursor, INSERT_PAYMENTS, "Payment records added")

        # Saviing all changes to database
        conn.commit()
        print("\n💾 All data saved to database!")

        # Step 9: see the data by running select queries
        print("\n" + "=" * 70)
        print("🔍 QUERYING DATA - LET'S SEE WHAT WE HAVE!")
        print("=" * 70)

        show_query_results(cursor, ACTIVE_STUDENTS, "ACTIVE STUDENTS WITH ROOM INFO")
        show_query_results(cursor, PENDING_PAYMENTS, "PENDING RENT PAYMENTS")
        show_query_results(cursor, AVAILABLE_ROOMS, "AVAILABLE ROOMS FOR RENT")
        # END!!!!

    else:
        print("Failed to connect to MySQL server")

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed")
