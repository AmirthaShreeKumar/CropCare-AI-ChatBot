# Regional Agent: provides location-based agricultural advice using RAG

from src.regional_rag import (
    get_regional_info,
    get_crop_recommendations_for_region,
    get_seasonal_calendar,
    get_climate_challenges,
    get_climate_specific_advice,
    search_region_by_climate
)
import os
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def get_regional_advice(location, crop_name="", context=""):
    """
    Enhanced regional agricultural advice using RAG knowledge base

    Args:
        location: User's location/region (e.g., "Karnataka", "California")
        crop_name: Optional crop they're interested in
        context: Additional context about their farming situation

    Returns:
        Dictionary with regional advice, crop recommendations, seasonal info
    """

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

Return JSON with these exact fields:
{{
  "region": "{location}",
  "best_crops": ["crop1", "crop2", "crop3"],
  "seasonal_advice": "when to plant what",
  "climate_considerations": "weather patterns and challenges",
  "recommended_practices": ["practice1", "practice2"],
  "water_management": "irrigation strategies",
  "pest_disease_alerts": ["alert1", "alert2"]
}}
"""

    try:
        result = llm.invoke(prompt)
        advice_data = safe_json_parse(result.content)

        if advice_data:
            return advice_data

    except Exception as e:
        print(f"Regional advice error: {e}")

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

def detect_location_from_text(text):
    """
    Try to detect location information from user text

    Args:
        text: User input text

    Returns:
        Detected location or None
    """
    # Common location keywords
    location_keywords = [
        # Indian states
        "karnataka", "tamil nadu", "maharashtra", "punjab", "uttar pradesh",
        "west bengal", "gujarat", "rajasthan", "madhya pradesh", "bihar",
        "andhra pradesh", "telangana", "kerala", "odisha", "jharkhand",
        "chhattisgarh", "haryana", "himachal pradesh", "uttarakhand", "goa",
        # Cities
        "bangalore", "mumbai", "delhi", "chennai", "kolkata", "hyderabad",
        "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur",
        "indore", "thane", "bhopal", "visakhapatnam", "pimpri", "patna",
        # International
        "california", "texas", "florida", "brazil", "china", "thailand",
        "vietnam", "indonesia", "philippines", "mexico", "argentina",
        # Climate zones
        "tropical", "subtropical", "temperate", "arid", "semi-arid"
    ]

    text_lower = text.lower()
    for keyword in location_keywords:
        if keyword in text_lower:
            return keyword.title()

    return None

def get_location_based_disease_risks(location, crop_name):
    """
    Get location-specific disease and pest risks

    Args:
        location: User's location
        crop_name: Crop they're growing

    Returns:
        Disease/pest risk information
    """
    try:
        regional_info = get_regional_info(location, k=1)

        if regional_info:
            content = regional_info[0]
            if "Pest/Disease Patterns" in content:
                # Extract pest/disease section
                patterns = content.split("Pest/Disease Patterns:")[1].strip()
                return patterns

        return f"Monitor common {crop_name} pests and diseases in {location} region"

    except Exception as e:
        print(f"Error getting disease risks: {e}")
        return "Consult local agricultural extension for pest/disease information"

def safe_json_parse(json_str):
    """Safely parse JSON string"""
    import json
    try:
        return json.loads(json_str)
    except:
        # Try to extract JSON from text
        import re
        json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        return None