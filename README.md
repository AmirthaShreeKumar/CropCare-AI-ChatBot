# 🌱 CropCare AI: Intelligent Multi-Agent Agricultural Assistant

**CropCare AI is a state-of-the-art multi-agent system that transforms how plant diseases are diagnosed. It orchestrates specialized AI agents to provide expert-level diagnostic reasoning, localized advice, and treatment protocols.**

---

## 🤖 The Multi-Agent Advantage
Unlike simple chatbots, CropCare AI uses a **Collaborative Agent Framework**. Each step of the diagnosis is handled by a specialized expert:

*   **👁️ Vision Agent**: A computer-vision specialist that identifies crop species and detects leaf anomalies.
*   **🩺 Symptom Agent**: A diagnostic reporter that translates visual signs into clinical plant symptoms.
*   **🔬 Disease Agent**: A reasoning engine that matches symptoms to known diseases using a specialized knowledge base (RAG).
*   **💊 Treatment Agent**: An agronomist that generates precise organic and chemical treatment plans.
*   **🌍 Regional Agent**: A localized consultant that adapts advice to your specific weather and soil conditions.

---

## 🚀 Key Features

*   **🧠 Intelligent Orchestration**: Sequential multi-agent pipeline for high-accuracy diagnostics.
*   **🎙️ Multilingual Voice Interface**: Full support for **English**, **Hindi**, and **Tamil** with real-time TTS.
*   **🔒 Production-Grade Security**: Gated sign-ups, Bcrypt encryption, and full session isolation.
*   **⏳ Resource Protection**: Built-in per-user rate limiting (10 req/min) to prevent API abuse.
*   **💬 Persistent Memory**: Securely stores and manages your diagnostic history in PostgreSQL.

---

## 🛠️ Tech Stack

*   **Intelligence**: Google Gemini (Vision) & Groq Llama 3 (Reasoning)
*   **Orchestration**: Custom sequential agent controller
*   **Frontend**: Streamlit (Premium UI with Glassmorphism)
*   **Database**: PostgreSQL (SQLAlchemy)
*   **Security**: Bcrypt Hashing & Shared Secret Gatekeeping

---

## ⚙️ Installation & Setup

1.  **Clone & Install**:
    ```bash
    git clone https://github.com/AmirthaShreeKumar/CropCare-AI-ChatBot.git
    cd CropCare-AI-ChatBot
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    Create a `.env` file with your `GOOGLE_API_KEY`, `GROQ_API_KEY`, `DATABASE_URL`, and `APP_SECRET`.

3.  **Run**:
    ```bash
    streamlit run app.py
    ```

---

## 🛡️ Production Readiness & Architecture
For a deep dive into the **Multi-Agent Orchestration** logic and our **12-Pillar Security Audit**, visit the **[Architecture Documentation](docs/architecture.md)**.
