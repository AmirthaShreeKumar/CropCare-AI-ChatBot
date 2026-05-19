# 🛠️ CropCare AI — Comprehensive Tech Stack & Technologies

Below is a complete, production-grade breakdown of the technologies, libraries, and frameworks powering **CropCare AI**, organized by system layers.

---

## 🐍 1. Core Platform & Web Layer
* **[Python 3.11+]**: The fundamental programming platform powering backend orchestration, machine learning inference, RAG vector lookups, and security policies.
* **[Streamlit]**: The core reactive frontend web framework. Provides an elegant, responsive UI dashboard, user forms, chat interfaces, and interactive sliders without the overhead of modern Javascript/React boilerplate.
* **[Streamlit Mic Recorder & Audio Recorder]**: Streamlit extensions enabling users to capture live microphone audio directly in their browser for speech-to-text querying.

---

## 👁️ 2. Computer Vision & Perception Layer
* **[PyTorch]**: The primary deep learning framework. Powers the local Computer Vision inference engine (`src/disease_classifier.py`).
* **[Torchvision]**: Used to instantiate the highly-optimized **MobileNetV2** Convolutional Neural Network (CNN) architecture and load pre-trained weights for localized crop/disease diagnostics.
* **[Pillow (PIL)]**: Handles low-level image processing, resizing, rotation normalization, and secure dimension validation.

---

## 🤖 3. Multimodal & Generative AI Stack
* **[Google Gemini API]**: Used in the **Gatekeeper Agent** to perform visual content filtering and in the **Symptom Agent** (`src/symptom_agent.py`) to translate complex pixel patterns into structured symptom texts using `gemini-2.5-flash`.
* **[Groq LPU Inference Engine]**: Powers all cognitive reasoning agents:
  * **Llama-3.3-70b-versatile**: Drives the Pathfinder, Treatment, and Regional agents due to its ultra-low latency, sub-second text generation.
  * **Whisper-Large-V3**: Used to run near-instantaneous transcription of multilingual voice recordings (English, Hindi, Tamil) into text.
* **[gTTS (Google Text-To-Speech)]**: Generates natural-sounding MP3 speech streams from LLM response texts to provide accessible audio playback for farmers.

---

## 📚 4. Vector Search & Retrieval-Augmented Generation (RAG)
* **[ChromaDB]**: The embedded high-performance vector database used to store and query the grounded facts (`src/disease_rag.py`) and microclimate adaptation protocols (`src/regional_rag.py`).
* **[HuggingFace SentenceTransformers]**: Loads the `all-MiniLM-L6-v2` transformer model locally to compute dense 384-dimensional vector embeddings, preventing API-key dependencies for semantic lookups.
* **[LangChain Core & Community]**: The standard AI framework used to manage structured prompt templates, manage LLM client configurations, and cleanly wrap ChromaDB vector stores.

---

## 🛡️ 5. Security, Validation & Input Safety Shield
* **[Bcrypt]**: Cryptographic password hashing library. Used to salt and hash user passwords (`src/auth.py`) to ensure database security.
* **[Pydantic v2]**: The standard data-validation library. Enforces structured JSON output from LLMs (`src/schemas.py`) and guarantees schema compliance.
* **[Pydantic Settings]**: Eagerly loads, validates, and parses system configurations and API keys from `.env` at startup to prevent mid-runtime failures.
* **[Tenacity]**: An advanced retry library used in `src/api_resilience.py` to handle transient network issues or API rate limits using **Exponential Backoff and Jitter**.
* **[python-magic]**: Reads file headers (magic bytes) to ensure uploaded image/audio files are authentic, preventing extension-spoofing attacks.

---

## 🗄️ 6. Storage & Database Management
* **[PostgreSQL]**: The robust, production-grade relational database management system. Safely persists user accounts, isolated chat sessions, and historical logs.
* **[SQLAlchemy Engine & ORM]**: Python's premium database SQL toolkit. Provides secure parameterized query building in `db.py` to prevent SQL injection vulnerabilities.
* **[psycopg2-binary]**: High-performance PostgreSQL database adapter for Python.

---

## 🐳 7. DevOps, Orchestration & Deployment
* **[Docker]**: The containerization tool used to compile the application runtime, dependencies, and local model weights into an isolated, lightweight layer.
* **[Docker Compose]**: The multi-container orchestration system used to deploy the complete local infrastructure with isolated networks:
  * **`web` container**: Streamlit dashboard, Multi-agent pipeline, and Local CNN classifier.
  * **`db` container**: Isolated PostgreSQL database using the official lightweight `postgres:15-alpine` image with volume persistence.
