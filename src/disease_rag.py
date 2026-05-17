"""
Disease Knowledge Base RAG System
Provides detailed disease information, treatments, and prevention methods
"""

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

# 🔥 Free embedding model
embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 📦 Vector DB for disease knowledge
disease_kb_path = "./disease_knowledge_base"
os.makedirs(disease_kb_path, exist_ok=True)

vectordb = Chroma(
    persist_directory=disease_kb_path,
    embedding_function=embedding,
    collection_name="cropcare_diseases"
)

# 🔍 Retriever for disease search
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# 📚 DISEASE KNOWLEDGE BASE
# Curated agricultural disease information
DISEASE_KNOWLEDGE = {
    # TOMATO DISEASES
    "Early Blight": """
    Early Blight (Alternaria solani)
    Crops Affected: Tomato, Potato, Pepper
    Symptoms: Dark brown spots with concentric rings on leaves, stems, and fruits. Yellow halos around spots.
    Causes: Fungal pathogen that overwinters in soil and plant debris. Spreads by wind, water, and infected seeds.
    Conditions: Thrives in warm, humid conditions (24-29°C) with frequent rainfall.
    Prevention:
    - Plant resistant varieties
    - Avoid overhead watering
    - Crop rotation (3-4 years)
    - Remove infected plant debris
    - Space plants for air circulation
    Treatments:
    - Organic: Copper fungicide, Neem oil, Baking soda spray (1 tsp per quart water)
    - Chemical: Chlorothalonil, Mancozeb, Azoxystrobin
    - Biological: Bacillus subtilis (Serenade)
    Safety: Wear protective clothing when applying chemicals. Wash hands after handling.
    """,

    "Late Blight": """
    Late Blight (Phytophthora infestans)
    Crops Affected: Tomato, Potato
    Symptoms: Water-soaked lesions on leaves that turn brown/black. White fungal growth on leaf undersides. Rapid plant death.
    Causes: Oomycete pathogen, spreads rapidly in cool, wet conditions. Famous for Irish Potato Famine.
    Conditions: Cool temperatures (10-20°C) with high humidity and leaf wetness.
    Prevention:
    - Plant resistant varieties
    - Avoid overhead irrigation
    - Good drainage
    - Remove volunteer plants
    - Fungicide applications during wet periods
    Treatments:
    - Organic: Copper fungicide, Potassium bicarbonate
    - Chemical: Mefenoxam, Chlorothalonil, Cymoxanil
    - Biological: Trichoderma harzianum
    Safety: Handle copper-based products carefully. Follow label instructions.
    """,

    "Fusarium Wilt": """
    Fusarium Wilt (Fusarium oxysporum)
    Crops Affected: Tomato, Banana, Cotton, Melon
    Symptoms: Yellowing of lower leaves, wilting during heat of day, brown vascular discoloration in stems.
    Causes: Soil-borne fungus that enters through roots. Survives in soil for many years.
    Conditions: Warm soil temperatures (24-32°C), acidic soil pH.
    Prevention:
    - Use disease-free seeds and transplants
    - Soil sterilization (solarization or fumigation)
    - Resistant varieties (VFN varieties)
    - Crop rotation (5-7 years)
    - Avoid planting in infected fields
    Treatments:
    - No cure once infected - remove and destroy plants
    - Soil fumigation with methyl bromide (restricted)
    - Biological control with Fusarium-resistant strains
    Safety: Soil fumigation requires professional application.
    """,

    "Bacterial Spot": """
    Bacterial Spot (Xanthomonas campestris)
    Crops Affected: Tomato, Pepper
    Symptoms: Small, dark, water-soaked spots on leaves and fruits. Spots may have yellow halos.
    Causes: Bacterial pathogen spread by wind-driven rain, contaminated tools, and workers.
    Conditions: Warm, humid weather (24-30°C) with frequent rain.
    Prevention:
    - Use certified disease-free seeds
    - Copper sprays during wet seasons
    - Avoid working with wet plants
    - Sanitize tools between plants
    Treatments:
    - Organic: Copper fungicide sprays
    - Chemical: Streptomycin, Oxytetracycline (restricted in some areas)
    - Biological: Bacteriophages
    Safety: Copper products are safe for organic farming.
    """,

    # POTATO DISEASES
    "Potato Late Blight": """
    Potato Late Blight (Phytophthora infestans)
    Crops Affected: Potato, Tomato
    Symptoms: Dark, water-soaked lesions on leaves. White mold on undersides. Tubers show brown rot.
    Causes: Same pathogen as tomato late blight. Devastating disease affecting potato production worldwide.
    Conditions: Cool, wet weather (15-20°C) with high humidity.
    Prevention:
    - Plant certified seed potatoes
    - Avoid overhead irrigation
    - Fungicide spray programs
    - Destroy infected plants immediately
    Treatments:
    - Organic: Copper fungicide
    - Chemical: Ridomil Gold, Curzate
    - Biological: Compost tea applications
    Safety: Early detection and removal prevents spread.
    """,

    # CORN DISEASES
    "Corn Borer": """
    Corn Borer (Ostrinia nubilalis)
    Crops Affected: Corn, Sorghum
    Symptoms: Holes in leaves, broken stalks, sawdust-like frass, ear damage.
    Causes: Insect pest that bores into corn stalks and ears.
    Conditions: Warm weather (21-32°C), available host plants.
    Prevention:
    - Plant resistant varieties
    - Crop rotation
    - Biological control (Trichogramma wasps)
    - Pheromone traps for monitoring
    Treatments:
    - Organic: Bt (Bacillus thuringiensis) sprays
    - Chemical: Carbaryl, Permethrin
    - Biological: Natural predators
    Safety: Bt is safe for beneficial insects.
    """,

    # GENERAL PLANT DISEASES
    "Powdery Mildew": """
    Powdery Mildew (Various fungi)
    Crops Affected: Many vegetables, fruits, ornamentals
    Symptoms: White, powdery coating on leaves and stems. Leaves may curl and yellow.
    Causes: Fungal pathogens that thrive in humid conditions without leaf wetness.
    Conditions: High humidity, moderate temperatures (20-25°C), poor air circulation.
    Prevention:
    - Improve air circulation
    - Avoid overhead watering
    - Plant resistant varieties
    - Space plants properly
    Treatments:
    - Organic: Baking soda spray, Milk spray, Neem oil
    - Chemical: Sulfur, Triadimefon, Myclobutanil
    - Biological: Ampelomyces quisqualis
    Safety: Sulfur can burn plants in hot weather.
    """,

    "Downy Mildew": """
    Downy Mildew (Various pathogens)
    Crops Affected: Grapes, lettuce, spinach, cucurbits
    Symptoms: Yellow spots on upper leaf surface, grayish mold on undersides.
    Causes: Oomycete pathogens requiring free water for infection.
    Conditions: Cool, humid weather with dew or rain.
    Prevention:
    - Avoid overhead watering
    - Improve air circulation
    - Plant resistant varieties
    - Fungicide applications
    Treatments:
    - Organic: Copper fungicide
    - Chemical: Mancozeb, Chlorothalonil
    - Biological: Compost extracts
    Safety: Copper products are organic-approved.
    """,

    "Root Rot": """
    Root Rot (Various fungi)
    Crops Affected: Most crops
    Symptoms: Wilting, yellowing leaves, stunted growth, brown/black roots.
    Causes: Soil-borne fungi (Pythium, Fusarium, Rhizoctonia) that attack roots.
    Conditions: Poor drainage, overwatering, cool soil temperatures.
    Prevention:
    - Well-drained soil
    - Avoid overwatering
    - Crop rotation
    - Soil sterilization
    Treatments:
    - Improve drainage
    - Reduce watering
    - Fungicide drenches (captan, thiophanate-methyl)
    - Biological control (Trichoderma)
    Safety: Prevention is key - treatment often ineffective.
    """,

    "Leaf Spot": """
    Leaf Spot Diseases (Various fungi/bacteria)
    Crops Affected: Most leafy vegetables and fruits
    Symptoms: Circular or irregular spots on leaves, ranging from brown to black.
    Causes: Fungal or bacterial pathogens spread by wind, water, insects.
    Conditions: Warm, humid weather with leaf wetness.
    Prevention:
    - Avoid overhead watering
    - Space plants for air circulation
    - Remove infected leaves
    - Fungicide sprays
    Treatments:
    - Organic: Copper fungicide, Baking soda spray
    - Chemical: Chlorothalonil, Mancozeb
    - Biological: Bacillus subtilis
    Safety: Copper products safe for organic use.
    """,

    # FRUIT TREE DISEASES
    "Apple Scab": """
    Apple Scab (Venturia inaequalis)
    Crops Affected: Apple, Pear
    Symptoms: Olive-green to black spots on leaves and fruits. Leaves may drop prematurely.
    Causes: Fungal pathogen that overwinters in fallen leaves.
    Conditions: Cool, wet spring weather.
    Prevention:
    - Plant resistant varieties
    - Rake and destroy fallen leaves
    - Fungicide spray program
    - Avoid overhead watering
    Treatments:
    - Organic: Sulfur sprays
    - Chemical: Captan, Myclobutanil
    - Biological: Serenade (Bacillus subtilis)
    Safety: Follow spray schedules carefully.
    """,

    "Citrus Canker": """
    Citrus Canker (Xanthomonas axonopodis)
    Crops Affected: Citrus trees
    Symptoms: Raised, corky lesions on leaves, stems, and fruits.
    Causes: Bacterial pathogen spread by wind-driven rain and contaminated tools.
    Conditions: Warm, humid weather with frequent rain.
    Prevention:
    - Use certified disease-free nursery stock
    - Copper sprays during wet seasons
    - Prune infected branches
    Treatments:
    - Organic: Copper fungicide
    - Chemical: Streptomycin (restricted)
    - Biological: Bacteriophages
    Safety: Quarantine infected trees.
    """,

    # SOYBEAN DISEASES
    "Soybean Rust": """
    Soybean Rust (Phakopsora pachyrhizi)
    Crops Affected: Soybean
    Symptoms: Orange to reddish-brown pustules on leaves. Premature defoliation.
    Causes: Fungal pathogen that can spread rapidly across continents.
    Conditions: Warm, humid weather (20-28°C) with dew.
    Prevention:
    - Plant resistant varieties
    - Fungicide applications
    - Crop rotation
    Treatments:
    - Chemical: Triazole fungicides, Strobilurin fungicides
    - Organic: Limited options - focus on prevention
    Safety: Fungicide resistance management important.
    """,

    # WHEAT DISEASES
    "Wheat Rust": """
    Wheat Rust (Puccinia spp.)
    Crops Affected: Wheat, Barley
    Symptoms: Orange to reddish-brown pustules on leaves and stems.
    Causes: Fungal pathogens that can cause severe yield losses.
    Conditions: Cool, moist weather during growing season.
    Prevention:
    - Plant resistant varieties
    - Fungicide applications
    - Crop rotation
    Treatments:
    - Chemical: Triazole fungicides
    - Organic: Sulfur sprays
    Safety: Monitor for resistant strains.
    """,

    # RICE DISEASES
    "Rice Blast": """
    Rice Blast (Magnaporthe oryzae)
    Crops Affected: Rice
    Symptoms: Diamond-shaped lesions with gray centers and brown borders on leaves.
    Causes: Fungal pathogen that can destroy entire rice fields.
    Conditions: High humidity, temperatures 25-30°C, nitrogen-rich soils.
    Prevention:
    - Balanced fertilization
    - Resistant varieties
    - Proper water management
    Treatments:
    - Chemical: Triazole fungicides
    - Organic: Silicon applications
    Safety: Integrated pest management crucial.
    """
}

