from fastapi import FastAPI
from src.api.chat_routes import router as chat_router

app = FastAPI(
    title="Nepal Airlines Customer Support Chatbot",
    description="AI-powered customer support assistant for flight-related queries"
)

# Include chat routes
app.include_router(chat_router)

# Optional: Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}