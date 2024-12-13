from fastapi import FastAPI

app = FastAPI(
    title="Nepal Airlines Customer Support Chatbot",
    description="AI-powered customer support assistant for flight-related queries"
)


# Optional: Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}