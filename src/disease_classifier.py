# Local Computer Vision Disease Classifier Model using PyTorch

import os
from src.logger import logger
from src.plant_village import PLANTVILLAGE_CLASSES

# Try to import torch, torchvision and PIL
try:
    import torch
    import torch.nn as nn
    from torchvision import models, transforms
    from PIL import Image
    TORCH_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PyTorch or torchvision is not available in the current environment: {e}")
    TORCH_AVAILABLE = False

class DiseaseClassifier:
    """
    Singleton Class to load the MobileNetV2 PyTorch image classification model.
    Performs preprocessing, inference, and outputs crop name, disease name, and confidence score.
    Gracefully returns None if torch is not available, weights are missing, or inference fails,
    triggering the zero-shot Gemini Vision fallback pipeline.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DiseaseClassifier, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, weights_path="weights/plant_disease_model.pth"):
        if self._initialized:
            return
        
        self.weights_path = weights_path
        self.model = None
        self.transform = None
        self.classes = PLANTVILLAGE_CLASSES
        
        if TORCH_AVAILABLE:
            try:
                # Check if model weights file exists; if not, we do not initialize the model 
                # so that the system gracefully triggers the Gemini Vision zero-shot fallback
                if not os.path.exists(self.weights_path):
                    logger.warning(f"Local weights not found at '{self.weights_path}'. Fallback to Gemini Vision is active.")
                    self.model = None
                else:
                    logger.info("Initializing MobileNetV2 local deep learning model structure...")
                    # Initialize MobileNetV2 architecture
                    self.model = models.mobilenet_v2(pretrained=False)
                    
                    # Reconstruct final linear head to map to exactly 38 PlantVillage classes
                    num_ftrs = self.model.classifier[1].in_features
                    self.model.classifier[1] = nn.Sequential(
                        nn.Dropout(0.2),
                        nn.Linear(num_ftrs, len(self.classes))
                    )
                    
                    logger.info(f"Loading local CV weights from {self.weights_path}...")
                    self.model.load_state_dict(torch.load(self.weights_path, map_location=torch.device('cpu')))
                    self.model.eval()
                    logger.info("Local CV model successfully loaded in evaluation mode.")

                    # Define standard ImageNet preprocessing transforms
                    self.transform = transforms.Compose([
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                    ])
            except Exception as e:
                logger.error(f"Error initializing local deep learning classifier: {e}")
                self.model = None
        else:
            logger.warning("PyTorch/torchvision are unavailable. Graceful fallback to Gemini Vision is active.")
            self.model = None

        self._initialized = True

    def predict(self, image_path):
        """
        Performs inference using the local PyTorch model.
        
        Args:
            image_path (str): Absolute or relative path to the crop leaf image.
            
        Returns:
            dict: { "crop": str, "disease_name": str, "confidence": float, "source": str }
            None: If PyTorch is unavailable, weights are missing, or inference fails.
        """
        if not TORCH_AVAILABLE or self.model is None:
            logger.info("Local CV model is not active/weights are missing. Engaging Gemini Vision fallback pipeline.")
            return None

        if not os.path.exists(image_path):
            logger.error(f"Image not found at path: {image_path}")
            return None

        try:
            # Load and preprocess image
            with Image.open(image_path) as img:
                img_rgb = img.convert('RGB')
                tensor_img = self.transform(img_rgb).unsqueeze(0)  # Add batch dimension

            # Run feedforward inference
            with torch.no_grad():
                outputs = self.model(tensor_img)
                probabilities = torch.softmax(outputs, dim=1)[0]
                
            # Get max prediction index and probability
            confidence, predicted_idx = torch.max(probabilities, dim=0)
            predicted_class = self.classes[predicted_idx.item()]
            
            # Parse crop and disease names
            if "___" in predicted_class:
                crop, disease = predicted_class.split("___")
            else:
                crop, disease = predicted_class, "healthy"

            crop_name = crop.replace("_", " ").strip()
            disease_name = disease.replace("_", " ").strip()
            
            # Strip trailing punctuation/underscores
            if disease_name.endswith("_"):
                disease_name = disease_name[:-1]
                
            # Human-readable healthy name formatting
            if disease_name.lower() == "healthy":
                disease_name = "Healthy"

            return {
                "crop": crop_name,
                "disease_name": disease_name,
                "confidence": round(float(confidence.item()), 4),
                "source": "Local CV Model (MobileNetV2)"
            }
        except Exception as e:
            logger.error(f"Local CV inference failed with error: {e}. Graceful fallback engaged.")
            return None
