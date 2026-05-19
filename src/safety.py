from src.factory import AIClientFactory
from src.api_resilience import retry_external_api_call
import os

class SafetyInterceptor:
    def __init__(self):
        self.llm = AIClientFactory.get_llm(model_name="llama-3.1-8b-instant", temperature=0)
        self.keywords = [
            "crop", "plant", "leaf", "farm", "agriculture", "soil", "pest", "disease",
            "fertilizer", "harvest", "seed", "irrigation", "weather", "seasonal",
            "ug", "pg", "degree", "research", "career", "education",
            "hello", "hi", "hey", "i am", "my name", "who are you", "what are you"
        ]
        self.hindi_keywords = [
            "कृषि", "फसल", "पौधा", "पत्ता", "खेत", "मिट्टी", "कीट", "रोग",
            "उर्वरक", "जल", "मौसम", "बीज", "सिंचाई", "फसलें", "विवेक", "बिल्ली"
        ]
        self.tamil_keywords = [
            "விவசாயம்", "பயிர்", "தாவரம்", "இலை", "நிலம்", "மண்", "பூச்சி",
            "நோய்", "நதி", "நீர்", "மழை", "மிளகாய்", "தக்காளி",
            "விதை", "சாகுபடி", "பாதிப்பு", "உர", "நீர்ப்பாசனம்", "கரும்பு"
        ]


    def is_agricultural_query(self, text: str) -> bool:
        if not text:
            return True # Assume image-only or empty is handled elsewhere
        
        # Fast keyword check
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in self.keywords):
            return True
        if any(keyword in text for keyword in self.hindi_keywords):
            return True
        if any(keyword in text for keyword in self.tamil_keywords):
            return True
        
        # LLM check for semantic meaning in any language
        prompt = f"""
        Analyze if the following query is:
        1. Related to agriculture, plants, farming, crop diseases, or agricultural technology.
        2. Related to agricultural education, research, or careers.
        3. A generic conversational greeting, a personal introduction (e.g., "I am [name]"), or a question about the assistant's identity.
        
        The query may be written in English, Hindi, Tamil, or another regional Indian language.
        Query: "{text}"
        
        Respond with ONLY 'YES' if it matches ANY of these criteria.
        Only respond with 'NO' if the query is completely unrelated to agriculture and is not a common conversational greeting/introduction.
        """

        try:
            response = retry_external_api_call(self.llm.invoke, prompt).content.strip().upper()
            return "YES" in response
        except Exception:
            return True # Fail safe

    def is_safe_image(self, image_path: str) -> bool:
        # Placeholder for image safety (e.g., using Gemini to check if it's actually a plant)
        # For now, we rely on the vision agent's internal detection.
        return True

safety_interceptor = SafetyInterceptor()
