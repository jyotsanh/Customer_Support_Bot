from fastapi import APIRouter, Query
from graphs.part_2_graph import get_response
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

# class ChatRequest(BaseModel):
#     query: str
#     sender_id: str = "123abc"

# class ChatResponse(BaseModel):
#     message: str

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
        print("--------Response from Runnable LLM node received-------")
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