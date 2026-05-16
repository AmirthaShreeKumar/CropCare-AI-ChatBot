import os
import google.generativeai as genai
from langchain_groq import ChatGroq
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIClientFactory:
    _instances = {}

    @classmethod
    def get_llm(cls, model_name="llama-3.1-8b-instant", temperature=0):
        key = f"llm_{model_name}_{temperature}"
        if key not in cls._instances:
            cls._instances[key] = ChatGroq(
                groq_api_key=os.getenv("GROQ_API_KEY"),
                model_name=model_name,
                temperature=temperature
            )
        return cls._instances[key]

    @classmethod
    def get_groq_client(cls):
        if "groq_raw" not in cls._instances:
            cls._instances["groq_raw"] = Groq(api_key=os.getenv("GROQ_API_KEY"))
        return cls._instances["groq_raw"]

    @classmethod
    def get_gemini_model(cls, model_name="models/gemini-2.5-flash"):
        if f"gemini_{model_name}" not in cls._instances:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            cls._instances[f"gemini_{model_name}"] = genai.GenerativeModel(model_name)
        return cls._instances[f"gemini_{model_name}"]
