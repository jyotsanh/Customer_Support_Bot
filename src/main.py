from fastapi import FastAPI
from api.chat_routes import router as chat_router

app = FastAPI(
    title="Customer Support Chatbot",
    description="AI-powered customer support assistant for flight-related queries"
)

# Include chat routes
app.include_router(chat_router)

# Optional: Add health check endpoint
@app.get("/")
async def health_check():
    response = {
                    "status": "healthy"
                }
    return response