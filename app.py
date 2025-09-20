import mysql.connector
from queries import *
from helper_functions import *
from main_functions import *


def create_database_connection():
    # create and return a MySQL database connection.
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tokom@0101",
        # No database parameter, we'll create it later....!!!!!!!!!
    )


def main():
    """Main function to run the hostel management system setup."""
    conn = None
    cursor = None

    try:
        # Connect to MySQL server
        conn = create_database_connection()

        if conn.is_connected():
            print("Connected to MySQL server")
            cursor = conn.cursor()

            # Setup database and tables
            setup_database(cursor)
            create_tables(cursor)

            # Insert sample data
            insert_sample_data(cursor)

            # Save all changes to database
            conn.commit()
            print("\n💾 All data saved to database!")

            # Display query results
            display_query_results(cursor)
            # find_student_by_email(cursor, "sneha@email.com")
            # find_students_by_name(cursor, "Takar")

        else:
            print("Failed to connect to MySQL server")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    main()
