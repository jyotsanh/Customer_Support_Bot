from typing import TypedDict, List, Tuple
from langchain_core.messages import BaseMessage

class State(TypedDict):
    """
    Defines the state structure for the LangGraph conversation.
    
    Attributes:
    - messages: Conversation history
    - user_info: Additional user context
    """
    messages: List[Tuple[str, str]]
    user_info: dict