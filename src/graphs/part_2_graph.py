# langGraphs imports
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import tools_condition

# cores
from core.state import State
from core.assistant import Assistant

#prompts
from prompts.primary_assistant import create_primary_assistant_runnable, part_2_tools


#tools
from tools.utility import create_tool_node_with_fallback
# from tools.math_tool import add, subtract, multiply


def build_graph():
    """
    Build the LangGraph for the customer support chatbot.
    """
    builder = StateGraph(State)

    # Define nodes
    # def user_info(state: State):
    #     return {"user_info": fetch_user_flight_information.invoke({})}

    # builder.add_node("fetch_user_info", user_info)
    # builder.add_edge(START, "fetch_user_info")

    # Create assistant and tools nodes
    assistant_runnable = create_primary_assistant_runnable()
    builder.add_node("assistant", Assistant(assistant_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(part_2_tools))

    # Define edges
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant") # ReAct agent
    builder.add_edge("assistant", END)

    # Compile the graph with memory
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    
    return builder.compile(
        checkpointer=memory
        # interrupt_before=["tools"]
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
    
    return part_2_graph.invoke({"messages": ("user", prompt)}, config)