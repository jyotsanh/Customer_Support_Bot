from langgraph.graph import StateGraph, START
from langchain_core.runnables import RunnableConfig

from src.core.state import State
from src.core.assistant import Assistant
from src.tools.flight_info import fetch_user_flight_information
from src.prompts.primary_assistant import create_primary_assistant_runnable
from src.tools.utility import create_tool_node_with_fallback

def tools_condition(state: State):
    """
    Determine whether to use tools based on the assistant's response.
    """
    last_message = state["messages"][-1]
    return "tool_calls" in last_message

def build_graph():
    """
    Build the LangGraph for the customer support chatbot.
    """
    builder = StateGraph(State)

    # Define nodes
    def user_info(state: State):
        return {"user_info": fetch_user_flight_information.invoke({})}

    builder.add_node("fetch_user_info", user_info)
    builder.add_edge(START, "fetch_user_info")

    # Create assistant and tools nodes
    assistant_runnable = create_primary_assistant_runnable()
    builder.add_node("assistant", Assistant(assistant_runnable))
    builder.add_node("tools", create_tool_node_with_fallback())

    # Define edges
    builder.add_edge("fetch_user_info", "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")

    # Compile the graph with memory
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    
    return builder.compile(
        checkpointer=memory,
        interrupt_before=["tools"]
    )

# Create the graph
part_2_graph = build_graph()

def get_response(prompt: str, sender_id: str):
    """
    Main function to get response from the chatbot.
    
    :param prompt: User's input message
    :param sender_id: Unique identifier for the conversation thread
    :return: Graph response
    """
    config = {
        "configurable": {
            "passenger_id": "3442 587242",  # Example passenger ID
            "thread_id": sender_id,
        }
    }
    
    return part_2_graph.invoke(
        {"messages": [("user", prompt)]}, 
        config
    )