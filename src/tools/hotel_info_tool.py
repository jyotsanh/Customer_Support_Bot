# langchain
from langchain_chroma import Chroma
from langchain_core.tools import tool

# tools
from config.settings import get_embeddings

# from models.db import VectorStore
embedding_function = get_embeddings(name = "google")
hotel_info = "hotel_info"

@tool
def get_info_about_hotel_bomo(query: str) -> str:
    """
    Retrieves any information about a hotel Bomo.
    
    Args:
        query (str): The user's query.
    
    Returns:    
        str: The information about the hotel.
    """
    try:
        print("---------Using get_hotel_info tool---------")
        vector_store = Chroma(
                        persist_directory=f"./Chroma/{hotel_info}_Chroma", 
                        embedding_function=embedding_function,
                        collection_name="hotel_info"
                        )
        docs = vector_store.similarity_search(query, k=4)
        print("------docs-------")
        print(docs)
        print("------end---------")
        return docs
    except Exception as e:
        print(f"Error in get_hotel_info tool: {e}")
        return "error fetching the similar docs for the hotel"