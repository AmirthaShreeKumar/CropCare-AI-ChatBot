import os
import streamlit as st
import io
import time
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
    
    t_start = time.perf_counter()
    
    # Save image bytes to a temporary path for agents that still expect a path
    temp_path = "temp_pipeline_image.jpg"
    with open(temp_path, "wb") as f:
        f.write(image_bytes)
    
    cv_inference_sec = 0.0
    symptom_analysis_sec = 0.0
    disease_reasoning_sec = 0.0
    treatment_generation_sec = 0.0
    regional_analysis_sec = 0.0
    
    try:
        # Phase 0: Validate if the image contains plant material using the Gemini Gatekeeper
        logger.info("Phase 0: Validating image content...")
        t_val_start = time.perf_counter()
        crop_info = detect_crop_with_llm(temp_path)
        
        if crop_info is None:
            logger.error("Failed to detect crop species.")
            return {"error": "Failed to analyze image content."}
            
        crop_name = crop_info.get("crop", "Unknown")
        logger.info(f"Gatekeeper detected: {crop_name}")

        # If no plant material is detected, stop the pipeline immediately
        if "N/A" in crop_name or "Unknown" in crop_name or "no plant material" in crop_name.lower():
            logger.warning("No plant material detected in image. Rejecting pipeline execution.")
            total_pipeline_sec = round(time.perf_counter() - t_start, 2)
            return {
                "crop_info": crop_info,
                "symptoms": "No plant material detected in the image.",
                "disease_info": {
                    "disease_name": "None",
                    "confidence": "high",
                    "reasoning": crop_info.get("reasoning", "The system correctly identified that the image does not contain a plant or crop leaf."),
                    "prediction_source": "Gemini Vision Gatekeeper",
                    "cv_confidence": None
                },
                "treatment_info": {
                    "treatment_steps": ["Please upload a clear image of a crop leaf from our supported dataset."],
                    "safety_precautions": []
                },
                "performance_metrics": {
                    "cv_inference_sec": round(time.perf_counter() - t_val_start, 2),
                    "symptom_analysis_sec": 0.0,
                    "disease_reasoning_sec": 0.0,
                    "treatment_generation_sec": 0.0,
                    "regional_analysis_sec": 0.0,
                    "total_pipeline_sec": total_pipeline_sec
                }
            }

        # Step 1: Run the local Computer Vision classifier first
        logger.info("Step 1: Running local CV disease classifier...")
        t_cv_start = time.perf_counter()
        classifier = AIClientFactory.get_disease_classifier()
        cv_prediction = classifier.predict(temp_path)

        if cv_prediction is not None:
            # Normal Mode: local deep learning classifier succeeded
            crop_name = cv_prediction["crop"]
            disease_name = cv_prediction["disease_name"]
            confidence = cv_prediction["confidence"]
            logger.info(f"Local CV classifier match: {crop_name} -> {disease_name} (Confidence: {round(confidence * 100, 2)}%)")
            
            crop_info = {
                "crop": crop_name,
                "confidence": "high" if confidence >= 0.75 else ("medium" if confidence >= 0.50 else "low"),
                "reasoning": f"Identified by local deep learning classifier with {round(confidence * 100, 2)}% confidence.",
                "alternatives": []
            }
        else:
            # Fallback Mode: PyTorch missing or weights missing. Zero-shot Gemini Vision is active
            logger.info("Local CV model is unavailable or inactive. Using gatekeeper detection as fallback...")
            # We already have crop_info and crop_name from the gatekeeper
            cv_inference_sec = round(time.perf_counter() - t_cv_start, 2) + round(time.perf_counter() - t_val_start, 2)
            pass
        cv_inference_sec = round(time.perf_counter() - t_cv_start, 2) + round(time.perf_counter() - t_val_start, 2)

        # Step 2: Describe symptoms
        logger.info("Step 2: Describing symptoms...")
        t_sym_start = time.perf_counter()
        symptoms = describe_symptoms(crop_name, temp_path)
        symptom_analysis_sec = round(time.perf_counter() - t_sym_start, 2)

        # Step 3: Diagnose/Verify disease (Pathfinder Reasoning Layer)
        logger.info(f"Step 3: Diagnosing/verifying disease for {crop_name}...")
        t_dis_start = time.perf_counter()
        disease_info = diagnose_disease(crop_name, symptoms, cv_prediction=cv_prediction)
        if disease_info is None:
            logger.warning("Disease diagnosis verification failed, utilizing failover structure.")
            disease_info = {
                "disease_name": cv_prediction["disease_name"] if cv_prediction else "Unknown",
                "reasoning": "Failed LLM diagnosis verification.",
                "confidence": "low"
            }

        # Add visual confidence source badges
        if cv_prediction:
            disease_info["prediction_source"] = "Local CV Model (MobileNetV2)"
            disease_info["cv_confidence"] = cv_prediction["confidence"]
        else:
            disease_info["prediction_source"] = "Fallback Mode: Gemini Vision Analysis"
            disease_info["cv_confidence"] = None
        disease_reasoning_sec = round(time.perf_counter() - t_dis_start, 2)

        # Step 4: Provide treatment
        disease_name = disease_info.get("disease_name", "Unknown")
        logger.info(f"Step 4: Getting treatment for {disease_name}...")
        t_treat_start = time.perf_counter()
        treatment_info = give_treatment(crop_name, disease_name)
        if treatment_info is None:
            treatment_info = {"treatment_steps": [], "safety_precautions": []}
        treatment_generation_sec = round(time.perf_counter() - t_treat_start, 2)

        # Step 5: Get regional advice
        regional_advice = None
        t_reg_start = time.perf_counter()
        if location:
            logger.info(f"Step 5: Fetching regional advice for {location}...")
            regional_advice = get_regional_advice(location, crop_name, user_text)
            disease_risks = get_location_based_disease_risks(location, crop_name)
            if disease_risks:
                disease_info["regional_risks"] = disease_risks
        regional_analysis_sec = round(time.perf_counter() - t_reg_start, 2)

        total_pipeline_sec = round(time.perf_counter() - t_start, 2)

        # Merge final result
        result = {
            "crop_info": crop_info,
            "symptoms": symptoms,
            "disease_info": disease_info,
            "treatment_info": treatment_info,
            "performance_metrics": {
                "cv_inference_sec": cv_inference_sec,
                "symptom_analysis_sec": symptom_analysis_sec,
                "disease_reasoning_sec": disease_reasoning_sec,
                "treatment_generation_sec": treatment_generation_sec,
                "regional_analysis_sec": regional_analysis_sec,
                "total_pipeline_sec": total_pipeline_sec
            }
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
