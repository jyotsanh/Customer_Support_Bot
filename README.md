# Customer Support Chatbot

## Project Structure
### Directory Overview

- `src/`: Main source code directory
  - `api/`: API routes and endpoints
  - `core/`: Core application logic and state management
  - `graphs/`: LangGraph configurations
  - `tools/`: External tool integrations
  - `prompts/`: Prompt templates and configurations
  - `config/`: Application settings and configurations

- `tests/`: Test suites
  - `unit/`: Unit test cases
  - `integration/`: Integration test cases

- `docs/`: Project documentation
- `logs/`: Application log storage
- `scripts/`: Deployment and setup scripts

## Key Components

- **FastAPI**: Web framework for building the API
- **LangGraph**: Conversational AI graph management
- **Google Generative AI**: Language model
- **Tavily Search**: Information retrieval tool

## Setup and Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
4. Set up environment variables in .env
5. Run the application:
    ```
    uvicorn src.main:app --reload
    ```