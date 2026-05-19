from src.factory import AIClientFactory
from src.api_resilience import retry_external_api_call
from src.logger import logger
import streamlit as st

llm = AIClientFactory.get_llm(model_name="llama-3.1-8b-instant", temperature=0)

@st.cache_data(show_spinner=False)
def autocorrect_and_normalize_query(query: str, preferred_language: str) -> str:
    """
    Uses a fast LLM call to correct common spelling, phonetic, and transliteration mistakes.
    Bridges terms like 'puvanjai' -> 'poonjai' / 'fungus' cleanly while respecting language preferences.
    Specifically designed to catch and fix common speech-to-text / Whisper transcription errors.
    """
    if not query or len(query.strip()) < 2:
        return query

    # Dynamic prompt building based on the selected language to prevent language bleeding
    if preferred_language == "English":
        prompt = f"""
        You are an expert agricultural query autocorrect and normalization engine.
        The user has selected ENGLISH as their preferred language.
        Therefore, your output query MUST be strictly in English. Do NOT output any Tamil or Hindi/Devanagari scripts under any circumstances.
        
        Your job:
        1. Correct any spelling, phonetic, or speech-to-text transcription errors in the query.
        2. Translate regional/transliterated terms directly into standard English vocabulary (e.g. 'poonjai' or 'puvanjai' or 'fafundi' -> 'fungus', 'noi' -> 'disease', 'keeda' -> 'insect/pest', 'elai' -> 'leaf').
        3. If there are phonetic garbles (e.g., 'fafund dhe mikya' or 'puvanjai noi'), identify the intended agricultural meaning and write it in clean English.
        4. Keep the core agricultural query intact, returned in plain English.
        
        Examples:
        - "puvanjai" -> "fungus"
        - "poonjai disease" -> "fungal disease"
        - "tamatar me keeda" -> "insect in tomato"
        - "puchi kadi" -> "insect bite"
        - "bimar paudha" -> "sick plant"
        - "takkali leaf noi" -> "tomato leaf disease"
        - "elai karuhal" -> "leaf blight"
        - "fafund dhe mikya kya hota hai" -> "what happens in fungal disease"
        
        Query to normalize: "{query}"
        
        Return ONLY the corrected English query. Do not explain, do not add intros or outros, do not add quotes.
        """
    elif "Tamil" in preferred_language:
        prompt = f"""
        You are an expert agricultural query autocorrect and normalization engine.
        The user has selected TAMIL (தமிழ்) as their preferred language.
        Therefore, your output query should prioritize standard, grammatically correct Tamil script for Tamil/transliterated terms.
        
        Your job:
        1. Correct any spelling, phonetic, or speech-to-text transcription errors in the query.
        2. Identify and resolve common Tamil phonetic/Whisper character substitution errors:
           - Mixing up small 'ra' (ர/ரு) and big 'ra' (ற/று). For example: "பறுத்தி", "பறுத்தியின்" are speech-to-text failures for "பருத்தி", "பருத்தியின்" (Cotton). You MUST correct this to "பருத்தி".
           - Mixing up 'la' (ல/லு), 'La' (ள/ளு), and 'zha' (ழ/ழு). For example: "காலான்", "காழான்" must be corrected to "காளான்" (fungus/mushroom).
        3. Convert transliterated/phonetic inputs into properly spelled Tamil script.
        4. Do NOT include any English translations, parenthetical notes, or explanations in your output.
        
        Examples:
        - "puvanjai" -> "பூஞ்சை"
        - "poonjai disease" -> "பூஞ்சை நோய்"
        - "puchi kadi" -> "பூச்சி கடி"
        - "takkali leaf noi" -> "தக்காளி இலை நோய்"
        - "elai karuhal" -> "இலை கருகல்"
        - "பறுத்தியின் பயன்கள்" -> "பருத்தியின் பயன்கள்"
        - "காலான் நோய்" -> "காளான் நோய்"
        - "என் மரத்தில் புவுஞ்சைகள் இருக்கின்ற நேரம்" -> "என் மரத்தில் பூஞ்சை காளான் இருக்கும் போது"
        
        Query to normalize: "{query}"
        
        Return ONLY the corrected Tamil query. Do not explain, do not add intros or outros, do not add quotes.
        """
    else: # Hindi
        prompt = f"""
        You are an expert agricultural query autocorrect and normalization engine.
        The user has selected HINDI (हिंदी) as their preferred language.
        Therefore, your output query should prioritize standard Hindi Devanagari script for Hindi/transliterated terms.
        
        Your job:
        1. Correct any spelling, phonetic, or speech-to-text transcription errors in the query.
        2. VERY IMPORTANT: Identify speech-to-text / Whisper phonetic mistakes. For example:
           - "fafund dhe mikya", "fafund dhe", "fafund de", "फफूंद दे मिक्या", "फफूंद दे मिका" are speech-to-text transcription failures for "फफूंदी में" (in fungus) or "फफूंद" (fungus). You MUST correct this to "फफूंदी" or "फफूंद".
           - "tamatar me fafund dhe mikya" must be corrected to "टमाटर में फफूंदी".
        3. Convert transliterated/phonetic inputs into properly spelled Devanagari script.
        4. Keep the core agricultural meaning intact.
        5. Do NOT include any English translations, parenthetical notes, or explanations in your output.
        
        Examples:
        - "tamatar me keeda" -> "टमाटर में कीड़ा"
        - "bimar paudha" -> "बीमार पौधा"
        - "patta sukhna" -> "पत्ता सूखना"
        - "khad kab dale" -> "खाद कब डालें"
        - "फफूंद दे मिक्या क्या रोग हो सकता है" -> "फफूंदी में क्या-क्या रोग हो सकते हैं"
        - "टमाटर में फफूंद देह मिक्या क्या होता है" -> "टमाटर में फफूंदी रोग क्या होता है"
        
        Query to normalize: "{query}"
        
        Return ONLY the corrected Hindi query. Do not explain, do not add intros or outros, do not add quotes.
        """

    try:
        response = retry_external_api_call(llm.invoke, prompt).content.strip()
        # Clean any surrounding quotes
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        elif response.startswith("'") and response.endswith("'"):
            response = response[1:-1]
            
        logger.info("Auto-correction match (%s): '%s' -> '%s'", preferred_language, query, response)
        return response
    except Exception as e:
        logger.warning("Query auto-correction failed: %s", e)
        return query
