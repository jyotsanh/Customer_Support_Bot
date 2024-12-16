# langchain 

from langchain_core.tools import tool

# libs
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

#config
from config.settings import send_verification_email, generate_unique_verification_code, validate_email, validate_phone_number



@tool
def book_hotel(name: str, check_in_date: str, check_out_date: str, num_rooms: int, num_guests: int) -> str:
    """
    Book a hotel.

    Args:
        name (str): The name of the hotel.
        check_in_date (str): The check-in date.
        check_out_date (str): The check-out date.
        num_rooms (int): The number of rooms.
        num_guests (int): The number of guests.

    Returns:
        str: A message indicating the hotel has been booked.
    """
    try:
        print("--------Using Booking tool---------")
        conn = sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db")
        c = conn.cursor()

        # Create test_booking table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS test_booking (
                id INTEGER PRIMARY KEY,
                hotel_name TEXT,
                check_in_date TEXT,
                check_out_date TEXT,
                num_rooms INTEGER,
                num_guests INTEGER
            )
        """)

        # Insert booking data into the test_booking table
        c.execute("""
            INSERT INTO test_booking (hotel_name, check_in_date, check_out_date, num_rooms, num_guests)
            VALUES (?, ?, ?, ?, ?)
        """, (name, check_in_date, check_out_date, num_rooms, num_guests))

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()
        return f"Hotel {name} has been booked from {check_in_date} to {check_out_date} for {num_rooms} rooms and {num_guests} guests."
    except Exception as e:
        return f"Error booking hotel: {e}"

 
@tool
def register_customer(name: str, email: str, phone: str,address: str) -> str:
    """
    Register a customer.

    Args:
        name (str): The name of the customer.
        email (str): The email address of the customer.
        phone (str): The phone number of the customer.
        address (str): The address of the customer.

    Returns:
        str: A message indicating the customer has been added.
    """
    try:
        # Validate phone number
        if not validate_phone_number(phone):
            return "Error: Phone number must be 10 digits long."

        # Validate email
        if not validate_email(email):
            return "Error: Invalid email format."
        
        print("--------Adding a Customer tool---------")
        conn = sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db")
        c = conn.cursor()
        
        print(f"Name: {name}, Email: {email}, Phone: {phone}, Address: {address}")
        
        # Generate a unique verification code
        verification_code = generate_unique_verification_code(conn)
        print("--------verifi---------")
        # Insert customer data into the customers table
        c.execute("""
            INSERT INTO customers_with_keys (name, email, phone, address, verification_code)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, address, verification_code))
        
        print("---executed---")
        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()
        
        # Send verification code to email (you would implement the email sending logic here)
        send_verification_email(email, verification_code)
        print("----sending the mail----")
        return f"Your account with email {email} has been added. A 6-digit verification code has been sent to your email."
    except Exception as e:
        return f"Error adding customer: {e}"
    
@tool
def check_customer_status(email: str) -> str:
    """
    Check the status of a customer.

    Args:
        email (str): The email address of the customer.

    Returns:
        str: A message indicating the customer's status.
    """
    pass