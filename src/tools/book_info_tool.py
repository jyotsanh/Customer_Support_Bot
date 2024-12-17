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
def book_hotel(check_in_date: str, check_out_date: str, num_rooms: int, num_guests: int, verification_code: int) -> str:
    """
    Book a room in a hotel.

    Args:
        check_in_date (str): The check-in date.
        check_out_date (str): The check-out date.
        num_rooms (int): The number of rooms.
        num_guests (int): The number of guests.
        verification_code (int): The verification code which was sent to the customer while registering.

    Returns:
        str: A message indicating the hotel has been booked.
    """
    try:
        name="Hotel Bomo"
        print("--------Using Booking tool---------")
        conn = sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db")
        c = conn.cursor()

        # check if the provided verification code is valid
        c.execute("SELECT COUNT(*) FROM customers_with_keys WHERE verification_code = ?", (verification_code,))
        customer_info = c.fetchone()
        print(customer_info)
        if customer_info[0] == 0:
            return "pls double check the verification code and try again."

        # Insert booking data into the test_booking table
        c.execute("""
                INSERT INTO booking_with_keys (hotel_name, check_in_date, check_out_date, num_rooms, num_guests, verification_code)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, check_in_date, check_out_date, num_rooms, num_guests, verification_code))

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
def check_customer_status(verification_code: str) -> str:
    """
    retrieve the customer status from the verification code.

    Args:
        verification_code (str): code sent to the customer

    Returns:
        str: A message returning the status of the customer booking the hotel check_in_date, check_out_date
    """
    print("--------Using check_customer_status tool---------")
    
    
        
    try: 
        conn = sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db")
        c = conn.cursor()
        
        c.execute("SELECT * FROM customers_with_keys WHERE verification_code = ?", (verification_code,))
        # Fetch the result
        customer_info = c.fetchone()
        print(customer_info)
        # fetch booking info
        c.execute("SELECT * FROM booking_with_keys WHERE verification_code = ?", (verification_code,))
        booking_info = c.fetchone()
        print(booking_info)
        # customer info
        customer_id, name, email, phone, address, verification_code = customer_info
        
        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()
        
        if booking_info and customer_info:
            # booking info
            id, hotel_name, check_in_date, check_out_date, num_rooms, num_guests, verification_code = booking_info
            print("-----------------chat-bot has user & booking info-----------------")
            print()
            return (
                 f"Welcome back {name}\n You have successfully registered for the following booking:\n"
                    f"Check-in: {check_in_date}\n"
                    f"Check-out: {check_out_date}\n"
                    f"Rooms: {num_rooms}\n"
                    f"Guests: {num_guests}"
            )
        elif customer_info:
            print("-----------------chat-bot has user info-----------------")
            print(customer_info)
            
            print(customer_id, name, email, phone, address)
            return (
                f"Customer Verified:\n"
                f"ID: {customer_id}\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Address: {address}\n"
                "You can proceed with booking a room."
                )
        else:
            return f"Okay, so {name}.It seems you have not Booked a room yet. Please Book a room "
    except Exception as e:
        return f"Pls register again"
    

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
        check_in_date: str=None, 
        check_out_date: str=None, 
        num_rooms: int=None, 
        num_guests: int=None,
        verification_code:str=None
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
    if not verification_code:
        return "Verification code is required to update booking."
    print("--------Using update_hotel_info tool---------")
    try:
        # Use context manager for database connection
        with sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db") as conn:
            conn = sqlite3.connect(f"{os.getenv('DATABASE_PATH')}.db")
            c = conn.cursor()

            # Check if the verification code exists
            c.execute("SELECT check_in_date, check_out_date, num_rooms, num_guests FROM booking_with_keys WHERE verification_code = ?", (verification_code,))
            booking_info = c.fetchone()
            if not booking_info:
                print("Booking not found.")
                return "You have not booked a room in our hotel yet."   
            
            print(f"Old Booking info: {booking_info}")

            # Use existing values if the new ones are empty
            updated_check_in_date = check_in_date if check_in_date else booking_info[0]
            updated_check_out_date = check_out_date if check_out_date else booking_info[1]
            updated_num_rooms = num_rooms if num_rooms else booking_info[2]
            updated_num_guests = num_guests if num_guests else booking_info[3]
            
            # Update the booking info
            c.execute("UPDATE booking_with_keys SET check_in_date = ?, check_out_date = ?, num_rooms = ?, num_guests = ? WHERE verification_code = ?",
                      (updated_check_in_date, updated_check_out_date, updated_num_rooms, updated_num_guests, verification_code))
            
                     
            conn.commit()
            conn.close()
    except Exception as e:
        return f"Error updating hotel info: {e}"
        
    return f"Hotel info updated successfully."