# Orchestrator Agent
# This file manages workflow across all agents
from src.vision_agent import detect_crop_with_llm
from src.symptom_agent import describe_symptoms
from src.disease_agent import diagnose_disease
from src.treatment_agent import give_treatment
from src.regional_agent import get_regional_advice, detect_location_from_text, get_location_based_disease_risks
from src.utils_json_parsing import safe_json_parse
import os
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def orchestrate_pipeline(image_path, user_text="", location=None):
    # Step 1: Detect crop
    crop_info = detect_crop_with_llm(image_path)
    
    if crop_info is None:
        return {"error": "Failed to detect crop"}

    crop_name = crop_info["crop"]

    # If no plant material is detected, stop the pipeline
    if "N/A" in crop_name or "Unknown" in crop_name or "no plant material" in crop_name.lower():
        return {
            "crop_info": crop_info,
            "symptoms": "No plant material detected in the image.",
            "disease_info": {
                "disease_name": "None",
                "confidence": "high",
                "reasoning": "The system correctly identified that the image does not contain a supported crop leaf."
            },
            "treatment_info": {
                "treatment_steps": ["Please upload a clear image of a crop leaf from our supported dataset (e.g., Tomato, Potato, Corn, Apple, etc.)"],
                "safety_precautions": []
            }
        }

    # Step 2: Describe symptoms
    symptoms = describe_symptoms(crop_name, image_path)

    # Step 3: Diagnose disease
    disease_info = diagnose_disease(crop_name, symptoms)
    if disease_info is None:
        disease_info = {"disease_name": "Unknown", "reasoning": "Failed LLM diagnosis", "confidence": "low"}

    # Step 4: Provide treatment
    disease_name = disease_info.get("disease_name", "Unknown")
    treatment_info = give_treatment(crop_name, disease_name)
    if treatment_info is None:
        treatment_info = {"treatment_steps": [], "safety_precautions": []}

    # Step 5: Get regional advice if location is available
    regional_advice = None
    if location:
        regional_advice = get_regional_advice(location, crop_name, user_text)
        # Add location-specific disease risks
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

    return result
