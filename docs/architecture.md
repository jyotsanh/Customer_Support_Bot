# Customer Support Chatbot Architecture

## Overview
The Customer Support Chatbot is an AI-powered assistant designed to handle flight-related queries and hotel information. It utilizes FastAPI for the web framework and LangChain for AI functionalities.

## Architecture Diagram
+---------------------+
| FastAPI Server |
| |
| +---------------+ |
| | Health Check | |
| +---------------+ |
| |
| +---------------+ |
| | Chat Endpoint | |
| +---------------+ |
| |
+---------+-----------+
|
|
v
+---------------------+
| Chat Routes |
| (src/api/chat_routes.py) |
| |
| +---------------+ |
| | Chat Request | |
| +---------------+ |
| |
| +---------------+ |
| | Chat Response | |
| +---------------+ |
+---------+-----------+
|
|
v
+---------------------+
| Graph Structure |
| (src/graphs/part_2_graph.py) |
| |
| +---------------+ |
| | State Graph | |
| +---------------+ |
| |
| +---------------+ |
| | Assistant Node | |
| +---------------+ |
| |
| +---------------+ |
| | Tools Node | |
| +---------------+ |
+---------+-----------+
|
|
v
+---------------------+
| Primary Assistant |
| (src/prompts/primary_assistant.py) |
| |
| +---------------+ |
| | LLM | |
| +---------------+ |
| |
| +---------------+ |
| | Tools | |
| +---------------+ |
+---------+-----------+
|
|
v
+---------------------+
| State Management |
| (src/core/state.py) |
| |
| +---------------+ |
| | State | |
| +---------------+ |
+---------------------+


## Components

### 1. FastAPI Server
- **Health Check Endpoint**: Checks the health status of the API.
- **Chat Endpoint**: Handles chat interactions with the AI assistant.

### 2. Chat Routes
- **ChatRequest**: Defines the structure of the incoming chat request.
- **ChatResponse**: Defines the structure of the outgoing chat response.

### 3. Graph Structure
- **StateGraph**: Manages the flow of the conversation and interactions.
- **Assistant Node**: Represents the primary assistant that processes user queries.
- **Tools Node**: Contains various tools for handling specific tasks (e.g., hotel information, booking).

### 4. Primary Assistant
- **LLM (Language Model)**: Utilizes a language model to generate responses based on user queries.
- **Tools**: Integrates various tools for hotel information and customer support.

### 5. State Management
- **State**: Manages the state of the conversation, including messages exchanged.

## Usage Flow
1. The user sends a request to the Chat Endpoint.
2. The request is processed, and the appropriate response is generated using the Assistant Node.
3. The response is sent back to the user through the Chat Response structure.
4. The State Graph manages the flow and context of the conversation.

## Conclusion
This architecture provides a comprehensive overview of the Customer Support Chatbot's structure and how its components interact to deliver a seamless user experience.