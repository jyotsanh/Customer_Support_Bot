#langchain
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# libs
import json
import traceback

# src/config
from config.settings import get_embeddings
import json

def process_hotel_info_to_documents(hotel_data):
    """Convert hotel information into document format."""
    documents = []
    
    # Process basic hotel information
    basic_info = f"""
    Hotel Name: {hotel_data['hotel_name']}
    Location: {hotel_data['location']['address']}
    Description: {hotel_data['description']}
    Airport Distance: {hotel_data['location']['proximity_to_airport']}
    """
    documents.append(Document(
        page_content=basic_info,
        metadata={
            "type": "basic_info",
            "hotel_name": hotel_data['hotel_name']
        }
    ))
    
    # Process features
    features_info = "Hotel Features:\n" + "\n".join(f"- {feature}" for feature in hotel_data['features'])
    documents.append(Document(
        page_content=features_info,
        metadata={
            "type": "features",
            "hotel_name": hotel_data['hotel_name']
        }
    ))
    
    # Process rooms
    for room in hotel_data['rooms']:
        room_info = f"""
        Room Type: {room['type']}
        Price: ${room['price_per_night']} per night
        Description: {room['description']}
        Capacity: {room['capacity']} persons
        Amenities: {', '.join(room['amenities'])}
        """
        documents.append(Document(
            page_content=room_info,
            metadata={
                "type": "room",
                "room_type": room['type'],
                "hotel_name": hotel_data['hotel_name']
            }
        ))
    
    # Process dining options
    for restaurant in hotel_data['dining']:
        dining_info = f"""
        Restaurant: {restaurant['name']}
        Cuisine: {restaurant['cuisine']}
        Timing: {restaurant['timing']}
        Highlights: {', '.join(restaurant['highlights'])}
        """
        documents.append(Document(
            page_content=dining_info,
            metadata={
                "type": "dining",
                "restaurant_name": restaurant['name'],
                "hotel_name": hotel_data['hotel_name']
            }
        ))
    
    # Process activities
    activities_info = "Activities:\n" + "\n".join(f"- {activity}" for activity in hotel_data['activities'])
    documents.append(Document(
        page_content=activities_info,
        metadata={
            "type": "activities",
            "hotel_name": hotel_data['hotel_name']
        }
    ))
    
    # Process policies
    policies_info = f"""
    Check-in: {hotel_data['policies']['check_in']}
    Check-out: {hotel_data['policies']['check_out']}
    Cancellation: {hotel_data['policies']['cancellation']}
    Pet Policy: {hotel_data['policies']['pet_policy']}
    """
    documents.append(Document(
        page_content=policies_info,
        metadata={
            "type": "policies",
            "hotel_name": hotel_data['hotel_name']
        }
    ))
    
    # Process reviews
    for review in hotel_data['reviews']:
        review_info = f"""
        Review by {review['author']}
        Rating: {review['rating']}
        Comment: {review['comment']}
        """
        documents.append(Document(
            page_content=review_info,
            metadata={
                "type": "review",
                "author": review['author'],
                "hotel_name": hotel_data['hotel_name']
            }
        ))
    print("---")
    contact_info = hotel_data['contact_info']
    contact_infoss = f"""
    Phone: {contact_info['phone']}
    Email: {contact_info['email']}
    Website: {contact_info['website']}
    """
    
    documents.append(Document(
        page_content=contact_infoss,
        metadata={
            "type": "contact_info",
            "hotel_name": hotel_data['hotel_name']
        }
    ))
    print("---")
    return documents

def create_hotel_info_vector_store(hotel_data):
    try:
        embedding_function = get_embeddings(name="google")
        
        documents = []
        documents.extend(process_hotel_info_to_documents(hotel_data))
        
        if not documents:
            print("No documents were created. Check the input data.")
            return
            
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Create and return Chroma vector store
        vector_store = Chroma.from_documents(
            split_docs, 
            persist_directory="./Chroma/new_hotel_info_Chroma", 
            embedding=embedding_function,
            collection_name="hotel_info"
        )
        
        print("New vector store created and saved.")
        return vector_store
        
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

