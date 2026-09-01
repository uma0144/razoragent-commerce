import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Default Bounded Gating Limits (INR)
    DEFAULT_MAX_TX_LIMIT = 5000.0        # Max single purchase without 2FA
    DEFAULT_SESSION_BUDGET = 15000.0     # Max total session budget
    DEFAULT_VELOCITY_LIMIT = 3           # Max transactions per 60 seconds
