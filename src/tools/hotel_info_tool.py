# langchain
from langchain_chroma import Chroma
from langchain_core.tools import tool

# tools
from config.settings import get_embeddings

# from models.db import VectorStore
embedding_function = get_embeddings(name = "google")
hotel_info = "hotel_info"
vector_store = Chroma(
                    persist_directory=f"./Chroma/{hotel_info}_Chroma", 
                    embedding_function=embedding_function,
                    collection_name="hotel_info"
                    )
@tool
def get_hotel_info(query: str) -> str:
    """get_hotel_info
    Retrieve information about a hotel based on a user's query.
    
    Args:
        query (str): The user's query.
    
    Returns:    
        str: The information about the hotel.
    """
    docs = vector_store.similarity_search(query, k=4)
    print("------docs-------")
    print(docs)
    print("------end---------")
    return docs