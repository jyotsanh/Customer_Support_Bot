import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

api_key = os.getenv('OPENAI_API_KEY')

def get_llm(model:str='google'):
    if model=="google":
        llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=1,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            # other params...
            )
        return llm
    elif model=="openai":
        llm=ChatOpenAI(api_key=api_key,model="gpt-4o-mini", stream_usage=True)
        
        return llm
    elif model=="groq":
        llm = ChatGroq(
                model="mixtral-8x7b-32768",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                # other params...
            )
    return llm
        
def get_embeddings(name:str = None):
   
    if name == "google":
        embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return embeddings 
    else:
        return "Only Open ai embeddings works for now."   