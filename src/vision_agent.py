import google.generativeai as genai
from PIL import Image
from src.utils_json_parsing import safe_json_parse
import os
import streamlit as st
import io
from src.schemas import CropDetection
from src.factory import AIClientFactory
from src.logger import logger

model = AIClientFactory.get_gemini_model()

@st.cache_data(show_spinner=False)
def _detect_crop_cached(image_bytes):
    """Internal cached function using image bytes as the key"""
    img = Image.open(io.BytesIO(image_bytes))
    
    prompt = f"""
    You are an expert plant pathologist and botanist.
    Analyze the image carefully.
    
    CRITICAL INSTRUCTION: If the image DOES NOT contain a plant, leaf, or crop (for example, if it is an animal, a person, or a random object), you MUST return "N/A" for the crop name. Do not attempt to guess a crop if there is no plant material.

    If it IS a plant leaf, observe the leaf shape, margin, vein patterns, and any disease symptoms.
    
    Here is the list of supported crops:
    - Apple
    - Blueberry
    - Cherry
    - Corn
    - Grape
    - Orange
    - Peach
    - Pepper
    - Potato
    - Raspberry
    - Soybean
    - Squash
    - Strawberry
    - Tomato

    Deduce which of these crops the leaf belongs to.
    
    Return ONLY JSON matching this format:
    {{
      "reasoning": "Detailed analysis leading to your conclusion. If it's not a plant, explain why.",
      "crop": "Exact name of one of the supported crops, OR 'N/A' if not a plant",
      "confidence": "high / medium / low",
      "alternatives": ["possible option1", "option2"]
    }}
    """
    try:
        logger.info("Calling Gemini Vision API for crop detection...")
        result = model.generate_content([prompt, img], generation_config={"response_mime_type": "application/json"})
        data = safe_json_parse(result.text)
        if data:
            validated = CropDetection(**data)
            logger.info(f"Detected crop: {validated.crop} (Confidence: {validated.confidence})")
            return validated.dict()
        return {"crop": "Unknown", "confidence": "low", "alternatives": []}
    except Exception as e:
        logger.error(f"Error in vision agent: {e}")
        return {"crop": "Unknown", "confidence": "low", "alternatives": []}

def detect_crop_with_llm(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return _detect_crop_cached(image_bytes)