def initialize_disease_kb():
    """Initialize the disease knowledge base with curated data"""
    print("🔄 Initializing Disease Knowledge Base...")

    # Check if already initialized
    try:
        existing_docs = vectordb.similarity_search("test", k=1)
        if existing_docs:
            print("✅ Disease Knowledge Base already initialized")
            return
    except:
        pass

    # Prepare documents for RAG
    documents = []
    metadatas = []

    for disease_name, content in DISEASE_KNOWLEDGE.items():
        # Clean and prepare content
        clean_content = content.strip()

        # Extract key info for metadata
        lines = clean_content.split('\n')
        crops_affected = ""
        for line in lines:
            if line.startswith("Crops Affected:"):
                crops_affected = line.replace("Crops Affected:", "").strip()
                break

        documents.append(clean_content)
        metadatas.append({
            "disease": disease_name,
            "crops": crops_affected,
            "type": "disease_info"
        })

    # Add to vector database
    if documents:
        vectordb.add_texts(documents, metadatas=metadatas)
        vectordb.persist()
        print(f"✅ Added {len(documents)} disease entries to knowledge base")

def get_disease_info(disease_name, k=1):
    """
    Retrieve detailed information about a specific disease

    Args:
        disease_name: Name of the disease (e.g., "Early Blight")
        k: Number of similar results to return

    Returns:
        List of disease information strings
    """
    try:
        results = vectordb.similarity_search(disease_name, k=k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error retrieving disease info: {e}")
        return []

def search_disease_by_symptoms(symptoms_description, crop_name=None, k=3):
    """
    Search for diseases based on symptom description and optional crop name filter

    Args:
        symptoms_description: Description of symptoms
        crop_name: Optional name of the crop to target the search
        k: Number of results to return

    Returns:
        List of matching disease information
    """
    try:
        if crop_name:
            query = f"{crop_name} disease with symptoms: {symptoms_description}"
        else:
            query = f"Disease with symptoms: {symptoms_description}"
        results = vectordb.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error searching diseases: {e}")
        return []

def get_treatment_for_disease(disease_name, k=2):
    """
    Get treatment information for a specific disease

    Args:
        disease_name: Name of the disease
        k: Number of treatment results

    Returns:
        List of treatment information
    """
    try:
        query = f"Treatment and prevention for {disease_name}"
        results = vectordb.similarity_search(query, k=k)
        treatments = []

        for doc in results:
            content = doc.page_content
            # Extract treatment section
            if "Treatments:" in content:
                treatments.append(content)

        return treatments if treatments else [results[0].page_content if results else ""]
    except Exception as e:
        print(f"Error getting treatment: {e}")
        return []

def get_prevention_methods(disease_name, k=1):
    """
    Get prevention methods for a disease

    Args:
        disease_name: Name of the disease

    Returns:
        Prevention information
    """
    try:
        query = f"Prevention methods for {disease_name}"
        results = vectordb.similarity_search(query, k=k)

        for doc in results:
            content = doc.page_content
            if "Prevention:" in content:
                return content

        return results[0].page_content if results else ""
    except Exception as e:
        print(f"Error getting prevention: {e}")
        return ""

def get_diseases_by_crop(crop_name, k=5):
    """
    Get diseases that affect a specific crop

    Args:
        crop_name: Name of the crop (e.g., "tomato")

    Returns:
        List of diseases affecting the crop
    """
    try:
        # Search for diseases mentioning this crop
        query = f"diseases affecting {crop_name}"
        results = vectordb.similarity_search(query, k=k)

        # Filter results that mention the crop
        crop_diseases = []
        for doc in results:
            content = doc.page_content.lower()
            if crop_name.lower() in content:
                crop_diseases.append(doc.page_content)

        return crop_diseases
    except Exception as e:
        print(f"Error getting diseases for crop: {e}")
        return []

def get_all_diseases():
    """Get list of all diseases in the knowledge base"""
    try:
        # Get a sample to find all unique diseases
        results = vectordb.similarity_search("disease", k=50)
        diseases = set()

        for doc in results:
            metadata = doc.metadata
            if metadata.get("disease"):
                diseases.add(metadata["disease"])

        return sorted(list(diseases))
    except Exception as e:
        print(f"Error getting disease list: {e}")
        return []

# Initialize when module is imported
if __name__ != "__main__":
    initialize_disease_kb()