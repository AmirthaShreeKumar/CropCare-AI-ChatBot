import google.generativeai as genai
from PIL import Image
from src.utils_json_parsing import safe_json_parse
from src.plant_village import PLANTVILLAGE_CLASSES
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
    dataset_classes = "\n".join(PLANTVILLAGE_CLASSES)
    
    prompt = f"""
    You are an expert plant pathologist and botanist.
    Analyze the image of the leaf very carefully. First, observe the leaf shape, margin (edges), vein patterns, and texture.
    Second, observe any disease symptoms (like spots, lesions, discoloration).
    
    Here is the exact dataset of crops AND their possible diseases:
    {dataset_classes}
    
    Use BOTH the leaf shape AND the specific disease symptoms you see to deduce which crop this is. 
    Return ONLY JSON like:
    {{
      "reasoning": "Detailed analysis of leaf shape, margin, and veins leading to your conclusion.",
      "crop": "name of the crop",
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
