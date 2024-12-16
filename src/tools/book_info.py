from langchain_core.tools import tool

@tool
def fetch_hotel_book_information():
    """
    
    """
    return {"tool_calls": "fetch_hotel_book_information"}