# Customer Support Chatbot API Documentation

## Overview
The Customer Support Chatbot is an AI-powered assistant designed to handle flight-related queries and hotel information. It utilizes FastAPI for the web framework and LangChain for the AI functionalities.

## Base URL
```
http://127.0.0.1:8000/chat

```

## Endpoints

### Health Check
- **GET** `/`
  
  This endpoint checks the health status of the API.

  **Response:**
  ```json
  {
      "status": "healthy"
  }
  ```

### Chat Endpoint
- **POST** `/chat/`
  
  This endpoint handles chat interactions with the AI assistant.

  **Request Body:**
  ```json
  {
      "query": "Your query here",
      "senderId": "Unique identifier for the conversation thread"
  }
  ```

  **Response:**
  ```json
  {
      "msg": "AI-generated response message"
  }
  ```

  **Error Response:**
  ```json
  {
      "msg": "I'm sorry, there was an error processing your request."
  }
  ```

## Tools and Functionalities
The chatbot integrates various tools to provide responses related to hotel information and customer support. The following tools are available:

- **TavilySearchResults**: For searching hotel-related information.
- **get_info_about_hotel_bomo**: To fetch specific information about Hotel Bomo.
- **Booking Tools**: Includes functionalities to book hotels, register customers, check customer status, cancel bookings, and update hotel information.

## Usage
1. **Start the FastAPI server** to expose the API.
2. **Send a POST request** to the `/chat/` endpoint with the user's query and sender ID.
3. **Receive the AI-generated response** in the JSON format.

## Example
### Request
```bash
curl -X POST "http://127.0.0.1:8000/chat/" -H "Content-Type: application/json" -d '{"query": "What are the amenities at Hotel Bomo?", "senderId": "123abc"}'
```
### Response
```json
{
"msg": "We offer a multi-cuisine dining experience, a swimming pool, and free Wi-Fi."
}
```

## Error Handling
In case of an error during processing, the API will return a generic error message. Ensure to handle exceptions in your application to provide a better user experience.

## Conclusion
This API documentation provides a comprehensive overview of the Customer Support Chatbot's functionalities and how to interact with it. For further assistance, please refer to the codebase or contact the development team.