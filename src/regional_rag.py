"""
Regional/Climate-Specific Agricultural Advice RAG System
Provides location-based farming recommendations, seasonal calendars, and climate-specific advice
"""

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

# 🔥 Free embedding model
embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 📦 Vector DB for regional knowledge
regional_kb_path = "./regional_knowledge_base"
os.makedirs(regional_kb_path, exist_ok=True)

vectordb = Chroma(
    persist_directory=regional_kb_path,
    embedding_function=embedding,
    collection_name="cropcare_regional"
)

# 🔍 Retriever for regional search
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# 🌍 REGIONAL AGRICULTURAL KNOWLEDGE BASE
# Curated regional farming information for major agricultural regions
REGIONAL_KNOWLEDGE = {
    # INDIA REGIONS
    "Karnataka": """
    Karnataka Agricultural Profile
    Location: Southern India
    Climate: Tropical savanna, semi-arid in north, tropical monsoon in south
    Major Crops: Rice, sugarcane, cotton, coffee, tea, coconut, areca nut
    Soil Types: Red lateritic, black cotton, alluvial
    Annual Rainfall: 600-4000mm (varies by region)

    Seasonal Calendar:
    Kharif (June-October): Rice, maize, cotton, groundnut, soybean
    Rabi (October-February): Wheat, barley, chickpea, mustard, potato
    Summer (March-May): Vegetables, fruits, spices

    Best Crops for Karnataka:
    - Bangalore Rural: Tomato, potato, cabbage, cauliflower
    - Mysore: Sugarcane, rice, coconut, coffee
    - Dharwad: Cotton, groundnut, maize, sunflower
    - Belgaum: Sugarcane, maize, soybean, grapes

    Climate Challenges:
    - Drought in northern districts
    - Heavy monsoon flooding in coastal areas
    - Temperature variations between regions

    Recommended Practices:
    - Use drought-resistant varieties in arid zones
    - Implement rainwater harvesting
    - Practice mixed cropping for risk reduction
    - Adopt precision irrigation techniques

    Pest/Disease Patterns:
    - Cotton: Bollworm, aphids, whitefly
    - Rice: Brown plant hopper, stem borer
    - Vegetables: Fruit borers, aphids, fungal diseases
    """,

    "Tamil Nadu": """
    Tamil Nadu Agricultural Profile
    Location: Southern India
    Climate: Tropical, semi-arid to humid
    Major Crops: Rice, sugarcane, cotton, groundnut, coconut, tea, coffee
    Soil Types: Red, black, alluvial, lateritic
    Annual Rainfall: 400-2000mm

    Seasonal Calendar:
    Kharif (June-October): Rice, cotton, maize, groundnut, sesame
    Rabi (October-February): Rice, wheat, barley, chickpea, potato
    Summer (March-May): Rice, vegetables, fruits, spices

    Best Crops for Tamil Nadu:
    - Cauvery Delta: Rice, sugarcane, banana, coconut
    - Western Ghats: Coffee, tea, cardamom, pepper
    - Dry Areas: Cotton, groundnut, maize, sunflower
    - Coastal: Coconut, cashew, mango, vegetables

    Climate Challenges:
    - Water scarcity in dry regions
    - Cyclonic storms in coastal areas
    - Temperature stress during summer

    Recommended Practices:
    - Efficient water management systems
    - Salt-tolerant varieties for coastal areas
    - Integrated pest management
    - Climate-resilient crop varieties

    Pest/Disease Patterns:
    - Rice: Blast, bacterial blight, stem borer
    - Cotton: Bollworm, sucking pests
    - Coconut: Rhinoceros beetle, root wilt
    """,

    "Maharashtra": """
    Maharashtra Agricultural Profile
    Location: Western India
    Climate: Tropical, semi-arid to humid
    Major Crops: Cotton, sugarcane, soybean, wheat, rice, oranges
    Soil Types: Black cotton, red, alluvial, lateritic
    Annual Rainfall: 400-4000mm

    Seasonal Calendar:
    Kharif (June-October): Cotton, soybean, maize, rice, groundnut
    Rabi (October-February): Wheat, gram, barley, mustard, potato
    Summer (March-May): Vegetables, fruits, spices, cotton

    Best Crops for Maharashtra:
    - Vidarbha: Cotton, soybean, oranges, turmeric
    - Marathwada: Cotton, sorghum, sunflower, grapes
    - Western Maharashtra: Sugarcane, rice, banana, mango
    - Konkan: Rice, coconut, cashew, mango

    Climate Challenges:
    - Drought in Marathwada region
    - Heavy rainfall in Konkan
    - Temperature extremes

    Recommended Practices:
    - Drought-resistant varieties
    - Watershed development
    - Crop diversification
    - Protected cultivation for vegetables

    Pest/Disease Patterns:
    - Cotton: Bollworm, aphids, jassids
    - Soybean: Stem fly, defoliators
    - Sugarcane: Borers, fungal diseases
    """,

    "Punjab": """
    Punjab Agricultural Profile
    Location: Northern India
    Climate: Semi-arid, subtropical
    Major Crops: Wheat, rice, cotton, sugarcane, maize
    Soil Types: Alluvial, sandy loam
    Annual Rainfall: 200-1000mm

    Seasonal Calendar:
    Kharif (April-October): Rice, maize, cotton, sugarcane, bajra
    Rabi (October-April): Wheat, barley, gram, mustard, potato

    Best Crops for Punjab:
    - Central Punjab: Wheat, rice, cotton, sugarcane
    - Border Areas: Cotton, maize, sunflower
    - Canal Areas: Rice, wheat, sugarcane
    - Dry Areas: Mustard, gram, barley

    Climate Challenges:
    - Low rainfall, dependence on irrigation
    - Extreme temperatures (hot summers, cold winters)
    - Water logging in some areas

    Recommended Practices:
    - Efficient irrigation systems
    - Crop rotation (rice-wheat system)
    - Conservation agriculture
    - Laser land leveling

    Pest/Disease Patterns:
    - Wheat: Rusts, aphids, termites
    - Rice: Stem borer, brown plant hopper
    - Cotton: Bollworm, whitefly
    """,

    "Uttar Pradesh": """
    Uttar Pradesh Agricultural Profile
    Location: Northern India
    Climate: Subtropical, semi-arid to humid
    Major Crops: Wheat, rice, sugarcane, potato, mustard, maize
    Soil Types: Alluvial, sandy loam, clay loam
    Annual Rainfall: 400-2000mm

    Seasonal Calendar:
    Kharif (June-October): Rice, maize, cotton, soybean, groundnut
    Rabi (October-February): Wheat, barley, gram, mustard, potato
    Zaid (March-May): Vegetables, melons, fodder

    Best Crops for Uttar Pradesh:
    - Western UP: Wheat, sugarcane, potato, mustard
    - Eastern UP: Rice, wheat, maize, lentil
    - Central UP: Sugarcane, wheat, rice, potato
    - Bundelkhand: Soybean, maize, gram

    Climate Challenges:
    - Drought in western regions
    - Floods in eastern regions
    - Temperature variations

    Recommended Practices:
    - Drought-resistant varieties
    - Flood-tolerant rice varieties
    - Integrated farming systems
    - Precision agriculture

    Pest/Disease Patterns:
    - Wheat: Rusts, aphids, karnal bunt
    - Rice: Blast, bacterial blight
    - Sugarcane: Borers, fungal diseases
    """,

    "West Bengal": """
    West Bengal Agricultural Profile
    Location: Eastern India
    Climate: Tropical monsoon
    Major Crops: Rice, jute, potato, tea, wheat, maize
    Soil Types: Alluvial, lateritic, red
    Annual Rainfall: 1200-3000mm

    Seasonal Calendar:
    Kharif (June-October): Rice, jute, maize, groundnut
    Rabi (October-February): Wheat, barley, potato, mustard
    Summer (March-May): Rice, vegetables, fruits

    Best Crops for West Bengal:
    - Gangetic Plain: Rice, jute, wheat, potato
    - Terai Region: Tea, cardamom, fruits
    - Coastal Areas: Coconut, betel vine, vegetables
    - Hill Areas: Tea, fruits, spices

    Climate Challenges:
    - Heavy monsoon rainfall
    - Cyclonic storms
    - Flooding in delta regions

    Recommended Practices:
    - Flood-tolerant varieties
    - Drainage improvement
    - Salt-tolerant crops for coastal areas
    - Integrated pest management

    Pest/Disease Patterns:
    - Rice: Blast, bacterial blight, stem borer
    - Jute: Stem weevil, semilooper
    - Potato: Late blight, bacterial wilt
    """,

    # OTHER COUNTRIES/REGIONS
    "California": """
    California Agricultural Profile
    Location: Western USA
    Climate: Mediterranean, desert, alpine
    Major Crops: Almonds, grapes, lettuce, strawberries, tomatoes
    Soil Types: Various - alluvial, sandy, clay
    Annual Rainfall: 100-1000mm

    Seasonal Calendar:
    Winter (Dec-Feb): Lettuce, broccoli, carrots
    Spring (Mar-May): Strawberries, tomatoes, peppers
    Summer (Jun-Aug): Corn, melons, grapes
    Fall (Sep-Nov): Pumpkins, apples, grapes

    Best Crops for California:
    - Central Valley: Almonds, walnuts, tomatoes, cotton
    - Coastal: Lettuce, strawberries, broccoli
    - Desert: Dates, table grapes, citrus
    - Sierra Nevada: Apples, pears, cherries

    Climate Challenges:
    - Drought conditions
    - Wildfires
    - Temperature extremes

    Recommended Practices:
    - Drip irrigation systems
    - Drought-tolerant varieties
    - Precision agriculture
    - Water conservation techniques

    Pest/Disease Patterns:
    - Almonds: Navel orangeworm, peach twig borer
    - Grapes: Powdery mildew, Pierce's disease
    - Vegetables: Aphids, thrips, fungal diseases
    """,

    "Texas": """
    Texas Agricultural Profile
    Location: Southern USA
    Climate: Subtropical, semi-arid
    Major Crops: Cotton, corn, wheat, sorghum, pecans
    Soil Types: Blackland prairie, sandy loam, clay
    Annual Rainfall: 300-1500mm

    Seasonal Calendar:
    Winter (Dec-Feb): Wheat, oats, rye
    Spring (Mar-May): Cotton, corn, sorghum
    Summer (Jun-Aug): Cotton, corn, soybeans
    Fall (Sep-Nov): Sorghum, wheat, vegetables

    Best Crops for Texas:
    - High Plains: Cotton, corn, wheat, sorghum
    - Blacklands: Cotton, corn, wheat, pecans
    - Rio Grande Valley: Citrus, vegetables, sugarcane
    - Rolling Plains: Wheat, cotton, peanuts

    Climate Challenges:
    - Drought conditions
    - Extreme temperatures
    - Variable rainfall

    Recommended Practices:
    - Drought-resistant varieties
    - Irrigation management
    - Crop rotation
    - Soil conservation

    Pest/Disease Patterns:
    - Cotton: Bollworm, aphids, spider mites
    - Corn: Corn borer, aphids, fungal diseases
    - Wheat: Rusts, aphids, Hessian fly
    """,

    "Brazil": """
    Brazil Agricultural Profile
    Location: South America
    Climate: Tropical, subtropical
    Major Crops: Soybeans, corn, sugarcane, coffee, cotton
    Soil Types: Oxisols, ultisols, alluvial
    Annual Rainfall: 1000-3000mm

    Seasonal Calendar:
    Summer (Dec-Mar): Soybeans, corn, cotton
    Autumn (Apr-Jun): Wheat, barley, oats
    Winter (Jul-Sep): Rice, beans, vegetables
    Spring (Oct-Nov): Sugarcane, coffee, fruits

    Best Crops for Brazil:
    - Cerrado: Soybeans, corn, cotton, coffee
    - Amazon: Rubber, palm oil, fruits
    - South: Wheat, soybeans, corn, grapes
    - Northeast: Sugarcane, fruits, vegetables

    Climate Challenges:
    - Deforestation impacts
    - Drought in northeast
    - Heavy rainfall in south

    Recommended Practices:
    - No-till farming
    - Crop rotation
    - Integrated pest management
    - Sustainable agriculture

    Pest/Disease Patterns:
    - Soybeans: Stem canker, sudden death syndrome
    - Coffee: Coffee rust, nematodes
    - Sugarcane: Borers, fungal diseases
    """,

    # CLIMATE-SPECIFIC ZONES
    "Tropical": """
    Tropical Agriculture Zone
    Characteristics: High temperature, high humidity, abundant rainfall
    Temperature Range: 20-35°C year-round
    Rainfall: 1500-4000mm annually
    Growing Season: Year-round with peaks

    Best Crops:
    - Rice, maize, cassava, sweet potato
    - Tropical fruits: Mango, papaya, pineapple, banana
    - Vegetables: Tomato, pepper, eggplant, leafy greens
    - Cash crops: Coffee, cocoa, rubber, palm oil

    Challenges:
    - High pest pressure
    - Fungal diseases
    - Soil erosion
    - Nutrient depletion

    Recommended Practices:
    - Intercropping systems
    - Organic matter management
    - Integrated pest management
    - Shade house cultivation

    Seasonal Considerations:
    - Wet season: Rice, maize, vegetables
    - Dry season: Drought-tolerant crops, irrigation
    - Year-round: Fruits, perennial crops
    """,

    "Subtropical": """
    Subtropical Agriculture Zone
    Characteristics: Mild winters, hot summers, moderate rainfall
    Temperature Range: 10-30°C seasonally
    Rainfall: 600-1500mm annually
    Growing Season: 8-10 months

    Best Crops:
    - Citrus, grapes, olives, almonds
    - Vegetables: Tomato, pepper, eggplant, broccoli
    - Field crops: Cotton, soybeans, maize, wheat
    - Fruits: Apple, pear, peach, plum

    Challenges:
    - Frost damage in winter
    - Heat stress in summer
    - Variable rainfall
    - Soil moisture management

    Recommended Practices:
    - Frost protection measures
    - Irrigation scheduling
    - Heat-tolerant varieties
    - Windbreak establishment

    Seasonal Considerations:
    - Spring: Vegetable planting, fruit trees
    - Summer: Field crops, irrigation management
    - Fall: Harvest, soil preparation
    - Winter: Frost protection, dormant crops
    """,

    "Temperate": """
    Temperate Agriculture Zone
    Characteristics: Distinct seasons, moderate temperatures
    Temperature Range: 0-25°C seasonally
    Rainfall: 500-1000mm annually
    Growing Season: 5-7 months

    Best Crops:
    - Cereals: Wheat, barley, oats, rye
    - Vegetables: Potato, cabbage, carrot, pea
    - Fruits: Apple, berry crops, stone fruits
    - Forage: Alfalfa, clover, grasses

    Challenges:
    - Short growing season
    - Frost risk
    - Soil moisture variability
    - Winter dormancy

    Recommended Practices:
    - Early maturing varieties
    - Soil moisture conservation
    - Crop rotation
    - Protected cultivation

    Seasonal Considerations:
    - Spring: Rapid growth, weed control
    - Summer: Irrigation, pest management
    - Fall: Harvest, soil building
    - Winter: Planning, equipment maintenance
    """,

    "Arid": """
    Arid Agriculture Zone
    Characteristics: Low rainfall, high temperatures, desert conditions
    Temperature Range: 15-40°C seasonally
    Rainfall: 100-400mm annually
    Growing Season: 4-6 months

    Best Crops:
    - Drought-tolerant: Sorghum, millet, cowpea
    - Desert crops: Date palm, olive, fig
    - Irrigated crops: Cotton, wheat, maize
    - Vegetables: Onion, garlic, tomato (irrigated)

    Challenges:
    - Water scarcity
    - Soil salinity
    - High evaporation
    - Extreme temperatures

    Recommended Practices:
    - Drip irrigation systems
    - Drought-resistant varieties
    - Soil moisture conservation
    - Salinity management

    Seasonal Considerations:
    - Winter: Cool season crops, irrigation
    - Spring: Heat-tolerant crops
    - Summer: Limited cultivation, shade
    - Monsoon: Rain-fed crops if applicable
    """
}

