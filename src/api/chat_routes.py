from fastapi import APIRouter, Query
from src.graphs.part_2_graph import get_response
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    sender_id: str = "123abc"

class ChatResponse(BaseModel):
    message: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat interactions with the AI assistant.
    
    :param request: Chat request containing query and sender ID
    :return: AI-generated response
    """
    try:
        response = get_response(request.query, request.sender_id)
        return ChatResponse(message=response['messages'][-1].content)
    except Exception as e:
        # Log the error (you'd use proper logging in production)
        print(f"Chat error: {e}")
        return ChatResponse(message="I'm sorry, there was an error processing your request.")