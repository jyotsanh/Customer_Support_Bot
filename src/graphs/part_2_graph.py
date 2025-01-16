# langGraphs imports
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import tools_condition

# redis
from redis_mem.redis import *
# cores
from core.state import *
from core.assistant import Assistant
from config.tool_routes import *

# assistants
from assistants.primary_assistant import *
from assistants.flight_booking_assisstant import *
from assistants.hotel_booking_assisstant import *
from assistants.car_booking_assisstant import *
from assistants.excursion_booking_assisstant import *


# tools
from tools.utility import create_tool_node_with_fallback
from tools.tour_booking_info import get_current_booking
from tools.flight_tools.fetch_user_info import fetch_user_flight_information

# libs
from datetime import datetime

# libs
from tools.utility import *

# def user_info(state: State):
#     return {"user_info": f"{get_current_booking.invoke({})}"}

##################################################################################
def build_graph():
    
    builder = StateGraph(State)


    def user_info(state: State):
        return {"user_info": fetch_user_flight_information.invoke({})}


    builder.add_node("fetch_user_info", user_info)
    builder.add_edge(START, "fetch_user_info")
    
    # Flight booking assistant
    builder.add_node(
        "enter_update_flight",
        create_entry_node("Flight Updates & Booking Assistant", "update_flight"),
    )
    builder.add_node("update_flight", Assistant(update_flight_runnable))
    builder.add_edge("enter_update_flight", "update_flight")
    builder.add_node(
        "update_flight_sensitive_tools",
        create_tool_node_with_fallback(update_flight_sensitive_tools),
    )
    builder.add_node(
        "update_flight_safe_tools",
        create_tool_node_with_fallback(update_flight_safe_tools),
    )


    builder.add_edge("update_flight_sensitive_tools", "update_flight")
    builder.add_edge("update_flight_safe_tools", "update_flight")
    builder.add_conditional_edges(
        "update_flight",
        route_update_flight,
        ["update_flight_sensitive_tools", "update_flight_safe_tools", "leave_skill", END],
    )
    builder.add_node("leave_skill", pop_dialog_state)
    builder.add_edge("leave_skill", "primary_assistant")
    
    # Car rental assistant

    builder.add_node(
        "enter_book_car_rental",
        create_entry_node("Car Rental Assistant", "book_car_rental"),
    )
    builder.add_node("book_car_rental", Assistant(book_car_rental_runnable))
    builder.add_edge("enter_book_car_rental", "book_car_rental")
    builder.add_node(
        "book_car_rental_safe_tools",
        create_tool_node_with_fallback(book_car_rental_safe_tools),
    )
    builder.add_node(
        "book_car_rental_sensitive_tools",
        create_tool_node_with_fallback(book_car_rental_sensitive_tools),
    )

    builder.add_edge("book_car_rental_sensitive_tools", "book_car_rental")
    builder.add_edge("book_car_rental_safe_tools", "book_car_rental")
    builder.add_conditional_edges(
        "book_car_rental",
        route_book_car_rental,
        [
            "book_car_rental_safe_tools",
            "book_car_rental_sensitive_tools",
            "leave_skill",
            END,
        ],
    )
    
    # Hotel booking assistant
    builder.add_node(
        "enter_book_hotel", create_entry_node("Hotel Booking Assistant", "book_hotel")
    )
    builder.add_node("book_hotel", Assistant(book_hotel_runnable))
    builder.add_edge("enter_book_hotel", "book_hotel")
    builder.add_node(
        "book_hotel_safe_tools",
        create_tool_node_with_fallback(book_hotel_safe_tools),
    )
    builder.add_node(
        "book_hotel_sensitive_tools",
        create_tool_node_with_fallback(book_hotel_sensitive_tools),
    )

    builder.add_edge("book_hotel_sensitive_tools", "book_hotel")
    builder.add_edge("book_hotel_safe_tools", "book_hotel")
    builder.add_conditional_edges(
        "book_hotel",
        route_book_hotel,
        ["leave_skill", "book_hotel_safe_tools", "book_hotel_sensitive_tools", END],
    )
    
        
    # Excursion assistant
    builder.add_node(
        "enter_book_excursion",
        create_entry_node("Trip Recommendation Assistant", "book_excursion"),
    )
    builder.add_node("book_excursion", Assistant(book_excursion_runnable))
    builder.add_edge("enter_book_excursion", "book_excursion")
    builder.add_node(
        "book_excursion_safe_tools",
        create_tool_node_with_fallback(book_excursion_safe_tools),
    )
    builder.add_node(
        "book_excursion_sensitive_tools",
        create_tool_node_with_fallback(book_excursion_sensitive_tools),
    )

    builder.add_edge("book_excursion_sensitive_tools", "book_excursion")
    builder.add_edge("book_excursion_safe_tools", "book_excursion")
    builder.add_conditional_edges(
        "book_excursion",
        route_book_excursion,
        ["book_excursion_safe_tools", "book_excursion_sensitive_tools", "leave_skill", END],
    )
    
    # Primary assistant
    assistant_runnable = test_primary_assistant_runnable()
    builder.add_node("primary_assistant", Assistant(assistant_runnable))
    builder.add_node(
        "primary_assistant_tools", create_tool_node_with_fallback(primary_assistant_tools)
    )

    # The assistant can route to one of the delegated assistants,
    # directly use a tool, or directly respond to the user
    builder.add_conditional_edges(
        "primary_assistant",
        route_primary_assistant,
        [
            "enter_update_flight",
            "enter_book_car_rental",
            "enter_book_hotel",
            "enter_book_excursion",
            "primary_assistant_tools",
            END,
        ],
    )
    builder.add_edge("primary_assistant_tools", "primary_assistant")

    builder.add_conditional_edges("fetch_user_info", route_to_workflow)
    # Compile the graph with memory
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    
    part_4_graph = builder.compile(
        checkpointer=memory,
        # Let the user approve or deny the use of sensitive tools
        interrupt_before=[
            "update_flight_sensitive_tools",
            "book_car_rental_sensitive_tools",
            "book_hotel_sensitive_tools",
            "book_excursion_sensitive_tools",
        ],
    )
    
    return part_4_graph

#########################################################################################################
# Create the graph
part_4_graph = build_graph()

def get_response(prompt: str, sender_id: str):
    """
    Main function to get response from the chatbot.
    
    :param prompt: User's input message
    :param sender_id: Unique identifier for the conversation thread
    :return: Graph response
    """
    
    config = {
        "configurable": {
            "passenger_id": "3442 587242",
            "thread_id": sender_id,
        }
    }
    
    return part_4_graph.invoke({"messages": ("user", prompt)}, config)