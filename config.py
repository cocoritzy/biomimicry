# config.py
import os
from dotenv import load_dotenv
import openai

load_dotenv()
AI_TOKEN = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=AI_TOKEN)
