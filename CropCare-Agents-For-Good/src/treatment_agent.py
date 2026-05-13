# Treatment Agent: recommends cure/prevention steps using RAG knowledge base

from src.utils_json_parsing import safe_json_parse
from src.disease_rag import get_treatment_for_disease, get_prevention_methods
import os
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def give_treatment(crop_name, disease_name):
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

Return JSON with these exact fields:
{{
  "treatment_steps": [
    "Step 1: Description of first treatment action",
    "Step 2: Description of second treatment action",
    "etc..."
  ],
  "safety_precautions": [
    "Safety precaution 1",
    "Safety precaution 2",
    "etc..."
  ]
}}
"""

    try:
        result = llm.invoke(prompt)
        treatment_data = safe_json_parse(result.content)

        if treatment_data:
            return treatment_data

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
