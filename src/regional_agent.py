import os
import streamlit as st
from src.regional_rag import (
    get_regional_info,
    get_crop_recommendations_for_region,
    get_seasonal_calendar,
    get_climate_challenges,
    get_climate_specific_advice,
    search_region_by_climate
)
from src.schemas import RegionalAdvice
from src.factory import AIClientFactory
from src.logger import logger

llm = AIClientFactory.get_llm()

@st.cache_data(show_spinner=False)
def get_regional_advice(location, crop_name="", context=""):
    """
    Enhanced regional agricultural advice using RAG knowledge base (cached)
    """
    structured_llm = llm.with_structured_output(RegionalAdvice)
    
    logger.info(f"Generating regional advice for {location} (Crop: {crop_name})")
    
    # Get regional information from RAG
    regional_info = get_regional_info(location, k=1)
    crop_recs = get_crop_recommendations_for_region(location, k=1)
    seasonal_info = get_seasonal_calendar(location, k=1)
    climate_challenges = get_climate_challenges(location, k=1)

    # Build enhanced prompt with RAG context
    rag_context = ""
    if regional_info:
        rag_context += f"\n\nREGIONAL INFORMATION:\n{regional_info[0]}"
    if crop_recs:
        rag_context += f"\n\nCROP RECOMMENDATIONS:\n{crop_recs}"
    if seasonal_info:
        rag_context += f"\n\nSEASONAL CALENDAR:\n{seasonal_info}"
    if climate_challenges:
        rag_context += f"\n\nCLIMATE CHALLENGES:\n{climate_challenges}"

    # If no specific region found, try climate-based search
    if not regional_info:
        climate_advice = get_climate_specific_advice(location, crop_name, k=1)
        if climate_advice:
            rag_context += f"\n\nCLIMATE-BASED ADVICE:\n{climate_advice[0]}"

    prompt = f"""
    You are a regional agricultural expert for {location}.
    Provide comprehensive farming advice for this location.
    
    {rag_context}
    
    Additional Context: {context}
    Crop of Interest: {crop_name}
    
    Provide advice on:
    - Best crops for this region and season
    - Optimal planting times
    - Climate-specific challenges and solutions
    - Local farming practices and recommendations
    - Water management strategies
    - Pest/disease patterns to watch for
    """

    try:
        advice_data = structured_llm.invoke(prompt)
        if advice_data:
            logger.info(f"Successfully generated regional advice for {location}")
            return advice_data.dict()
    except Exception as e:
        logger.error(f"Regional advice error for {location}: {e}")

    # Fallback advice
    return {
        "region": location,
        "best_crops": [crop_name] if crop_name else ["Consult local extension service"],
        "seasonal_advice": f"Check local agricultural calendar for {location}",
        "climate_considerations": f"Consider local climate patterns in {location}",
        "recommended_practices": [
            "Consult local agricultural extension services",
            "Visit nearby agricultural universities",
            "Join local farmer cooperatives"
        ],
        "water_management": "Use appropriate irrigation for local conditions",
        "pest_disease_alerts": ["Monitor local pest and disease patterns"]
    }

@st.cache_data(show_spinner=False)
def detect_location_from_text(text):
    """
    Try to detect location information from user text (cached)
    """
    location_keywords = [
        "karnataka", "tamil nadu", "maharashtra", "punjab", "uttar pradesh",
        "west bengal", "gujarat", "rajasthan", "madhya pradesh", "bihar",
        "andhra pradesh", "telangana", "kerala", "odisha", "jharkhand",
        "chhattisgarh", "haryana", "himachal pradesh", "uttarakhand", "goa",
        "bangalore", "mumbai", "delhi", "chennai", "kolkata", "hyderabad",
        "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur",
        "indore", "thane", "bhopal", "visakhapatnam", "pimpri", "patna",
        "california", "texas", "florida", "brazil", "china", "thailand",
        "vietnam", "indonesia", "philippines", "mexico", "argentina",
        "tropical", "subtropical", "temperate", "arid", "semi-arid"
    ]

    text_lower = text.lower()
    for keyword in location_keywords:
        if keyword in text_lower:
            logger.info(f"Detected location '{keyword.title()}' in user text.")
            return keyword.title()

    return None

@st.cache_data(show_spinner=False)
def get_location_based_disease_risks(location, crop_name):
    """
    Get location-specific disease and pest risks (cached)
    """
    try:
        regional_info = get_regional_info(location, k=1)
        if regional_info:
            content = regional_info[0]
            if "Pest/Disease Patterns" in content:
                patterns = content.split("Pest/Disease Patterns:")[1].strip()
                return patterns
        return f"Monitor common {crop_name} pests and diseases in {location} region"
    except Exception as e:
        logger.error(f"Error getting disease risks for {location}: {e}")
        return "Consult local agricultural extension for pest/disease information"