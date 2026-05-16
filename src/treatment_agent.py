# Treatment Agent: recommends cure/prevention steps using RAG knowledge base

from src.utils_json_parsing import safe_json_parse
from src.disease_rag import get_treatment_for_disease, get_prevention_methods
import os
from src.schemas import TreatmentPlan
from src.factory import AIClientFactory

llm = AIClientFactory.get_llm()


def give_treatment(crop_name, disease_name):
    structured_llm = llm.with_structured_output(TreatmentPlan)
    """
    Enhanced treatment recommendations using RAG knowledge base

    Args:
        crop_name: Name of the crop
        disease_name: Name of the diagnosed disease

    Returns:
        Dictionary with treatment_steps and safety_precautions
    """

    # First, try to get treatment info from RAG knowledge base
    rag_treatments = get_treatment_for_disease(disease_name, k=1)
    rag_prevention = get_prevention_methods(disease_name, k=1)

    # Build enhanced prompt with RAG context
    rag_context = ""
    if rag_treatments:
        rag_context += f"\n\nTREATMENT KNOWLEDGE:\n{rag_treatments[0]}"
    if rag_prevention:
        rag_context += f"\n\nPREVENTION KNOWLEDGE:\n{rag_prevention}"

    prompt = f"""
You are an agricultural treatment expert.
Provide comprehensive treatment recommendations for {crop_name} affected by {disease_name}.

{rag_context}

Consider:
- Organic and chemical treatment options
- Safety precautions for farmers
- Prevention methods
- Step-by-step treatment process
"""

    try:
        treatment_data = structured_llm.invoke(prompt)

        if treatment_data:
            return treatment_data.dict()

    except Exception as e:
        print(f"Treatment recommendation error: {e}")

    # Fallback treatment
    return {
        "treatment_steps": [
            f"Consult local agricultural extension service for {disease_name} treatment",
            f"Remove and destroy infected plant parts",
            f"Apply appropriate fungicide/insecticide as recommended by experts",
            f"Improve field sanitation and crop rotation"
        ],
        "safety_precautions": [
            "Wear protective clothing when applying chemicals",
            "Follow label instructions carefully",
            "Keep children and pets away from treated areas",
            "Wash hands after handling chemicals"
        ]
    }
