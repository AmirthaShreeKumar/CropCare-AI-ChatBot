# Symptom Agent: describes crop symptoms using Gemini
import google.generativeai as genai
from PIL import Image
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "models/gemini-2.5-flash"

model = genai.GenerativeModel(MODEL)

def describe_symptoms(crop_name, image_path):
    prompt = f"""
You are an expert plant pathologist.
Analyze the {crop_name} leaf in the image very carefully.
Describe the symptoms in extreme detail. Focus on:
1. Lesion shape, size, and color (e.g., tan, gray, brown, yellow halos).
2. Location of symptoms (e.g., interveinal, leaf margins, concentric rings).
3. Any signs of fungal growth or blight.

Return ONLY a detailed text description of the symptoms. Do NOT mention the disease name, just describe what you see visually.
"""
    try:
        with Image.open(image_path) as img:
            result = model.generate_content([prompt, img])
            return result.text.strip()
    except Exception as e:
        print(f"Error in symptom agent: {e}")
        return "Could not determine symptoms from the image."
