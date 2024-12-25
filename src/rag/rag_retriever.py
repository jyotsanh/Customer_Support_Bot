from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import get_embeddings
from langchain.tools.retriever import create_retriever_tool

hotel_info = "hotel_info"
vector_store = Chroma(
                        persist_directory=f"./Chroma/{hotel_info}_Chroma", 
                        embedding_function=get_embeddings(name = "google"),
                        collection_name="hotel_info"
                    )

retriever = vector_store.as_retriever()
def get_tools():
    retriever_tool = create_retriever_tool(
        retriever,
        "retrieve_blog_posts",
        "Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
    )

    tools = [retriever_tool]
    return tools    