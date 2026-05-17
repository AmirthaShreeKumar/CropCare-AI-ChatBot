# 🛠️ Tech Stack & Technologies Used

Below is a comprehensive breakdown of the core technologies powering **CropCare AI**, including exactly where they are used and why they were chosen for this production-grade architecture.

### 🐍 Core Language & Frameworks
* **[Python 3.11+]**: The backbone programming language used for the entire application, bridging machine learning, database management, and backend logic.
* **[Streamlit]**: The frontend framework used to build the beautiful, interactive dashboard and chat interface without needing React or JavaScript.

### 👁️ Deep Learning & Perception
* **[PyTorch]**: The deep learning framework that powers the local Computer Vision inference engine (`src/disease_classifier.py`).
* **[MobileNetV2]**: The highly efficient Convolutional Neural Network (CNN) architecture used for instantly classifying 38 plant diseases on edge hardware without API latency.

### 🤖 Multimodal & Cognitive LLMs
* **[Google Gemini Vision]**: The multimodal AI used in the Gatekeeper and Symptom Agents (`src/vision_agent.py`) because of its unparalleled ability to translate raw images into descriptive text.
* **[Groq (Llama 3)]**: The ultra-fast LPU inference engine used for all cognitive reasoning agents (Disease, Treatment, Regional) because it provides instantaneous, sub-second text generation.
* **[Whisper-Large-V3]**: The speech-to-text model hosted via Groq that instantly transcribes the user's multilingual voice recordings into text.

### 📚 Vector Search & Retrieval-Augmented Generation (RAG)
* **[ChromaDB]**: The embedded vector database used in `disease_rag.py` and `regional_rag.py` to store and retrieve specific agricultural facts, preventing LLM hallucinations.
* **[HuggingFace Embeddings (all-MiniLM-L6-v2)]**: The lightweight, free embedding model used to quickly convert text documents into vector numbers for ChromaDB.

### 💾 Persistent Storage & Security
* **[PostgreSQL]**: The robust relational database used to permanently and securely store user accounts and chat histories.
* **[SQLAlchemy]**: The Object-Relational Mapper (ORM) used in `db.py` to securely manage database interactions and prevent SQL injection attacks.
* **[Pydantic]**: The data validation framework used in `src/schemas.py` to force the LLMs to strictly output clean, structured JSON formats.
* **[Bcrypt]**: The cryptographic hashing library used to safely encrypt user passwords before storing them in the database.

### 🐳 Deployment & DevOps
* **[Docker]**: The containerization platform used (`Dockerfile`) to package the entire application and its dependencies into a single isolated unit for cloud deployment.
