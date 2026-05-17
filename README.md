# README.md

# 🌱 CropCare AI — Hybrid Multimodal Agricultural Intelligence Platform

CropCare AI is a production-grade Hybrid AI System that combines Computer Vision, Multi-Agent LLM Reasoning, and Retrieval-Augmented Generation (RAG) to provide intelligent crop disease diagnosis, agronomist-level reasoning, and localized agricultural guidance.

Unlike traditional AI chatbots that rely solely on Large Language Models, CropCare AI separates:

* Visual Perception (Deep Learning CNN)
* Cognitive Reasoning (Multi-Agent LLM Pipeline)
* Knowledge Verification (RAG)
* Regional Intelligence (Environmental Context)

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

The system orchestrates specialized AI agents:

| Agent             | Responsibility                          |
| ----------------- | --------------------------------------- |
| Vision Gatekeeper | Validates uploaded image                |
| Symptom Agent     | Extracts agronomic symptom descriptions |
| Pathfinder Agent  | Performs disease verification via RAG   |
| Treatment Agent   | Generates recovery protocols            |
| Regional Agent    | Adapts recommendations to local climate |

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

## 🔐 Secure Authentication System

CropCare AI includes a secure login and registration workflow.

### Authentication Features

* User login and signup pages
* Password-protected authentication flow
* Shared-secret protected registration system
* Persistent user session handling
* Isolated conversation histories

### Shared Secret Gatekeeping

The signup page requires a hidden application shared secret.

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

## 🛡️ Production-Grade Engineering

The platform implements:

✅ safety interceptors
✅ confidence-aware orchestration
✅ structured schema validation
✅ rate limiting
✅ SQL sanitization
✅ shared-secret protection
✅ automatic media cleanup
✅ persistent PostgreSQL memory
✅ Docker deployment support

---

# 🏛️ Hybrid AI System Architecture

CropCare AI uses a layered Hybrid Perception-Reasoning Architecture.

The system separates:

1. Deep Learning Perception Layer
2. Multimodal Translation Layer
3. Cognitive Reasoning Layer
4. Knowledge Verification Layer
5. Regional Intelligence Layer

📌 For complete architecture details and diagrams:

➡️ Refer to:

```text
/docs/architecture.md
```

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
| Deployment         | Docker + Streamlit Cloud        |
| Observability      | Python Logging                  |

---

# 📂 Project Structure

```text
CropCare-AI/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
├── .env.example
│
├── docs/
│   └── architecture.md
│
├── src/
│   ├── orchestrator.py
│   ├── disease_classifier.py
│   ├── vision_agent.py
│   ├── symptom_agent.py
│   ├── disease_agent.py
│   ├── treatment_agent.py
│   ├── regional_agent.py
│   ├── safety.py
│   ├── cleanup.py
│   ├── summarizer.py
│   ├── factory.py
│   ├── schemas.py
│   └── db.py
│
├── model_weights/
│   └── plant_disease_model.pth
│
├── logs/
│   └── app.log
│
└── development_scripts/
    └── train_cv_model.py
```

---

# ⚙️ Local Setup

## 1. Clone Repository

```bash
git clone <repo-url>
cd CropCare-AI
```

---

## 2. Create Virtual Environment

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

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env`

```env
GOOGLE_API_KEY=your_key
GROQ_API_KEY=your_key
APP_SECRET=your_secret
DATABASE_URL=postgresql://...
```

---

## 5. Run Application

```bash
streamlit run app.py
```

---

# 🐳 Docker Deployment

## Build Docker Image

```bash
docker build -t cropcare-ai .
```

---

## Run Container

```bash
docker run -p 8501:8501 cropcare-ai
```

---

## Open Application

```text
http://localhost:8501
```

---



# 🛡️ Reliability & Safety Features

| Feature                          | Status |
| -------------------------------- | ------ |
| Deterministic Safety Interceptor | ✅      |
| Shared Secret Protection         | ✅      |
| SQL Injection Protection         | ✅      |
| Rate Limiting                    | ✅      |
| Structured Pydantic Validation   | ✅      |
| Automatic Media Cleanup          | ✅      |
| Persistent PostgreSQL Memory     | ✅      |
| Context Summarization            | ✅      |
| Singleton AI Client Management   | ✅      |
| Confidence-Aware Pipeline        | ✅      |

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
* Gemini handles multimodal understanding
* Groq handles reasoning and synthesis
* ChromaDB handles factual grounding
* Orchestrator handles coordination and observability

This creates a far more reliable and scalable AI architecture than relying on a single monolithic model.

---

---

---

