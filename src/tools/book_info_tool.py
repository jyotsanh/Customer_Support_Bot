# langchain 
from langchain_core.tools import tool

# libs
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

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
    