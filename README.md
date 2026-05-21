# 🌱 CropCare AI — Hybrid Multimodal Agricultural Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Docker](https://img.shields.io/badge/Deployment-Docker-blue)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-316192)
![CI](https://github.com/AmirthaShreeKumar/CropCare-AI-ChatBot/actions/workflows/ci.yml/badge.svg)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)

CropCare AI is a production-grade Hybrid AI System that combines Computer Vision, Multi-Agent LLM Reasoning, and Retrieval-Augmented Generation (RAG) to provide intelligent crop disease diagnosis, agronomist-level reasoning, and localized agricultural guidance.

Unlike traditional AI chatbots that rely solely on Large Language Models, CropCare AI utilizes a highly decoupled, multi-layer architecture that separates:

* Visual Perception (Deep Learning CNN)
* Multimodal Translation (Gemini Vision to Text translation)
* Cognitive Reasoning (Multi-Agent LLM Pipeline)
* Knowledge Verification (RAG)
* Regional Intelligence (Environmental Context)
* Persistence & History Isolation (PostgreSQL Database)

This architecture enables the system to perform highly specialized plant disease classification while still delivering explainable reasoning, treatment generation, and region-specific recommendations.

---

# 🚀 Core Highlights

## 🧠 Hybrid AI Architecture

CropCare AI combines:

* Local Computer Vision (MobileNetV2)
* Gemini Vision Analysis
* Groq Llama 3 Cognitive Reasoning
* ChromaDB Retrieval-Augmented Generation
* Multi-Agent Sequential Orchestration

instead of forcing a single LLM to perform all tasks.

---

## 👁️ Deep Learning Disease Classification

A dedicated MobileNetV2-based CNN performs:

* Crop classification
* Plant disease prediction
* Confidence scoring
* Fast local inference

The model is optimized for PlantVillage-style agricultural datasets.

---

## 🤖 Multi-Agent Cognitive Pipeline

The system orchestrates specialized AI agents through a highly decoupled pipeline:

| Agent             | Responsibility                          |
| ----------------- | --------------------------------------- |
| Vision Gatekeeper | Validates uploaded image                |
| Symptom Agent     | Extracts agronomic symptom descriptions |
| Pathfinder Agent  | Performs disease verification via RAG   |
| Treatment Agent   | Generates recovery protocols            |
| Regional Agent    | Adapts recommendations to local climate |
| Translation Layer | Provides localized language output      |

---

## 📚 Retrieval-Augmented Verification

The Disease Pathfinder Agent uses ChromaDB to:

* validate CNN predictions
* reduce hallucinations
* retrieve disease knowledge
* ground treatments in verified context

---

## 🌐 Multilingual Voice Intelligence

CropCare AI supports multilingual agricultural interaction through integrated voice and language-aware conversational workflows.

Supported languages:

* English
* Tamil
* Hindi

Users can configure their preferred language directly from the Streamlit interface.

The system supports:

✅ multilingual responses
✅ speech-to-text voice interaction
✅ text-to-speech response generation
✅ persistent language preference handling

Voice recordings are processed and translated into structured agricultural queries before entering the AI pipeline.

---

## 📝 Example Use Cases & Sample Inputs

To test the system, you can use the following sample inputs. 

> [!WARNING]  
> **Agricultural Domain Only**: CropCare AI is equipped with a strict safety interceptor. It will instantly block and refuse to answer any queries or analyze any images that are not related to plants, farming, or agriculture.

### 📷 1. Image Uploads
You can test the deep learning Computer Vision and RAG pipeline by uploading test images. The local CNN is specifically trained on the **[PlantVillage Dataset](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset)**, meaning it excels at identifying exactly 38 specific crop-disease combinations.
We have provided sample images for you in the `Sample_image_inputs/` folder in this repository. 
* *Example*: Upload `temp_grape_leaf_blight.jpg` to see the multi-agent system diagnose Black Rot and prescribe regional treatments.
* *Example*: Upload `temp_cow.jpg` to see the Gemini Gatekeeper reject the image because it is an animal, not a plant!

### 💬 2. Text Queries
You can ask complex agricultural questions directly:
* *"What is the best organic treatment for powdery mildew on my tomato plants?"*
* *"When is the best time to plant wheat in Punjab?"*

### 🎙️ 3. Voice Inputs
Using the microphone button, you can speak your questions in English, Tamil, or Hindi:
* *"Mera khet mein keede lag gaye hain, koi dawa batao"* (Hindi for: My field is infested with pests, tell me some medicine)
* *"En thakkali sediyil manjal nira pulligal ullana, enna seivathu?"* (Tamil for: My tomato plant has yellow spots, what should I do?)

---

## 🔐 Secure Authentication System

CropCare AI includes a secure, production-ready login and registration workflow backed by a PostgreSQL database.

### Authentication Features

* User login and signup pages
* Bcrypt Password-protected authentication flow
* Shared-secret protected registration system
* Persistent user session handling (Isolated user chat states)
* Isolated conversation histories per session

### Shared Secret Gatekeeping

The signup page requires a hidden application shared secret (`APP_SECRET`).

This prevents:

* unauthorized public registrations
* malicious API abuse
* automated spam account creation
* uncontrolled AI credit consumption

Only users with the correct shared secret can create accounts.

---

## ⚡ Full Observability & Metrics

CropCare AI includes a complete observability layer.

The system tracks:

* CNN inference latency
* symptom extraction latency
* RAG reasoning latency
* treatment generation latency
* regional analysis latency
* total pipeline execution time

Metrics are rendered inside a premium glassmorphic Streamlit performance dashboard.

---

# 🏛️ Hybrid AI System Architecture

CropCare AI uses a layered Hybrid Perception-Reasoning Architecture.

The system separates:

1. Security & Authentication Shield
2. Deep Learning Perception Layer
3. Multimodal Translation Layer
4. Cognitive Reasoning Layer
5. Knowledge Verification Layer
6. Regional Intelligence Layer
7. Persistent Relational Storage

📌 For complete architecture details and diagrams:

➡️ Refer to: [docs/architecture.md](docs/architecture.md)

---

# ⚡ Performance Metrics

## Example Runtime Metrics

| Stage                 | Typical Latency |
| --------------------- | --------------- |
| CNN Inference         | 0.3 – 0.8 sec   |
| Symptom Extraction    | 1 – 2 sec       |
| RAG Verification      | 1 – 2 sec       |
| Treatment Generation  | 0.5 – 1 sec     |
| Regional Intelligence | 0.5 – 1 sec     |
| Total Pipeline        | ~4 – 7 sec      |

---

## Runtime Metrics Example

```json
{
  "performance_metrics": {
    "cv_inference_sec": 0.42,
    "symptom_analysis_sec": 1.18,
    "disease_reasoning_sec": 1.91,
    "treatment_generation_sec": 0.88,
    "regional_analysis_sec": 0.63,
    "total_pipeline_sec": 5.02
  }
}
```

---

# 📊 Technology Stack

| Layer              | Technology                      |
| ------------------ | ------------------------------- |
| Frontend           | Streamlit                       |
| Voice Interface    | Speech-to-Text + Text-to-Speech |
| Multilingual Layer | English + Tamil + Hindi         |
| Computer Vision    | PyTorch + MobileNetV2           |
| Vision AI          | Gemini Vision                   |
| LLM Reasoning      | Groq Llama 3                    |
| Vector Database    | ChromaDB                        |
| Embeddings         | Sentence Transformers           |
| Database           | PostgreSQL                      |
| ORM                | SQLAlchemy                      |
| Validation         | Pydantic                        |
| Deployment         | Docker + Docker Compose         |
| Observability      | Python Logging                  |

---

# 📂 Project Structure

```text
CropCare-AI/
│
├── app.py                      # Main Streamlit Frontend
├── db.py                       # PostgreSQL client & CRUD operations for sessions/chats/messages.
├── requirements.txt            # Python dependencies list
├── Dockerfile                  # Application build container recipe
├── docker-compose.yml          # Container orchestration setup for spinning up both Web and Database services together.
├── .dockerignore               # Docker ignore rules
├── README.md                   # Project documentation
├── .env.example                # Example environment variables setup
│
├── docs/
│   └── architecture.md         # Detailed architectural guide
│
├── src/
│   ├── config.py               # Pydantic Settings & Startup Validator
│   ├── auth.py                 # Bcrypt Session Auth UI logic
│   ├── uploads.py              # File signature & size safety validation (Magic Bytes checks).
│   ├── api_resilience.py       # Tenacity backoff & API retry logic
│   ├── health.py               # Pre-flight startup health checks
│   ├── logger.py               # Rotating File Logger configuration
│   ├── orchestrator.py         # Multi-Agent Routing & Pipeline Hub
│   ├── disease_classifier.py   # PyTorch CNN local crop/disease predictor
│   ├── vision_agent.py         # Multimodal visual analysis integration
│   ├── symptom_agent.py        # Gemini-2.5 symptom text mapping
│   ├── disease_agent.py        # Pathfinder Agent reasoning code
│   ├── treatment_agent.py      # Prescribes Chemical & Organic Plans
│   ├── regional_agent.py       # Regional Coordinator Agent
│   ├── safety.py               # Prompt safety filtering interceptor
│   ├── cleanup.py              # Temporary folder cleaning tools
│   ├── summarizer.py           # Multi-turn history summarization
│   ├── schemas.py              # Pydantic data schemas
│   └── db.py
│
├── model_weights/
│   └── plant_disease_model.pth # Pre-trained CNN weights
│
├── Sample_image_inputs/        # Sample images for testing the platform
│
├── logs/
│   └── app.log                 # Output logs
│
└── development_scripts/
    └── train_cv_model.py       # Model training script
```

---

# 🐳 Production Docker Deployment (Recommended)

CropCare AI is built to run as a multi-container Docker Compose application, ensuring that the frontend Streamlit application and the PostgreSQL database are properly networked, isolated, and scalable.

## 1. Clone Repository & Setup Env

```bash
git clone <repo-url>
cd CropCare-AI
cp .env.example .env
```
*Make sure to fill in `GROQ_API_KEY`, `GOOGLE_API_KEY`, and `APP_SECRET` in the `.env` file.*

## 2. Build and Start Services

Run the application in detached mode using Docker Compose:

```bash
docker compose up -d --build
```

This will:
- Spin up the `db` container running PostgreSQL.
- Build and spin up the `web` container running Streamlit.
- Automatically link them together over a dedicated bridge network.

## 3. Open Application

```text
http://localhost:8501
```

## 4. Viewing Logs & Diagnostics

To see real-time container logs for debugging:

```bash
# View Web UI logs
docker compose logs web -f

# View Database logs
docker compose logs db -f
```

---

# ⚙️ Manual Local Setup (Alternative)

If you prefer to run the app directly on your host machine without Docker, follow these steps:

## 1. Setup Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Database & Environment Configuration

Make sure you have a local PostgreSQL instance running. Create a `.env` file and point `DATABASE_URL` to your local DB:

```env
GOOGLE_API_KEY=your_key
GROQ_API_KEY=your_key
APP_SECRET=your_secret
DATABASE_URL=postgresql://username:password@localhost:5432/cropcare
```

## 4. Run Application

```bash
streamlit run app.py
```

---

# 🛡️ Reliability & Safety Features

| Feature                          | Status |
| -------------------------------- | ------ |
| Deterministic Safety Interceptor | ✅      |
| Shared Secret Protection         | ✅      |
| Bcrypt Password Hashing          | ✅      |
| SQL Injection Protection         | ✅      |
| Rate Limiting & API Backoff      | ✅      |
| Magic Byte File Validation       | ✅      |
| Structured Pydantic Validation   | ✅      |
| Automatic Media Cleanup          | ✅      |
| Persistent PostgreSQL Memory     | ✅      |
| Context Summarization            | ✅      |
| Singleton AI Client Management   | ✅      |
| Confidence-Aware Pipeline        | ✅      |

---

# ✅ Testing & CI/CD

CropCare AI includes lightweight automated testing and continuous integration workflows.

### Current Testing Coverage

- Authentication validation tests
- Database CRUD operation tests
- Prompt injection detection tests
- Agent routing tests
- Smoke import verification

### CI/CD Pipeline

GitHub Actions automatically:

- installs dependencies
- validates imports
- runs pytest suite
- checks project stability on every push and pull request

This helps ensure reproducibility and prevents dependency or integration regressions.
---

# 🔍 Logging & Observability

All major system events are logged centrally using the production logging system.

Log File Location:

```text
logs/app.log
```

Logged events include:

* pipeline execution
* model inference
* fallback activations
* RAG retrievals
* errors and exceptions
* performance timings
* security triggers

---

# 🎯 Design Philosophy

CropCare AI is designed around the idea that:

> Different AI systems should specialize in different forms of intelligence.

Therefore:

* CNNs handle visual classification
* Gemini handles multimodal understanding (Image-to-Text Symptoms)
* Groq handles reasoning and synthesis
* ChromaDB handles factual grounding
* Orchestrator handles coordination and observability
* PostgreSQL handles state and history

This creates a far more reliable, modular, and scalable AI architecture than relying on a single monolithic model.

---
