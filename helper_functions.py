import mysql.connector


# Insert query....!!!!!!!!!!!!!!!!!!!
def insert_query(cursor, query, description):
    try:
        cursor.execute(query)
        print(f"✅ {description}")
    except mysql.connector.Error as e:
        print(f"❌ eerror in {description}: {e}")


# Select and display query....!!!!!!!!!!!!!!!!!!!
def select_and_display_query(cursor, query, title):
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


# Find a single student by email address....!!!!!!!!!!!!!!!!!!!
def find_student_by_email(cursor, email):
    try:
        query = """
        SELECT student_id, name, email, phone, gender 
        FROM students 
        WHERE email = %s
        """

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            student_id, name, email, phone, gender = result
            print(f"\n👤 STUDENT FOUND:")
            print(
                f"ID: {student_id} | Name: {name} | Email: {email} | Phone: {phone} | Gender: {gender}"
            )
        else:
            print(f"\n❌ No student found with email: {email}")

    except mysql.connector.Error as e:
        print(f"❌ Error searching by email: {e}")



# Find all students with the same name....!!!!!!!!!
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
                print(
                    f"ID: {student_id} | Name: {name} | Email: {email} | Phone: {phone} | Gender: {gender}"
                )
        else:
            print(f"\n❌ No students found with name: {name}")

    except mysql.connector.Error as e:
        print(f"❌ Error searching by name: {e}")



# Delete a student by email address....!!!!!!!!!
def delete_student_by_email(cursor, email):
    try:
        # First check if student exists
        check_query = "SELECT student_id, name FROM students WHERE email = %s"
        cursor.execute(check_query, (email,))
        result = cursor.fetchone()

        if result:
            student_id, name = result

            # Delete the student
            delete_query = "DELETE FROM students WHERE email = %s"
            cursor.execute(delete_query, (email,))

            print(f"\n✅ STUDENT DELETED:")
            print(f"ID: {student_id} | Name: {name} | Email: {email}")
        else:
            print(f"\n❌ No student found with email: {email}")

    except mysql.connector.Error as e:
        print(f"❌ Error deleting student: {e}")

