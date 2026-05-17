import urllib.request
import os
import json

os.makedirs("weights", exist_ok=True)
weights_url = "https://huggingface.co/Daksh159/plant-disease-mobilenetv2/resolve/main/mobilenetv2_plant.pth"
classes_url = "https://huggingface.co/Daksh159/plant-disease-mobilenetv2/resolve/main/class_names.json"

print("[*] Downloading pre-trained weights from Hugging Face...")
try:
    urllib.request.urlretrieve(weights_url, "weights/plant_disease_model.pth")
    print("[+] Pre-trained weights downloaded successfully and saved to 'weights/plant_disease_model.pth'!")
except Exception as e:
    print(f"[-] Failed to download weights: {e}")

print("[*] Downloading class names mapping...")
try:
    urllib.request.urlretrieve(classes_url, "weights/class_names.json")
    print("[+] Class names mapping downloaded successfully!")
    with open("weights/class_names.json", "r") as f:
        classes = json.load(f)
    print(f"[+] Total downloaded classes: {len(classes)}")
    print("[+] Sample classes:", list(classes.values())[:5])
except Exception as e:
    print(f"[-] Failed to download class mapping: {e}")
