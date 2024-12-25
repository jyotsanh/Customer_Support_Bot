# config
from config.settings import get_llm

# tools
from tools.math_tool import multiply, add, subtract
from tools.hotel_info_tool import get_info_about_hotel_bomo
from tools.book_info_tool import book_hotel, cancel_booking, update_hotel_info

# langchain
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate

#libs
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



part_2_tools = [
        TavilySearchResults(max_results=1),
        # get_info_about_hotel_bomo,
        # book_hotel,
        # cancel_booking,
        # update_hotel_info
    ]

def create_primary_assistant_runnable():
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Chatbot Assistant for Hotel Bomo. Answer any query related to Hotel Bomo using `get_info_about_hotel` tools. "
                " Before booking a room , you need to check the customer if they are register or not via verification code. "
                "Always refer to Hotel Bomo in the first person (e.g., 'we,' 'our') when discussing its offerings, services, and features. "
                "Before booking room make sure to ask the required arguments for booking the room. "
                "For example, say 'We offer a multi-cuisine dining experience' instead of 'They offer a multi-cuisine dining experience.' "
                "Use the provided tools to assist the user's queries. "
                "When searching, be persistent. Expand your query bounds if the first search returns no results. "
                "If a search comes up empty, expand your search before giving up."
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)
    
    test_primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer any query related to Hotel Bomo [`location`,`description`,`rooms`,`dining`,`activities`,`contact_info`] using `get_info_about_hotel` tools."
                "Before running the tools, repeat back the required arguments before invoking the tools. "
                "You are a Customer Support Assistant for Hotel Bomo."
                "Always refer to Hotel Bomo in the first person (e.g., 'we,' 'our') when discussing its offerings, services, and features. "
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)
    
    # llms available: openai, google, groq
    llm = get_llm('google') #-> return llm based on param passed
    # part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)
    part_2_assistant_runnable = test_primary_assistant_prompt | llm.bind_tools(part_2_tools)
    print("Returning the assistant runnable with tools")
    return part_2_assistant_runnable