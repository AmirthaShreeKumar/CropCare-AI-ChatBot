# 🌱 CropCare AI: Multi-Agent Agricultural Assistant

**A high-performance multi-agent AI system powered by Gemini and Groq that provides real-time plant disease diagnosis, treatment recommendations, and localized agricultural advice via image, voice, and text.**

---

## 🚀 Key Features

*   **🔍 Sequential Multi-Agent Pipeline**: Specialized agents for Vision, Symptoms, Diagnosis, Treatment, and Regional Advice.
*   **🤖 Hybrid AI Intelligence**: Leverages **Google Gemini 2.5 Flash** for superior visual reasoning and **Groq Llama 3.1 8B** for lightning-fast text generation.
*   **📚 Retrieval-Augmented Generation (RAG)**: Connects to a specialized knowledge base (ChromaDB) to ensure diagnostic accuracy based on the PlantVillage dataset.
*   **🎙️ Multilingual Voice Interface**: Supports **English**, **Hindi (हिंदी)**, and **Tamil (தமிழ்)** with real-time transcription (Whisper v3) and text-to-speech (gTTS).
*   **🌍 Regional Intelligence**: Automatically detects user location to provide localized crop advice and climate-specific alerts.
*   **💬 Professional Chat Management**: Persistent chat history with PostgreSQL, allowing users to rename, save, and manage multiple diagnostic sessions.

---

## 🧠 The Agent Team

| Agent | Responsibility | Model |
| :--- | :--- | :--- |
| **Vision Agent** | Identifies the crop species from a leaf image. | Gemini 2.5 Flash |
| **Symptom Agent** | Analyzes the leaf to describe specific disease markers (spots, lesions, etc.). | Gemini 2.5 Flash |
| **Disease Agent** | Matches symptoms to a specific disease using RAG search. | Groq Llama 3.1 8B |
| **Treatment Agent** | Provides step-by-step chemical and organic treatment protocols. | Groq Llama 3.1 8B |
| **Regional Agent** | Gives seasonal advice based on the user's geographical location. | Groq Llama 3.1 8B |

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **Orchestration**: LangChain
*   **Visual Reasoning**: Google Gemini API
*   **Inference Engine**: Groq (Llama 3.1, Whisper v3)
*   **Vector Database**: ChromaDB (HuggingFace Embeddings)
*   **Database**: PostgreSQL (SQLAlchemy)
*   **Voice**: gTTS, audio-recorder-streamlit

---

## 📂 Project Structure

For a detailed look at the internal multi-agent logic and data flow, please check the **[Architecture Documentation](docs/architecture.md)**.

```text
cropcare-ai/
├── app.py                # Main Streamlit UI & Chat Logic
├── db.py                 # PostgreSQL Database Management
├── src/
│   ├── orchestrator.py   # Pipeline Controller
│   ├── vision_agent.py   # Crop Identification
│   ├── symptom_agent.py  # Symptom Analysis
│   ├── disease_agent.py  # Diagnostic Engine
│   ├── treatment_agent.py# Treatment Recommendations
│   └── regional_agent.py # Localized Agricultural Advice
├── disease_rag.py        # Disease Knowledge Base Logic
├── regional_rag.py       # Regional Knowledge Base Logic
└── requirements.txt      # Project Dependencies
```

---

## ⚙️ Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/AmirthaShreeKumar/CropCare-AI-ChatBot.git
    cd CropCare-AI-ChatBot
    ```

2.  **Set Up Environment**:
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_key
    GROQ_API_KEY=your_groq_key
    DATABASE_URL=your_postgresql_url
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

---