if __name__ == "__main__":
    # Your hotel data JSON
    hotel_data = {
    "hotel_name": "Bomo",
    "location": {
      "address": "Lazimpat, Kathmandu, Nepal",
      "latitude": 27.7226,
      "longitude": 85.3223,
      "proximity_to_airport": "6 km from Tribhuvan International Airport"
    },
    "description": "Hotel Bomo is a boutique luxury property nestled in the heart of Kathmandu, blending traditional Nepali architecture with modern comfort. It's an ideal choice for leisure and business travelers seeking a serene yet accessible retreat.",
    "features": [
      "Traditional Nepali design with modern amenities",
      "Rooftop terrace with panoramic city views",
      "Spa and wellness center offering Ayurvedic treatments",
      "Free high-speed Wi-Fi",
      "Conference and meeting rooms",
      "Multi-cuisine dining options",
      "Fitness center",
      "Airport shuttle service"
    ],
    "rooms": [
      {
        "type": "Deluxe Room",
        "price_per_night": 120,
        "description": "Comfortable room with traditional Nepali décor, a queen-sized bed, and modern amenities.",
        "capacity": 2,
        "amenities": [
          "Air conditioning",
          "Flat-screen TV",
          "Mini bar",
          "Complimentary tea and coffee",
          "Rainfall shower"
        ]
      },
      {
        "type": "Executive Suite",
        "price_per_night": 200,
        "description": "Spacious suite featuring a living room, king-sized bed, and a private balcony with city views.",
        "capacity": 3,
        "amenities": [
          "Private balcony",
          "Separate living area",
          "Luxury bathroom with bathtub",
          "Work desk",
          "Complimentary bottled water"
        ]
      },
      {
        "type": "Heritage Suite",
        "price_per_night": 300,
        "description": "A luxurious suite adorned with traditional Nepali craftsmanship, featuring a private terrace and exclusive amenities.",
        "capacity": 2,
        "amenities": [
          "Private terrace",
          "Handcrafted wooden furniture",
          "Complimentary Nepali tea service",
          "Exclusive spa discounts",
          "Butler service"
        ]
      }
    ],
    "dining": [
      {
        "name": "Thakali Kitchen",
        "cuisine": "Authentic Nepali and Thakali cuisine",
        "timing": "7:00 AM - 10:00 PM",
        "highlights": ["Traditional Nepali Thali", "Locally sourced ingredients"]
      },
      {
        "name": "SkyLounge",
        "cuisine": "Continental and Asian fusion",
        "timing": "5:00 PM - 11:00 PM",
        "highlights": ["Rooftop dining", "Live music events"]
      }
    ],
    "activities": [
      "Guided tours to cultural heritage sites",
      "Yoga and meditation sessions",
      "Cooking classes on traditional Nepali cuisine",
      "Evening cultural performances",
      "Hiking and trekking coordination services"
    ],
    "reviews": [
      {
        "author": "Ram Prasad",
        "rating": 4.7,
        "comment": "A perfect blend of Nepali tradition and modern luxury. Loved the rooftop views!"
      },
      {
        "author": "Sita Shrestha",
        "rating": 4.9,
        "comment": "The Heritage Suite was amazing, and the staff were very hospitable. Highly recommended!"
      }
    ],
    "policies": {
      "check_in": "2:00 PM",
      "check_out": "12:00 PM",
      "cancellation": "Free cancellation up to 24 hours before check-in",
      "pet_policy": "Pets are not allowed."
    },
    "contact_info": {
      "phone": "+977-1-442-1234",
      "email": "info@hotelbomo.com",
      "website": "https://www.hotelbomo.com"
    }
  }
  
    
    vector_store = create_hotel_info_vector_store(hotel_data)