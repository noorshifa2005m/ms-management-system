import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Function to connect to MySQL and insert data
def insert_medicalshop_data(conn, cursor):
    try:
        # Get input from user
        name = input("Enter your name: ")
        productname = input("Enter product name: ")
        productprice = float(input("Enter product price: "))  # Convert input to float for decimals
        purchasing_date = input("Enter purchasing date (YYYY-MM-DD): ")

        # Validate and parse the date
        try:
            purchasing_date = datetime.strptime(purchasing_date, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")
            return

        # Check if the person already exists in the database
        query = "SELECT total FROM medicalshop WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        if result:
            current_total = result[0]
            new_total = current_total + productprice

            # Update the existing record with the new total
            update_query = """
            UPDATE medicalshop
            SET productname = %s, productprice = %s, total = %s, purchasing_date = %s
            WHERE name = %s
            """
            data = (productname, productprice, new_total, purchasing_date, name)
            cursor.execute(update_query, data)
            print('Data updated successfully')

        else:
            # Insert a new record if the person does not exist
            insert_query = """
            INSERT INTO medicalshop (name, productname, productprice, total, purchasing_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (name, productname, productprice, productprice, purchasing_date)
            cursor.execute(insert_query, data)
            print('Data inserted successfully')

        # Commit changes to database
        conn.commit()

    except Error as error:
        print(f'Error: {error}')

# Function to display total amount for a particular person
def display_total_amount(conn, cursor):
    try:
        name = input("Enter name to display total amount: ")

        # Prepare SQL query to fetch total amount for the given name
        query = """
        SELECT SUM(total) AS total_amount
        FROM medicalshop
        WHERE name = %s
        """
        # Execute the query
        cursor.execute(query, (name,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            total_amount = result[0]
            print(f'Total amount for {name}: {total_amount}')
        else:
            print(f'No records found for {name}')

    except Error as error:
        print(f'Error: {error}')

# Main function to manage menu options
def main():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            database='medicaldb',
            user='NoorShifa',
            password='shifa2005'  # Use the actual password
        )

        if conn.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object
            cursor = conn.cursor()

            while True:
                print("\nMenu:")
                print("1. Add items")
                print("2. Display total amount for a particular person")
                print("3. Exit")
                choice = input("Enter your choice (1/2/3): ")

                if choice == '1':
                    insert_medicalshop_data(conn, cursor)
                elif choice == '2':
                    display_total_amount(conn, cursor)
                elif choice == '3':
                    print("Exiting program...")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

    except Error as error:
        print(f'Error: {error}')

    finally:
        # Close cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('MySQL connection closed')

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
