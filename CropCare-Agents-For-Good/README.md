# CropCare-Agents-For-Good
Sequential multi-agent LLM system that analyzes PlantVillage leaf images to identify the crop, detect symptoms, classify plant diseases, and recommend treatments. Uses Gemini Flash multimodal reasoning with sequential orchestration, handling color, grayscale, and segmented images.
This is the official submission for the **Google AI Agents for Good Hackathon**.

---

## 🚀 Features

| Agent | Role |
|------|------|
| Vision Agent | Analyzes leaf images and predicts symptoms |
| Symptom Agent | Extracts key symptoms from farmer’s input text |
| Disease Agent | Determines the most probable crop disease |
| Treatment Agent | Suggests actionable treatment and prevention steps |
| Orchestrator | Coordinates all agents into one unified pipeline |

---

## 🧠 Architecture
Detailed diagrams are available in:  
📄 `docs/architecture.md`

---

## 📂 Repository Structure

```

cropcare-agents/
│
├── notebooks/
│   └── CropCare_Agents_For_Good.ipynb    <-- MAIN NOTEBOOK 
│
├── image/                                <-- few sample PlantVillage images
│                   
│
├── src/
│   ├── orchestrator.py                   <-- Full pipeline orchestrator
│   ├── vision_agent.py                   <-- Vision Agent code
│   ├── symptom_agent.py                  <-- Symptom Agent code
│   ├── disease_agent.py                  <-- Disease Agent code
│   ├── treatment_agent.py                <-- Treatment Agent code
│   └── utils.py                          <-- JSON cleaning, logging, helpers
│
├── docs/
│   ├── architecture.md                   <-- Agent architecture diagrams + explanation
│   
│
├── .gitignore                            <-- Prevents unwanted files in repo
├── LICENSE                               <-- MIT license or Apache 2.0
├── README.md                             <-- How to run + project description
└── requirements.txt                      <-- Dependencies for local execution

````

---

## 🛠 Setup Instructions (Local)



---

## 🚀 How to Run

Follow these simple steps to test **CropCare — Agents for Good** on your system:

---

### ✅ 1️⃣ Clone the Repository

```bash
git clone https://github.com/AmirthaShreeK/CropCare-Agents-For-Good.git
cd CropCare-Agents-For-Good
```

---

### 🧩 2️⃣ Create & Activate Virtual Environment

#### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📦 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If Jupyter Notebook isn’t installed:

```bash
pip install notebook
```

---

### 📓 4️⃣ Open the Notebook

```bash
jupyter notebook
```

➡ In Jupyter, open:

```
notebooks/CropCare_Agents_For_Good.ipynb
```

Run all cells **top to bottom**.

---

### 🔑 5️⃣ Setup Gemini API Key

This application **requires a valid Google Gemini API Key**.

#### Option A — Set as Environment Variable (Recommended)

##### Windows (PowerShell)

```powershell
$env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

##### macOS / Linux

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

#### Option B — (If you don’t want to use Terminal)

➡ In the **first code cell** of Jupyter Notebook, paste:

```python
import os
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
print("🔐 API Key Loaded Successfully")
```

⚠️ Replace `"YOUR_API_KEY_HERE"` with the real key.

---

### 🖼️ 6️⃣ Provide a Plant Image

Inside repository:

```bash
image/
 ├── COLOR_APPLE_HEALTHY.jpg
 ├── COLOR_CORN_MAIZE_Cercospora Leaf Spot.jpg
 ├── GRAYSCALE_CHERRY_Powdery_mildew.jpg
 ├── SEGMENTED_APPLE_APPLE SCAB.jpg
```

➡ When prompted in notebook, enter a path like:

```
..image/COLOR_APPLE_HEALTHY.jpg
```

> Ypu can also upload **their own leaf images** to \image to test detection.

---

## 🎯 What Happens Next?

The Agent Pipeline will:
1️⃣ Identify crop
2️⃣ Detect the disease
3️⃣ Generate treatment suggestions
4️⃣ Provide preventive measures & risk factors

---

### 🎉 You’re All Set

If all steps succeeded, you’ll see:
✔ Crop recognized
✔ Disease detected
✔ Cure & recommendations displayed

---

### 🆘 Need Help?

If any cell errors:

* Re-check API key
* Re-run kernel → *Restart & Run All*
* Ensure a valid image path

---



### 🎯 Expected Output

You will receive:

* Detected crop name
* Disease name (if any)
* Severity category
* Recommended treatment






---

## 📝 Input Format

| Input         | Type                        |
| ------------- | --------------------------- |
| Crop image    | JPG/PNG (Leaf)              |


---

## 🎯 Output Includes

✔ Extracted symptoms (from image + text)
✔ Top probable crop diseases
✔ Possible symptoms
✔ Validated treatment recommendations


---

## 📌 Tech Stack

* Python
* OpenAI Agents / LLM-powered services
* PlantVillage dataset (for testing)

---



---

## 📜 License

MIT License – Free for research and educational use.

---

🌾 *Empowering farmers with accessible AI crop healthcare.*

```

