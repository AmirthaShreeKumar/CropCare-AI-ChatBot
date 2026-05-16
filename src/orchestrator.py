import os
import streamlit as st
import io
from src.vision_agent import detect_crop_with_llm
from src.symptom_agent import describe_symptoms
from src.disease_agent import diagnose_disease
from src.treatment_agent import give_treatment
from src.regional_agent import get_regional_advice, detect_location_from_text, get_location_based_disease_risks
from src.utils_json_parsing import safe_json_parse
from src.factory import AIClientFactory
from src.logger import logger

llm = AIClientFactory.get_llm()

MAX_STEPS = 10

@st.cache_data(show_spinner=False)
def _orchestrate_pipeline_cached(image_bytes, user_text="", location=None):
    """Internal cached pipeline orchestration using image bytes as the key"""
    logger.info("Starting pipeline orchestration (cached call)...")
    
    # Save image bytes to a temporary path for agents that still expect a path
    # (Though we should eventually refactor them to take bytes too)
    temp_path = "temp_pipeline_image.jpg"
    with open(temp_path, "wb") as f:
        f.write(image_bytes)
    
    try:
        # Step 1: Detect crop
        logger.info("Step 1: Detecting crop...")
        crop_info = detect_crop_with_llm(temp_path)
        if crop_info is None:
            logger.error("Failed to detect crop.")
            return {"error": "Failed to detect crop"}

        crop_name = crop_info["crop"]
        logger.info(f"Crop detected: {crop_name}")

        # If no plant material is detected, stop the pipeline
        if "N/A" in crop_name or "Unknown" in crop_name or "no plant material" in crop_name.lower():
            logger.warning("No plant material detected in image.")
            return {
                "crop_info": crop_info,
                "symptoms": "No plant material detected in the image.",
                "disease_info": {
                    "disease_name": "None",
                    "confidence": "high",
                    "reasoning": "The system correctly identified that the image does not contain a supported crop leaf."
                },
                "treatment_info": {
                    "treatment_steps": ["Please upload a clear image of a crop leaf from our supported dataset."],
                    "safety_precautions": []
                }
            }

        # Step 2: Describe symptoms
        logger.info("Step 2: Describing symptoms...")
        symptoms = describe_symptoms(crop_name, temp_path)

        # Step 3: Diagnose disease
        logger.info(f"Step 3: Diagnosing disease for {crop_name}...")
        disease_info = diagnose_disease(crop_name, symptoms)
        if disease_info is None:
            logger.warning("Disease diagnosis failed, using fallback.")
            disease_info = {"disease_name": "Unknown", "reasoning": "Failed LLM diagnosis", "confidence": "low"}

        # Step 4: Provide treatment
        disease_name = disease_info.get("disease_name", "Unknown")
        logger.info(f"Step 4: Getting treatment for {disease_name}...")
        treatment_info = give_treatment(crop_name, disease_name)
        if treatment_info is None:
            treatment_info = {"treatment_steps": [], "safety_precautions": []}

        # Step 5: Get regional advice
        regional_advice = None
        if location:
            logger.info(f"Step 5: Fetching regional advice for {location}...")
            regional_advice = get_regional_advice(location, crop_name, user_text)
            disease_risks = get_location_based_disease_risks(location, crop_name)
            if disease_risks:
                disease_info["regional_risks"] = disease_risks

        # Merge final result
        result = {
            "crop_info": crop_info,
            "symptoms": symptoms,
            "disease_info": disease_info,
            "treatment_info": treatment_info
        }

        if regional_advice:
            result["regional_advice"] = regional_advice

        logger.info("Pipeline orchestration completed successfully.")
        return result
        
    finally:
        # Cleanup temporary file used during orchestration
        if os.path.exists(temp_path):
            os.remove(temp_path)

def orchestrate_pipeline(image_path, user_text="", location=None):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return _orchestrate_pipeline_cached(image_bytes, user_text, location)
