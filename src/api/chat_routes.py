from fastapi import APIRouter, Query
from graphs.part_2_graph import get_response
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

# class ChatRequest(BaseModel):
#     query: str
#     sender_id: str = "123abc"

# class ChatResponse(BaseModel):
#     message: str

# libs
from datetime import datetime

# logging
import logging

# Configure logging
logging.basicConfig(
    filename='chatbot.log',
    level=logging.INFO,
    format='%(message)s'  # Simple format to match your desired output
)
@router.post("/")
def chat_endpoint(query: str, senderId: str):
    """
    Handle chat interactions with the AI assistant.
    
    :param request: Chat request containing query and sender ID
    :return: AI-generated response
    """
    try:
        print("--------Getting response from Runnable LLM node-------")
        response = get_response(query,senderId)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time}\nUser: {query}\n"
        logging.info(log_message)
        log_message = f"{current_time}\nResponse: {response['messages'][-1].content}\n"
        print()
        print("--------Response from Runnable LLM node received-------")
        print()
        print("-----------------API Booking Response-----------------")
        print("Response: \n",response['messages'][-1].content)
        print("-----------------API Booking Response------------------")
        print()
        # return ChatResponse(message=response['messages'][-1].content)
        respond = {"msg":response['messages'][-1].content}
        
        return respond
    except Exception as e:
        # Log the error (you'd use proper logging in production)
        print(f"Chat error: {e}")
        respond = {
            "msg": "I'm sorry, there was an error processing your request."
        }
        return respond