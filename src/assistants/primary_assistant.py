# config
from config.settings import get_llm

from langchain_community.tools.tavily_search import TavilySearchResults

# core
from core.state import *

# tools
from tools.tour_booking_info import *
from tools.flight_tools.search_flights import *
from tools.policy import *

# langchain
from langchain_core.prompts import ChatPromptTemplate

#libs
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()



part_2_tools = [
        book_tour,
        cancel_tour_booking,
        reschedule_tour_time,
        
        get_today_date,
        get_available_slots,
        get_current_booking,
        is_date_valid,
        
        get_steps_for_booking_tour,
        get_steps_for_reschedule_tour,
        get_steps_for_cancelling_tour
    
    ]

primary_assistant_tools = [
        TavilySearchResults(max_results=1),
        search_flights,
        lookup_policy,
        ]

def create_primary_assistant_runnable():

    """
    Creates a primary assistant runnable with tools for booking, rescheduling, 
    and canceling tours using LangChain's ChatPromptTemplate and integrated LLMs.
    
    Returns:
        AssistantRunnable: Configured runnable for handling tour management queries.
    """
    test_primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                   """
                   ## CRITICAL GUIDELINES YOU HAVE TO FOLLOW:
                    You are a helpful customer support assistant for booking a tour.
                    `DO NOT MENTION WHAT YOU ARE GOING TO DO, JUST ASK USER`
                    Don't ask Customer information in one go, ask for it step by step.
                    You always have to follow `get_steps` tool which will provide you a proper steps for booking, rescheduling or canceling a tour.
                    Be clear, concise, and use the tools to provide the required information for each step of the process.
                    If additional details are needed or the user has questions, guide them accordingly.
                    When searching, be persistent. Expand your query bounds if the first search returns no results.
                    If a search comes up empty, try a broader search before giving up.
                    \nPresent time: {time}.
                    \nPresent Year: {year}
                    """
                ),
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(
        time=datetime.now,
        year=datetime.now().year
    )
    print(datetime.now().year)
    # llms available: openai, google, groq
    llm = get_llm('openai') #-> return llm based on param passed
    # part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)
    part_2_assistant_runnable = test_primary_assistant_prompt | llm.bind_tools(part_2_tools)
    print("Returning the assistant runnable with tools")
    return part_2_assistant_runnable

def test_primary_assistant_runnable():
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful customer support assistant for Swiss Airlines. "
                "Your primary role is to search for flight information and company policies to answer customer queries. "
                "If a customer requests to update or cancel a flight, book a car rental, book a hotel, or get trip recommendations, "
                "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                " Only the specialized assistants are given permission to do this for the user."
                "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                " If a search comes up empty, expand your search before giving up."
                "\n\nCurrent user flight information:\n<Flights>\n{user_info}\n</Flights>"
                "\nCurrent time: {time}.",
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)
    
    llm = get_llm(model="google")
    
    assistant_runnable = primary_assistant_prompt | llm.bind_tools(
            primary_assistant_tools
            + [
                ToFlightBookingAssistant,
                ToBookCarRental,
                ToHotelBookingAssistant,
                ToBookExcursion,
            ]
        )
    return assistant_runnable