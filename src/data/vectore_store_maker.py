#langchain
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# libs
import json
import traceback

# src/config
from config.settings import get_embeddings

def flatten_metadata(metadata):
    """
    Flatten nested dictionaries in metadata.
    Converts nested dicts to string representations.
    """
    flattened = {}
    for key, value in metadata.items():
        if isinstance(value, dict):
            # Convert dict to a string representation
            flattened[key] = str(value)
        elif isinstance(value, list):
            # Convert list to a string representation
            flattened[key] = ', '.join(map(str, value))
        else:
            # Keep original value for simple types
            flattened[key] = value
    return flattened

def process_hotel_info_to_documents(data):
    documents = []
    
    # Check if the input is a single hotel dictionary or a list of hotels
    hotel_list = data if isinstance(data, list) else [data]
    
    print(f"Number of hotels found: {len(hotel_list)}")
    
    # Process general hotel information
    for hotel in hotel_list:
        try:
            if not isinstance(hotel, dict):
                print(f"Skipping invalid hotel entry: {hotel}")
                continue

            print(f"\n--- Processing Hotel: {hotel.get('hotel_name', 'Unknown')} ---")

            # Create general hotel document
            general_info = Document(
                page_content=hotel.get("description", "No description available."),
                metadata=flatten_metadata({
                    "hotel_name": hotel.get("hotel_name", "Unknown"),
                    "location": hotel.get("location", {}),
                    "features": hotel.get("features", []),
                    "contact_info": hotel.get("contact_info", {})
                })
            )
            documents.append(general_info)
            print(f"Created general hotel document for {hotel.get('hotel_name', 'Unknown')}")

            # Process room details
            for room in hotel.get("rooms", []):
                room_info = Document(
                    page_content=room.get("description", "No room description available."),
                    metadata=flatten_metadata({
                        "hotel_name": hotel.get("hotel_name", "Unknown"),
                        "room_type": room.get("type", "Unknown"),
                        "price_per_night": room.get("price_per_night", "Unknown"),
                        "capacity": room.get("capacity", "Unknown"),
                        "amenities": room.get("amenities", [])
                    })
                )
                documents.append(room_info)
                print(f"Created room document: {room.get('type', 'Unknown')} room")

            # Process dining options
            for dining in hotel.get("dining", []):
                dining_info = Document(
                    page_content=dining.get("name", "Unknown dining option") + " - " + 
                                 dining.get("cuisine", "Cuisine details unavailable."),
                    metadata=flatten_metadata({
                        "hotel_name": hotel.get("hotel_name", "Unknown"),
                        "dining_timings": dining.get("timing", "Unknown"),
                        "highlights": dining.get("highlights", [])
                    })
                )
                documents.append(dining_info)
                print(f"Created dining document: {dining.get('name', 'Unknown')}")

            # Process activities
            for activity in hotel.get("activities", []):
                activity_info = Document(
                    page_content=activity,
                    metadata=flatten_metadata({
                        "hotel_name": hotel.get("hotel_name", "Unknown"),
                        "type": "activity"
                    })
                )
                documents.append(activity_info)
                print(f"Created activity document: {activity}")

            # Process reviews
            for review in hotel.get("reviews", []):
                review_info = Document(
                    page_content=review.get("comment", "No review comment available."),
                    metadata=flatten_metadata({
                        "hotel_name": hotel.get("hotel_name", "Unknown"),
                        "review_author": review.get("author", "Unknown"),
                        "rating": review.get("rating", "Unknown")
                    })
                )
                documents.append(review_info)
                print(f"Created review document by {review.get('author', 'Unknown')}")
                
            # Process policies
            for policies in hotel.get("policies", []):
                policies_info = Document(
                    page_content=policies,
                    metadata=flatten_metadata({
                        "hotel_name": hotel.get("hotel_name", "Unknown"),
                        "type": "policies"
                    })
                )
                documents.append(policies_info)
                print(f"Created policies document")
            # Process Conatct Info
            for contact in hotel.get("contact_info", []):
                conatct_info = Document(
                    page_content=contact,
                    metadata=flatten_metadata({
                        "hotel_name": hotel.get("hotel_name", "Unknown"),
                        "type": "Contact Info"
                    })
                )
                documents.append(conatct_info)
                print(f"Created contact document")

        except Exception as e:
            print(f"Error processing hotel: {hotel.get('hotel_name', 'Unknown')}")
            print(traceback.format_exc())

    print(f"\nTotal documents created: {len(documents)}")
    return documents


def create_hotel_info_vector_store():
    try:
        embedding_function = get_embeddings(name = "google")
        
        with open("./data/hotel_info.json",'r', encoding='utf-8') as info_file:
            info_data = json.load(info_file)
            
            print(type(info_data))  # Check the type and first two items of the data
        print(info_data)

        
        
        documents = []
        # documents.extend(process_prices_to_documents(prices_data))
        documents.extend(process_hotel_info_to_documents(info_data))
        
        print("-------------------------")
        print(documents)
        print("------------------------------------")
        if not documents:
            print("No documents were created. Check the input data.")
            return
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        split_docs = text_splitter.split_documents(documents)
        
        
        hotel_info="hotel_info"
        # Create and return Chroma vector store
        vector_store = Chroma.from_documents(
            split_docs, 
            persist_directory=f"./Chroma/{hotel_info}_Chroma", 
            embedding=embedding_function,
            collection_name="hotel_info"
        )
        
        print("New vector store created and saved.")
        
    except Exception as e:
        print(f"Error creating vector store: {e}")
if __name__ == "__main__":
    create_hotel_info_vector_store()