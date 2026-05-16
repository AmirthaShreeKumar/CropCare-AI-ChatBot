from pydantic import BaseModel, Field
from typing import List, Optional

class CropDetection(BaseModel):
    reasoning: str = Field(description="Detailed analysis of leaf shape, margin, and veins.")
    crop: str = Field(description="Name of the detected crop.")
    confidence: str = Field(description="Confidence level: high, medium, or low.")
    alternatives: List[str] = Field(default_factory=list, description="Other possible crops.")

class DiseaseDiagnosis(BaseModel):
    disease_name: str = Field(description="Exact disease name from the supported list.")
    confidence: str = Field(description="Confidence level: high, medium, or low.")
    reasoning: str = Field(description="Brief explanation for the diagnosis.")
    detailed_info: Optional[str] = Field(default="", description="Detailed disease description from knowledge base.")
    treatments: Optional[str] = Field(default="", description="Treatment overview from knowledge base.")
    prevention: Optional[str] = Field(default="", description="Prevention strategies from knowledge base.")

class TreatmentPlan(BaseModel):
    treatment_steps: List[str] = Field(description="Step-by-step treatment actions.")
    safety_precautions: List[str] = Field(description="Safety measures for the farmer.")

class RegionalAdvice(BaseModel):
    region: str = Field(description="The location for which advice is provided.")
    best_crops: List[str] = Field(description="Crops recommended for this region.")
    seasonal_advice: str = Field(description="Advice on planting times and seasonal care.")
    climate_considerations: str = Field(description="Weather patterns and local climate challenges.")
    recommended_practices: List[str] = Field(description="General local farming best practices.")
    water_management: str = Field(description="Irrigation and water conservation advice.")
    pest_disease_alerts: List[str] = Field(description="Current pest or disease risks in the area.")
