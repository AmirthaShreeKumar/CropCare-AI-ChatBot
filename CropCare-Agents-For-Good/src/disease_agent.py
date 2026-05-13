# Disease Agent: decides final disease prediction using combined features

from src.utils_json_parsing import safe_json_parse
from src.plant_village import PLANTVILLAGE_CLASSES
from src.disease_rag import (
    get_disease_info,
    search_disease_by_symptoms,
    get_treatment_for_disease,
    get_prevention_methods
)
import os
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


def diagnose_disease(crop_name, symptoms):
    """
    Enhanced disease diagnosis using LLM + RAG knowledge base

    Args:
        crop_name: Name of the crop (e.g., "tomato")
        symptoms: Description of symptoms from vision agent

    Returns:
        Dictionary with disease info, treatments, and prevention
    """
    classes_list = "\n".join(PLANTVILLAGE_CLASSES)

    # First, try to find diseases based on symptoms using RAG
    symptom_matches = search_disease_by_symptoms(symptoms, k=2)

    # Build enhanced prompt with RAG context
    rag_context = ""
    if symptom_matches:
        rag_context = "\n\nRELEVANT DISEASE INFORMATION:\n" + "\n---\n".join(symptom_matches[:1])

    prompt = f"""
You are an agricultural disease expert.
Crop: {crop_name}
Symptoms: {symptoms}

{rag_context}

Diagnose ONLY from this PlantVillage list:
{classes_list}

Return JSON with these exact fields:
{{
  "disease_name": "exact disease name from list",
  "confidence": "high/medium/low",
  "reasoning": "brief explanation"
}}
"""

    try:
        result = llm.invoke(prompt)
        diagnosis = safe_json_parse(result.content)

        if diagnosis and diagnosis.get("disease_name"):
            disease_name = diagnosis["disease_name"]

            # Get detailed information from RAG knowledge base
            detailed_info = get_disease_info(disease_name, k=1)
            treatments = get_treatment_for_disease(disease_name, k=1)
            prevention = get_prevention_methods(disease_name, k=1)

            # Enhance the diagnosis with RAG data
            enhanced_diagnosis = {
                "disease_name": disease_name,
                "confidence": diagnosis.get("confidence", "medium"),
                "reasoning": diagnosis.get("reasoning", ""),
                "detailed_info": detailed_info[0] if detailed_info else "",
                "treatments": treatments[0] if treatments else "",
                "prevention": prevention if prevention else ""
            }

            return enhanced_diagnosis

    except Exception as e:
        print(f"Disease diagnosis error: {e}")

    # Fallback: return basic diagnosis
    return {
        "disease_name": "Unknown",
        "confidence": "low",
        "reasoning": "Diagnosis failed - please consult local agricultural expert",
        "detailed_info": "",
        "treatments": "",
        "prevention": ""
    }
