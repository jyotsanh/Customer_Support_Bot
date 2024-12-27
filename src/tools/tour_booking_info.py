# langchain 
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
# libs
from datetime import datetime, date
import random
import string
import uuid
import os

# redis_mem
from redis_mem.redis import *


from dotenv import load_dotenv
load_dotenv()

BOOKING_KEY = "abc"

@tool
def get_available_slots(startDate, endDate, startTime,config: RunnableConfig) -> str:
    """
    This tool is used to validate if a given time is within business hours (9 AM–6 PM) on a specified date

    Args:
        startDate (str): The check-in date in YYYY-MM-DD format.
        endDate (str): The check-out date in YYYY-MM-DD format.
        startTime (str): The time of the tour in HH:MM AM/PM format.

        
    Returns:
        str: A message indicating availability.
    """
    from datetime import datetime

    print("--------Using get_available_slots tool---------")
    try:
        # Define slot boundaries
        available_start = datetime.strptime("9:00 AM", "%I:%M %p")
        available_end = datetime.strptime("6:00 PM", "%I:%M %p")

        # Convert the given startTime to a datetime object
        user_time = datetime.strptime(startTime, "%I:%M %p")

        # Check if the given time is within the range
        if available_start <= user_time <= available_end:
            return "yes it's available"
        else:
            return "not available try tomorrow"
    except Exception as e:
        return f"Error checking available slots: {e}"



@tool
def book_tour(startDate: str, endDate: str, startTime) -> str:
    """
    Book a room in a hotel.

    Args:
        startDate (str): The check-in date .
        endDate (str): The check-out date in t.
        startTime (str): The time of the tour.
    Returns:
        str: A message indicating that the tour has been booked.
    """
    print("--------Using book_tour tool---------")
    try:
        print(f"Booking tour from {startDate} to {endDate}...")
        # Generate a unique booking ID
        # Create booking data
        if startDate == endDate:
            return "endDate is same , ask the user 'for how many days would you like to go for tour ?'"
        booking_data = {
            "startDate": startDate,
            "endDate": endDate,
            "startTime": startTime,
            "status": "confirmed"
        }
        
        # Store in Redis using fixed key
        setData(BOOKING_KEY, booking_data)
        
        return f"Tour Booking confirmed! Your tour is scheduled from {startDate} to {endDate} at {startTime}"

    except Exception as e:
        return f"Error booking hotel: {e}"
@tool
def is_date_valid(date_str: str) -> str:
    """
    Check if the given date is in the past or future compared to the current date.

    Args:
        date_str (str): The date to check in YYYY-MM-DD format.

    Returns:
        str: A message indicating whether the date is in the past or future.
    """
    try:
        
        print("--------Using is_date_valid tool---------")
        # Parse the input date
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        # Get today's date
        today = datetime.today().date()
        # Compare the input date with today's date
        
        if today == input_date:
            return f"Sorry, same-day bookings are not available. Please select a future date."
        if input_date < today:
            print(f"The date {date_str} is in the past.")
            return f"The date {date_str} is in the past."
        elif input_date > today:
            print(f"The date {date_str} is valid and in the future.")
            return f"The date {date_str} is valid and in the future."
        else:
            print(f"The date {date_str} is today.")
            return f"The date {date_str} is today."
    except Exception as e:
        return f"Error checking the date: {e}"

@tool
def get_today_date() -> str:
    """
    Get today's date in YYYY-MM-DD format.

    Returns:
        str: Today's date in YYYY-MM-DD format.
    """
    print("--------Using get_today_date tool---------")
    today = date.today().strftime("%Y-%m-%d")
    print(f"Todat Date is {today}")
    return str(today)

# @tool
# def get_days_from_today(days: int) -> str:
#     """
#     Get the date that is `days` days from today.

#     Args:
#         days (int): The number of days from today.

#     Returns:
#         str: The date that is `days` days from today in YYYY-MM-DD format.
#     """
#     print("--------Using get_days_from_today tool---------")
#     return str(datetime.date.today() + datetime.timedelta(days=days))    

@tool
def cancel_tour_booking() -> str:
    """
    Using this tool to cancel the booking of a tour.

    Returns:
        str: A message indicating the Tour has been cancel.
    """
    print("--------Using Cancel_booking tool---------")
    
    try:
        # Get current booking data from Redis
        booking_data = getData(BOOKING_KEY)
        
        if booking_data is None:
            return "No active booking found to cancel."
            
        # Update booking status
        booking_data["status"] = "cancelled"
        setData(BOOKING_KEY, booking_data)
        
        return "Your tour booking has been successfully canceled."
        
    except Exception as e:
        return f"Error cancelling your tour: {e}"

    
