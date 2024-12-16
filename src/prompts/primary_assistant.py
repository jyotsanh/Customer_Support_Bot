from tools.math_tool import multiply, add, subtract
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


part_2_tools = [
        TavilySearchResults(max_results=1),
        add,
        subtract,
        multiply
    ]

def create_primary_assistant_runnable():
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful Tutor Assistant. "
                " Use the provided tools to solve the user's math problem to assist the user's queries. "
                " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                " If a search comes up empty, expand your search before giving up.",
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)

    
    # part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)
    part_2_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_2_tools)
    print("Returning the assistant runnable with tools")
    return part_2_assistant_runnable