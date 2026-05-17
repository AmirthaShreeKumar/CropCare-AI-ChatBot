import os
import sys

# Force UTF-8 mode inside the script
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Resolve module paths
sys.path.append(os.getcwd())

from src.orchestrator import orchestrate_pipeline

print("[*] Running end-to-end pipeline test on 'temp_1.jpg'...")
try:
    res = orchestrate_pipeline("temp_1.jpg")
    print("[+] Pipeline execution succeeded!")
    print("[+] Result keys:", list(res.keys()))
    print("[+] Disease predicted:", res["disease_info"]["disease_name"])
    print("[+] Prediction source:", res["disease_info"]["prediction_source"])
    print("[+] CV confidence:", res["disease_info"]["cv_confidence"])
    
    # Check if the temporary file was cleaned up successfully
    temp_path = "temp_pipeline_image.jpg"
    if os.path.exists(temp_path):
        print("[-] Error: Temporary image file was NOT cleaned up!")
    else:
        print("[+] Success: Temporary image file was successfully cleaned up and deleted!")
except Exception as e:
    print(f"[-] Pipeline failed with error: {e}")