@tool
def reschedule_tour_time(
        newStartDate: str,
        newEndDate: str,
        newStartTime: str
        ) -> str:
    """
    Reschedule the Tour Booking.

    Args:
        newStartDate (str): The new check-in date in YYYY-MM-DD format.
        newEndDate (str): The new check-out date in YYYY-MM-DD format.

    Returns:
        str: A message indicating the update status.
    """
    print("--------Using reschedule_tour tool---------")
    
    try:
        # Get existing booking
        booking_data = getData(BOOKING_KEY)
        
        if booking_data is None:
            return "No active booking found to reschedule."
            
        if booking_data["status"] == "cancelled":
            return "Cannot reschedule a cancelled booking. Please make a new booking."
        
        # Update booking data
        booking_data.update({
            "startDate": newStartDate,
            "endDate": newEndDate,
            "startTime": newStartTime,
            "status": "rescheduled"
        })
        
        # Save updated booking
        setData(BOOKING_KEY, booking_data)
        
        return f"Your tour has been rescheduled successfully. New dates: {newStartDate} to {newEndDate} at {newStartTime}"
    except Exception as e:
        return f"Error updating hotel info: {e}"


@tool
def get_current_booking() -> str:
    """
    Get details of the current tour booking.

    Returns:
        str: A message containing the current booking details.
    """
    try:
        print("--------Using get_current_booking tool---------")
        booking_data = getData(BOOKING_KEY)
        
        if booking_data is None:
            print("no booking found")
            return "No active booking found.It's a NEW USER use 'get_steps_for_booking_tour' tool "
        print("-----------------------  Booking Data -----------------------")
        print(booking_data)
        print("-----------------------  Booking Data -----------------------")
        
        
        return f"""Current Booking Details:
                    Start Date: {booking_data['startDate']}
                    End Date: {booking_data['endDate']}
                    Start Time: {booking_data['startTime']}
                    Status: {booking_data['status']}"""
    
    except Exception as e:
        return f"Error retrieving booking details: {e}"
    
## STEPS TOOL FOR BOOKING A TOUR
    
@tool
def get_steps_for_booking_tour() -> str:
    """
    Get the precise and proper steps for booking a tour.

    Returns:
        str: A message containing the steps for booking a tour.
    """
    print("--------Using get_steps_for_booking_tour tool---------")
    print()
    steps = """
                "SUNDAY and SATURDAY is not allowed for Booking."
                "check for past date through `is_date_valid` tool."
                If the user's input specifies only a month and day (e.g., "Jan 5"), and the date falls in the past relative to ${today_date}, assume the next occurrence of that date in the future.
                "Booking for today is not allwoed"
                ## Steps for Booking a Tour:
                0. Convert the user's input into the required format YYYY-MM-DD.
                1. Verify if the user has provided a start date, end date, and start time.
                2. Use the `get_today_date` tool to retrieve the current date.
                3. Ensure that the provided dates are not in the past.
                4. Confirm the provided dates do not fall on restricted days (e.g., Saturday and Sunday).
                5. Use the `get_available_slots` tool to check availability for the provided date and time.
                6. If the date or time is unavailable:
                   - Suggest alternative slots.
                   - Request the user to choose one of the available options.
                7. Handle the result of the booking process:
                   - Success: Notify the user that the booking is confirmed and send confirmation details.
                   - Failure: Inform the user that the booking couldn't be completed and suggest retrying later.
                8. End the interaction by asking if there's anything else the user needs assistance with.
            """
    steps2 = """ 
                1. convert the user's input into the required format YYYY-MM-DD.
                2. call the `is_date_valid` tool to check if the date is in the past.
                3. "SUNDAY and SATURDAY is not allowed for Booking."
                4. if needed, use the `get_today_date` tool to retrieve the current date.
                5. Use the `get_available_slots` tool to check availability for the provided date and time.
                6. If the date or time is unavailable:
                   - Suggest alternative slots.
                7. Handle the result of the booking process:
                   - Success: Notify the user that the booking is confirmed and send confirmation details.
                   - Failure: Inform the user that the booking couldn't be completed and suggest retrying later.
            """
    print(steps2)
    print()
    return steps2

