# 🌱 CropCare AI: Multi-Agent Agricultural Assistant

**A production-hardened multi-agent AI system powered by Gemini and Groq that provides real-time plant disease diagnosis, treatment recommendations, and localized agricultural advice.**

---

## 🚀 Key Features

*   **🔒 Secure Access**: Account creation is gated by a mandatory **App Access Key** to prevent unauthorized usage.
*   **⏳ Rate Limiting**: Built-in protection (10 requests/min per user) to manage API costs and prevent abuse.
*   **🔍 Sequential Multi-Agent Pipeline**: Specialized agents for Vision, Symptoms, Diagnosis, Treatment, and Regional Advice.
*   **🤖 Hybrid AI Intelligence**: Leverages **Google Gemini** for visual reasoning and **Groq Llama 3** for lightning-fast text generation.
*   **🎙️ Multilingual Voice Interface**: Supports **English**, **Hindi**, and **Tamil** with real-time transcription and TTS.
*   **💬 Professional Chat Management**: Isolated, persistent chat history for every user with secure session management.

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **Intelligence**: Google Gemini API & Groq (Llama 3, Whisper v3)
*   **Database**: PostgreSQL (SQLAlchemy)
*   **Security**: Bcrypt (Password Hashing), Shared Secret Gatekeeping
*   **Voice**: gTTS, audio-recorder-streamlit

---

## ⚙️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/AmirthaShreeKumar/CropCare-AI-ChatBot.git
    cd CropCare-AI-ChatBot
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    # AI Keys
    GOOGLE_API_KEY=your_gemini_key
    GROQ_API_KEY=your_groq_key

    # Database (PostgreSQL)
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=cropcare

    # Security
    APP_SECRET=cropcare2024  # Shared key required for new sign-ups
    ```

4.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

---

## 🛡️ Security & Production Readiness
This project has been hardened for production deployment. For a detailed breakdown of the 12-pillar audit (including Caching, Logging, and Rate Limiting), please refer to the **[Architecture Documentation](docs/architecture.md)**.

*   **Passwords**: Encrypted using salted Bcrypt hashes.
*   **Rate Limiting**: Users are limited to 10 diagnostic requests per minute.
*   **Session Isolation**: Chat history is strictly isolated per user; switching accounts clears all temporary session data.
*   **Sanitization**: All database queries are parameterized to prevent SQL injection.