def initialize_regional_kb():
    """Initialize the regional knowledge base with curated data"""
    print("🌍 Initializing Regional Knowledge Base...")

    # Check if already initialized
    try:
        existing_docs = vectordb.similarity_search("agriculture", k=1)
        if existing_docs:
            print("✅ Regional Knowledge Base already initialized")
            return
    except:
        pass

    # Prepare documents for RAG
    documents = []
    metadatas = []

    for region_name, content in REGIONAL_KNOWLEDGE.items():
        # Clean and prepare content
        clean_content = content.strip()

        # Extract key info for metadata
        lines = clean_content.split('\n')
        climate_type = ""
        major_crops = ""

        for line in lines:
            if line.startswith("Climate:"):
                climate_type = line.replace("Climate:", "").strip()
            elif line.startswith("Major Crops:"):
                major_crops = line.replace("Major Crops:", "").strip()

        documents.append(clean_content)
        metadatas.append({
            "region": region_name,
            "climate": climate_type,
            "crops": major_crops,
            "type": "regional_info"
        })

    # Add to vector database
    if documents:
        vectordb.add_texts(documents, metadatas=metadatas)
        vectordb.persist()
        print(f"✅ Added {len(documents)} regional entries to knowledge base")

def get_regional_info(region_name, k=1):
    """
    Retrieve detailed information about a specific region

    Args:
        region_name: Name of the region (e.g., "Karnataka")
        k: Number of similar results to return

    Returns:
        List of regional information strings
    """
    try:
        results = vectordb.similarity_search(region_name, k=k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error retrieving regional info: {e}")
        return []

def search_region_by_climate(climate_description, k=3):
    """
    Search regions based on climate description

    Args:
        climate_description: Description of climate conditions
        k: Number of results to return

    Returns:
        List of matching regional information
    """
    try:
        query = f"Region with climate: {climate_description}"
        results = vectordb.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error searching regions: {e}")
        return []

def get_crop_recommendations_for_region(region_name, k=1):
    """
    Get crop recommendations for a specific region

    Args:
        region_name: Name of the region

    Returns:
        Crop recommendation information
    """
    try:
        query = f"Crop recommendations for {region_name}"
        results = vectordb.similarity_search(query, k=k)

        for doc in results:
            content = doc.page_content
            if "Best Crops" in content or "Major Crops" in content:
                return content

        return results[0].page_content if results else ""
    except Exception as e:
        print(f"Error getting crop recommendations: {e}")
        return ""

def get_seasonal_calendar(region_name, k=1):
    """
    Get seasonal farming calendar for a region

    Args:
        region_name: Name of the region

    Returns:
        Seasonal calendar information
    """
    try:
        query = f"Seasonal calendar for {region_name}"
        results = vectordb.similarity_search(query, k=k)

        for doc in results:
            content = doc.page_content
            if "Seasonal Calendar" in content:
                return content

        return results[0].page_content if results else ""
    except Exception as e:
        print(f"Error getting seasonal calendar: {e}")
        return ""

def get_climate_challenges(region_name, k=1):
    """
    Get climate challenges and recommended practices for a region

    Args:
        region_name: Name of the region

    Returns:
        Climate challenge information
    """
    try:
        query = f"Climate challenges in {region_name}"
        results = vectordb.similarity_search(query, k=k)

        for doc in results:
            content = doc.page_content
            if "Climate Challenges" in content:
                return content

        return results[0].page_content if results else ""
    except Exception as e:
        print(f"Error getting climate challenges: {e}")
        return ""

def get_regions_by_crop(crop_name, k=5):
    """
    Get regions where a specific crop is commonly grown

    Args:
        crop_name: Name of the crop (e.g., "rice")

    Returns:
        List of regions suitable for the crop
    """
    try:
        # Search for regions mentioning this crop
        query = f"regions where {crop_name} is grown"
        results = vectordb.similarity_search(query, k=k)

        # Filter results that mention the crop
        crop_regions = []
        for doc in results:
            content = doc.page_content.lower()
            if crop_name.lower() in content:
                crop_regions.append(doc.page_content)

        return crop_regions
    except Exception as e:
        print(f"Error getting regions for crop: {e}")
        return []

def get_all_regions():
    """Get list of all regions in the knowledge base"""
    try:
        # Get a sample to find all unique regions
        results = vectordb.similarity_search("agriculture", k=50)
        regions = set()

        for doc in results:
            metadata = doc.metadata
            if metadata.get("region"):
                regions.add(metadata["region"])

        return sorted(list(regions))
    except Exception as e:
        print(f"Error getting region list: {e}")
        return []

def get_climate_specific_advice(climate_type, crop_type="", k=2):
    """
    Get climate-specific agricultural advice

    Args:
        climate_type: Type of climate (tropical, subtropical, etc.)
        crop_type: Optional crop type for specific advice
        k: Number of results

    Returns:
        Climate-specific advice
    """
    try:
        query = f"{climate_type} climate agriculture {crop_type}"
        results = vectordb.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error getting climate advice: {e}")
        return []

# Initialize when module is imported
if __name__ != "__main__":
    initialize_regional_kb()