@tool
def get_steps_for_reschedule_tour() -> str:
    """
    Get the precise and proper steps for rescheduling a tour.

    Returns:
        str: A message containing the steps for rescheduling a tour.
    """
    print("--------Using get_steps_for_reschedule_tour tool---------")
    print()
    steps = """
                "SUNDAY and SATURDAY is not allowed for Booking."
                "PAST DATE is not allowed for Booking."
                ## Steps for Rescheduling a Tour:
                1. Verify if the user already has a tour booked through `get_current_booking`:
                2. Confirm the new date and time from the user.
                3. Use the `get_today_date` tool to ensure the new date is in the future.
                4. Validate the provided date:
                   - Ensure it does not fall on restricted days (e.g., Saturday and Sunday).
                   - Check the availability of the new date and time using the `getAvailableSlots` tool.
                5. Handle availability results:
                   - If unavailable:
                     - Suggest alternative slots and ask the user to select one.
                   - If available:
                     - Confirm the reschedule by triggering the `get_available_slots` function with the selected date and time.
                6. Handle the result of the rescheduling process:
                   - Success: Notify the user that the booking has been rescheduled successfully and send a confirmation message.
                   - Failure: Inform the user that the rescheduling couldn't be completed and suggest trying again later.
                7. End the interaction by asking if there’s anything else the user needs assistance with.
            """
    steps2 = """
               1. Verify if the user already has a tour booked through `get_current_booking`
               2. Convert the user's input into the required format YYYY-MM-DD.
               3. Confirm the new date and time from the user
               4. Call the `is_date_valid` tool to check if the date is in the past.
               5. "SUNDAY and SATURDAY is not allowed for Booking."
               6. If needed, use the `get_today_date` tool to retrieve the current date.
               7. Use the `get_available_slots` tool to check availability for the provided date and time.
               8. If the date or time is unavailable:
                   - Suggest alternative slots.
               9. Handle the result of the booking process:
                   - Success: Notify the user that the booking is confirmed and send confirmation details.
                   - Failure: Inform the user that the booking couldn't be completed and suggest retrying later.
            """
    print(steps2)
    print() 
    print("--------Using get_steps_for_reschedule_tour tool---------")
    return steps2

@tool
def get_steps_for_cancelling_tour() -> str:
    """
    Get the precise and proper steps for canceling a tour.

    Returns:
        str: A message containing the steps for canceling a tour.
    """
    print("--------Using get_steps_for_cancelling_tour tool START ---------")
    print()
    steps = """
                ## Steps for Cancelling a Tour:
                1. Verify if the user has an active booking using the `get_current_booking` tool:
                2. Confirm with the user that they wish to cancel the tour.
                   - Ask: "Would you prefer to reschedule the tour instead?"
                3. If the user confirms cancellation:
                   - Trigger the `cancel_tour_booking` tool to process the cancellation.
                4. Handle the result of the cancellation:
                   - **Success:**
                     - Notify the user: "Your booking has been canceled successfully."
                   - **Failure:**
                     - Inform the user: "Unfortunately, the cancellation couldn't be processed. Please try again later."
                5. End the interaction:
                   - Ask: "Is there anything else I can assist you with today?"
                   - If no further queries, thank the user and close the conversation.
            """
    print(steps)
    print()
    print("--------Using get_steps_for_cancelling_tour tool END ---------")
    return steps



# TESTING FUNCTION FOR BOOKING A TOUR
def test_book_tour(startDate: str, endDate: str) -> str:
    """
    Book a room in a hotel.

    Args:
        startDate (str): The check-in date in YYYY-MM-DD format.
        endDate (str): The check-out date in YYYY-MM-DD format.
    Returns:
        str: A message indicating that the tour has been booked.
    """
    print("--------Using book_tour tool---------")
    try:
        print(f"Booking tour from {startDate} to {endDate}...")
        
        return f"""Tour Booking confirmed!"""

    except Exception as e:
        return f"Error booking hotel: {e}"


def test_cancel_tour_booking() -> str:
    """
    Using this tool to cancel the booking of a tour.

    Returns:
        str: A message indicating the Tour has been cancel.
    """
    print("--------Using Cancel_booking tool---------")
    
    try:
        print(f"Cancelling tour booking...")

        return f"Booking successfully canceled."
        
    except Exception as e:
        return f"Error cancelling your tour: {e}"


def test_reschedule_tour_time(
        newStartDate: str,
        newEndDate: str,
        ) -> str:
    """
    Reschedule the Tour Booking.

    Args:
        newStartDate (str): The new check-in date in YYYY-MM-DD format.
        newEndDate (str): The new check-out date in YYYY-MM-DD format.

    Returns:
        str: A message indicating the update status.
    """
    print("--------Using reschedule_tour tool---------")
    
    try:
        print(f"Rescheduling tour from {newStartDate} to {newEndDate}...")
        return f"Your tour has been rescheduled from {newStartDate} to {newEndDate} successfully."
    except Exception as e:
        return f"Error updating hotel info: {e}"
        
    return f"Hotel info updated successfully."
