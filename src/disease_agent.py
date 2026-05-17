# Disease Agent: decides final disease prediction using combined features

from src.utils_json_parsing import safe_json_parse
from src.plant_village import PLANTVILLAGE_CLASSES
from src.disease_rag import (
    get_disease_info,
    search_disease_by_symptoms,
    get_treatment_for_disease,
    get_prevention_methods
)
from src.schemas import DiseaseDiagnosis
import os

from src.factory import AIClientFactory

llm = AIClientFactory.get_llm()


def diagnose_disease(crop_name, symptoms, cv_prediction=None):
    structured_llm = llm.with_structured_output(DiseaseDiagnosis)
    """
    Enhanced disease diagnosis using LLM + RAG knowledge base.
    Serves as the Pathfinder Reasoning Layer to verify local CV predictions,
    or falls back to zero-shot guessing if the CV model is inactive.

    Args:
        crop_name: Name of the crop (e.g., "tomato")
        symptoms: Description of symptoms from symptom agent
        cv_prediction: Optional dict from local CV classifier containing crop, disease_name, confidence, source

    Returns:
        Dictionary with disease info, treatments, and prevention
    """
    try:
        if cv_prediction:
            disease_name = cv_prediction["disease_name"]
            
            # Fetch detailed pathology, treatments, and prevention from RAG for verification
            detailed_info = get_disease_info(disease_name, k=1)
            treatments = get_treatment_for_disease(disease_name, k=1)
            prevention = get_prevention_methods(disease_name, k=1)

            rag_context = ""
            if detailed_info:
                rag_context += f"DISEASE PATHOLOGY DETAILS:\n{detailed_info[0]}\n\n"
            if prevention:
                rag_context += f"PREVENTION PROTOCOLS:\n{prevention}\n"

            prompt = f"""
You are an expert plant pathologist and AI verifier acting as the "Pathfinder Reasoning Layer".
A local Computer Vision (CV) model has classified a leaf disease. Your role is to cross-reference and verify if the leaf visual symptoms match the known pathology for this disease.

Crop Name: {crop_name}
CV Predicted Disease: {disease_name} (Confidence: {round(cv_prediction["confidence"] * 100, 2)}%)
Extracted Visual Symptoms: {symptoms}

RAG PATHOLOGY REFERENCE INFORMATION:
{rag_context}

Please analyze if the extracted symptoms (spots, margin discoloration, lesions, leaf curling) are consistent with the pathology of {disease_name} described in the database.
Formulate a clear verification explanation, explaining the visual markers and their correlation.
Set the final disease_name to exactly "{disease_name}".
"""
            diagnosis = structured_llm.invoke(prompt)

            if diagnosis:
                diagnosis.disease_name = disease_name
                diagnosis.detailed_info = detailed_info[0] if detailed_info else ""
                diagnosis.treatments = treatments[0] if treatments else ""
                diagnosis.prevention = prevention if prevention else ""
                return diagnosis.dict()

        else:
            # Filter classes list to only include options belonging to crop_name
            crop_key = crop_name.lower().strip()
            if "cherry" in crop_key:
                crop_key = "cherry"
            elif "corn" in crop_key or "maize" in crop_key:
                crop_key = "corn"
            elif "pepper" in crop_key:
                crop_key = "pepper"
            
            filtered_classes = [cls for cls in PLANTVILLAGE_CLASSES if crop_key in cls.lower()]
            if not filtered_classes:
                filtered_classes = PLANTVILLAGE_CLASSES
            classes_list = "\n".join(filtered_classes)

            symptom_matches = search_disease_by_symptoms(symptoms, crop_name=crop_name, k=2)

            # Build enhanced prompt with RAG context
            rag_context = ""
            if symptom_matches:
                rag_context = "\n\nRELEVANT DISEASE INFORMATION:\n" + "\n---\n".join(symptom_matches[:1])

            prompt = f"""
You are an expert agricultural disease expert performing fallback zero-shot diagnosis.
Crop: {crop_name}
Symptoms: {symptoms}

{rag_context}

Diagnose ONLY from this PlantVillage list:
{classes_list}
"""
            diagnosis = structured_llm.invoke(prompt)

            if diagnosis and diagnosis.disease_name:
                disease_name = diagnosis.disease_name

                # Get detailed information from RAG knowledge base
                detailed_info = get_disease_info(disease_name, k=1)
                treatments = get_treatment_for_disease(disease_name, k=1)
                prevention = get_prevention_methods(disease_name, k=1)

                # Enhance the diagnosis with RAG data
                diagnosis.detailed_info = detailed_info[0] if detailed_info else ""
                diagnosis.treatments = treatments[0] if treatments else ""
                diagnosis.prevention = prevention if prevention else ""

                return diagnosis.dict()

    except Exception as e:
        print(f"Disease diagnosis error: {e}")

    # Fallback: return basic diagnosis
    fallback_disease = cv_prediction["disease_name"] if cv_prediction else "Unknown"
    return {
        "disease_name": fallback_disease,
        "confidence": "low",
        "reasoning": "Diagnosis verification failed - please consult a local agricultural extension expert.",
        "detailed_info": "",
        "treatments": "",
        "prevention": ""
    }

