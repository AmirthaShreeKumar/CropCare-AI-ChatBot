# 🏗️ Architecture Design: Collaborative Multi-Agent System

CropCare AI is designed as a **Sequential Multi-Agent System**. Instead of relying on a single general-purpose AI model, it decomposes the complex agricultural diagnostic process into a series of specialized tasks, each handled by a dedicated "Expert Agent."

---

## 🖼️ System Architecture Diagram
The diagram below illustrates how user data flows through the security layer into the multi-agent orchestration core.

![System Architecture](Architecture.png)

---

## 🤖 The Multi-Agent Orchestration Core
The heart of the system is `src/orchestrator.py`, which manages the state and handoffs between the following agents:

### 1. Vision Agent (`src/vision_agent.py`)
*   **Role**: Visual Perception Specialist.
*   **Action**: Analyzes uploaded images using Gemini Pro Vision. It identifies the crop type and locates specific leaf anomalies or discoloration patterns.
*   **Output**: Structured visual markers.

### 2. Symptom Agent (`src/symptom_agent.py`)
*   **Role**: Diagnostic Reporter.
*   **Action**: Takes the raw visual markers and translates them into a professional agricultural symptom report (e.g., "Interveinal chlorosis with necrotic spotting").
*   **Output**: Technical symptom description.

### 3. Disease Agent (`src/disease_agent.py`)
*   **Role**: Diagnostic Pathologist.
*   **Action**: Uses **Retrieval-Augmented Generation (RAG)** to query the internal `disease_knowledge_base`. It matches the technical symptoms against thousands of documented crop diseases.
*   **Output**: Confirmed diagnosis and confidence level.

### 4. Treatment Agent (`src/treatment_agent.py`)
*   **Role**: Agronomist & Pharmacist.
*   **Action**: Generates a tiered treatment plan, providing both **organic (biological)** and **chemical** solutions for the identified disease.
*   **Output**: Step-by-step recovery protocol.

### 5. Regional Agent (`src/regional_agent.py`)
*   **Role**: Local Field Consultant.
*   **Action**: Injects geographical context by querying the `regional_knowledge_base`. It adapts the treatment based on local weather conditions and provides preventive measures specific to the user's region.
*   **Output**: Localized advice and preventive strategies.

---

## 🔄 Data Pipeline Flow
1.  **Safety Interception**: Request is sanitized by `src/safety.py`.
2.  **State Initialization**: Orchestrator creates a shared state object.
3.  **Sequential Execution**: Agents run in order (Vision → Symptom → Disease → Treatment → Regional). Each agent enriches the shared state with its expert findings.
4.  **Final Synthesis**: The Orchestrator merges all agent outputs into a final, user-friendly summary.
5.  **Persistence**: The entire interaction is saved to the PostgreSQL database for future reference.

---

## 🛡️ Production Readiness Audit (12 Pillars)
While the agents provide the intelligence, the following 12 pillars provide the **stability and security**:

1.  **Deterministic Safety**: Keywords + LLM-based filtering.
2.  **Async AI Clients**: Non-blocking client initialization.
3.  **Schema Validation**: Pydantic models for all data exchange.
4.  **App Access Gate**: `APP_SECRET` required for registration.
5.  **Generic Error Handling**: Sanitized user-facing exceptions.
6.  **Persistent State**: PostgreSQL via SQLAlchemy.
7.  **Agent Loop Guard**: `MAX_STEPS` prevents infinite reasoning loops.
8.  **Context Management**: Automatic history slicing and summarization.
9.  **Rate Limiting**: Sliding-window 10 requests/min per user.
10. **SQL Sanitization**: 100% parameterized queries.
11. **Media Cleanup**: Automated purging of temp files.
12. **Singleton/Factory**: Centralized resource management in `src/factory.py`.
