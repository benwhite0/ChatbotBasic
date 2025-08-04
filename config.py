# config.py
import os
from dotenv import load_dotenv

def load_api_key() -> str | None:
    """
    Loads the OpenAI API key from a .env file.

    Returns:
        The API key if found, otherwise None.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEYY")