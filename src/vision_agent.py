# Vision Agent: identifies crop using Gemini
import google.generativeai as genai
from PIL import Image
from src.utils_json_parsing import safe_json_parse
from src.plant_village import PLANTVILLAGE_CLASSES
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "models/gemini-2.5-flash"

model = genai.GenerativeModel(MODEL)

def detect_crop_with_llm(image_path):
    img = Image.open(image_path)
    # Pass the full PlantVillage classes as a hint
    dataset_classes = "\n".join(PLANTVILLAGE_CLASSES)
    
    prompt = f"""
You are an expert plant pathologist and botanist.
Analyze the image of the leaf very carefully. First, observe the leaf shape, margin (edges), vein patterns, and texture.
Second, observe any disease symptoms (like spots, lesions, discoloration).

Here is the exact dataset of crops AND their possible diseases:
{dataset_classes}

Use BOTH the leaf shape AND the specific disease symptoms you see to deduce which crop this is. 
For example, if you see rectangular gray spots, it is likely Corn. If you see yellow halos with target spots, it might be Tomato.

You MUST choose the crop ONLY from the dataset provided. Do NOT guess crops outside this list.

Return ONLY JSON like:
{{
  "reasoning": "Detailed analysis of leaf shape, margin, and veins leading to your conclusion.",
  "crop": "name of the crop",
  "confidence": "high / medium / low",
  "alternatives": ["possible option1", "option2"]
}}
"""
    try:
        result = model.generate_content([prompt, img])
        return safe_json_parse(result.text)
    except Exception as e:
        print(f"Error in vision agent: {e}")
        return {"crop": "Unknown", "confidence": "low", "alternatives": []}
