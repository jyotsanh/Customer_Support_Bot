# Customer Support Chatbot

## Project Structure

customer-support-chatbot/
│
├── src/
│   ├── main.py                 # Main application entry point
│   │
│   ├── api/
│   │   └── chat_routes.py      # API routes for chat interactions
│   │
│   ├── core/
│   │   ├── init.py
│   │   ├── state.py            # State management for LangGraph
│   │   └── assistant.py        # Assistant class and core logic
│   │
│   ├── graphs/
│   │   ├── init.py
│   │   ├── part_1_graph.py     # Part 1 of the graph (if needed)
│   │   └── part_2_graph.py     # Part 2 of the graph
│   │
│   ├── tools/
│   │   ├── init.py
│   │   ├── tavily_search.py    # Tavily search tool
│   │   └── flight_info.py      # Flight information retrieval tool
│   │
│   ├── prompts/
│   │   ├── init.py
│   │   └── primary_assistant.py # Prompt templates
│   │
│   └── config/
│       ├── init.py
│       └── settings.py         # Configuration management
│
├── tests/
│   ├── unit/
│   │   ├── test_assistant.py
│   │   ├── test_tools.py
│   │   └── test_prompts.py
│   │
│   └── integration/
│       └── test_chat_flow.py
│
├── docs/
│   ├── architecture.md
│   └── api_documentation.md
│
├── logs/                       # Application logs
│
├── scripts/
│   ├── setup.sh
│   └── deploy.sh
│
├── requirements.txt
├── .env                        # Environment variables
├── .gitignore
└── README.md