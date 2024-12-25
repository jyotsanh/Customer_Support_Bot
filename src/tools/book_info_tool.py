# langchain 

import datetime
import random
import string
import uuid
from langchain_core.tools import tool
from redis_mem.redis import *
# libs
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

#config
from config.settings import send_verification_email, generate_unique_verification_code, validate_email, validate_phone_number, send_email

def generate_room_number():
    # Generate a random room number
    room_number = ''.join(random.choices(string.digits, k=4))
    return room_number

@tool
def book_hotel(check_in_date: str, check_out_date: str, num_rooms: int, num_guests: int) -> str:
    """
    Book a room in a hotel.

    Args:
        check_in_date (str): The check-in date.
        check_out_date (str): The check-out date.
        num_rooms (int): The number of rooms.
        num_guests (int): The number of guests.
    Returns:
        str: A message indicating the hotel has been booked.
    """
    try:
        # Validate input data
        try:
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
            if check_out <= check_in:
                raise ValueError("Check-out date must be after check-in date")
        except ValueError as e:
            return f"Invalid date format or date logic: {e}"

        if num_rooms <= 0 or num_guests <= 0:
            return "Number of rooms and guests must be positive"

        # Create booking data
        booking_id = str(uuid.uuid4())
        booking_data = {
            "booking_id": booking_id,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "num_rooms": num_rooms,
            "num_guests": num_guests,
            "status": "confirmed",
        }

        # Store booking in Redis
        setData(f"booking:{booking_id}", booking_data)

        return f"""Booking confirmed!"""

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
def cancel_booking(verification_code: str) -> str:
    """
    Using the verification code send via mail,The Cancels the booking of a hotel room.
    
    Args:
        verification_code (int): The verification code sent to the customer.
    
    Returns:
        str: A message indicating the booking cancellation status.
    """
    print("--------Using Cancel_booking tool---------")
    
    try:
        # Use context manager for database connection
        with sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db") as conn:
            cursor = conn.cursor()

            # First, check if the booking exists
            cursor.execute("SELECT * FROM booking_with_keys WHERE verification_code = ?", (verification_code,))
            booking = cursor.fetchone()
            print("--------booking---------")
            if not booking:
                print("Booking not found.")
                return "You have not booked a room in our hotel yet."
            # booking info
            id, hotel_name, check_in_date, check_out_date, num_rooms, num_guests, verification_code = booking
        
            # Delete the booking
            cursor.execute("DELETE FROM booking_with_keys WHERE verification_code = ?", (verification_code,))
            print("--------booking deleted---------")
            # # Optionally, you might want to delete associated customer info or mark as canceled
            # cursor.execute("DELETE FROM customers_with_keys WHERE verification_code = ?", (verification_code,))

            # Commit the changes
            conn.commit()

            return f"Booking successfully canceled."
        
    except Exception as e:
        return f"Error cancelling customer: {e}"
    
    
@tool
def update_hotel_info(
        request_id
        ) -> str:
    """
    Updates the Booking status for a hotel in the database.

    Args:
        check_in_date (str, optional): The new check-in date.
        check_out_date (str, optional): The new check-out date.
        num_rooms (int, optional): The new number of rooms.
        num_guests (int, optional): The new number of guests.
        verification_code (str, optional): The verification code for the booking.

    Returns:
        str: A message indicating the update status.
    """
    try:
        pass
    except Exception as e:
        return f"Error updating hotel info: {e}"
        
    return f"Hotel info updated successfully."