import os
import random
import re
import string
from dotenv import load_dotenv
load_dotenv()

# langhcain
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# smtp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_llm(model:str='google'):
    if model=="google":
        llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=1,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            # other params...
            )
        return llm
    elif model=="openai":
        llm=ChatOpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                model="gpt-4o-mini", 
                temperature=0,
                stream_usage=True
            )
        
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
      
def send_email(smtp_host, smtp_port, sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach the email body
        message.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Upgrade connection to secure
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

  
def get_embeddings(name:str = None):
   
    if name == "google":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return embeddings 
    else:
        return "Only Google embeddings works for now."   
    
# Function to validate phone number (10 digits)
def validate_phone_number(phone: str) -> bool:
    """Validate phone number to be exactly 10 digits."""
    return len(phone) == 10 and phone.isdigit()

# Function to validate email address format
def validate_email(email: str) -> bool:
    """Validate email format using a simple regex pattern."""
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))

def generate_unique_verification_code(conn):
    """
    Generate a unique 6-digit verification code.
    
    Args:
        conn (sqlite3.Connection): Database connection to check for existing codes.
    
    Returns:
        str: A unique 6-digit verification code.
    """
    while True:
        # Generate a random 6-digit code
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # Check if the code is unique in the database
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers_with_keys WHERE verification_code = ?", (verification_code,))
        
        # If the code is unique (count is 0), return it
        if cursor.fetchone()[0] == 0:
            return verification_code

def send_verification_email(email: str, verification_code: str):
    """
    Send verification code to customer's email.
    
    Args:
        email (str): Customer's email address
        verification_code (str): 6-digit verification code
    
    Note: Implement actual email sending logic using a library like smtplib
    """
    send_email(
        smtp_host=os.getenv("SMTP_HOST"),
        smtp_port=os.getenv("SMTP_PORT"),
        sender_email=os.getenv("EMAIL"),
        sender_password=os.getenv("EMAIL_PASSWORD"),
        recipient_email=email,
        subject="Verification Code",
        body=f"Your verification code is: {verification_code}"
    )
    print("Email sent successfully!")
    print(f"Sending verification code {verification_code} to {email}")
