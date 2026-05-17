import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from audio_recorder_streamlit import audio_recorder
import tempfile
from gtts import gTTS
import base64


from src.cleanup import cleanup_old_temp_files
from src.logger import logger
from src.rate_limiter import limiter

load_dotenv()

logger.info("CropCare AI App starting up...")

# Cleanup old temp files on startup
cleanup_old_temp_files()




from src.factory import AIClientFactory

llm = AIClientFactory.get_llm()
groq_client = AIClientFactory.get_groq_client()


from db import save_message, get_all_chats, get_chat_messages, create_chat, get_chat_title, get_all_chats_with_titles, update_chat_title, init_db, create_user, authenticate_user

# Initialize database tables
init_db()


from src.orchestrator import orchestrate_pipeline
from src.safety import safety_interceptor
from src.summarizer import summarizer

@st.cache_data(show_spinner=False)
def generate_chat_title(message):
    """Generate a meaningful chat title from the first message (cached)"""
    if not message:
        return "New Chat"

    # Clean and truncate the message
    title = message.strip()

    # If it's an image upload message, make it more descriptive
    if title.startswith("📷"):
        return "Plant Disease Analysis"

    # Remove common prefixes and get first meaningful part
    prefixes_to_remove = ["I have", "I want", "Can you", "Please", "Help with", "About"]
    for prefix in prefixes_to_remove:
        if title.lower().startswith(prefix.lower()):
            title = title[len(prefix):].strip()
            break

    # Truncate to reasonable length
    if len(title) > 50:
        title = title[:47] + "..."

    # Capitalize first letter
    if title:
        title = title[0].upper() + title[1:]

    return title or "New Chat"

LANGUAGES = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Tamil (தமிழ்)": "ta"
}

@st.cache_data(show_spinner=False)
def transcribe_audio(audio_bytes, language_code):
    """Transcribe audio bytes using Groq Whisper (cached)"""
    if not audio_bytes:
        return None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(tmp_path, file.read()),
                model="whisper-large-v3",
                language=language_code,
                prompt=f"The audio is in {language_code}. It is related to agriculture.",
                response_format="text",
            )
        
        # Cleanup
        os.unlink(tmp_path)
        
        return transcription.strip()
    except Exception as e:
        st.error(f"Error transcribing audio with Groq: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def text_to_speech(text, lang):
    """Convert text to speech (cached)"""
    try:
        logger.info(f"Generating TTS for text: {text[:50]}...")
        
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        
        os.unlink(tmp_path)
        return audio_bytes
    except Exception as e:
        st.error(f"Error in TTS: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def translate_response(text, target_lang_hint):
    """Translate the final response (cached)"""
    if not target_lang_hint or target_lang_hint.lower() == 'english':
        return text
    
    try:
        prompt = f"Translate the following agricultural advice to {target_lang_hint}. Maintain the formatting and professional tone.\n\nText:\n{text}"
        response = llm.invoke(prompt)
        return response.content
    except:
        return text


st.set_page_config(
    page_title="CropCare AI Assistant",
    page_icon="🌱",
    layout="wide"
)

# Modern UI Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;500;600;700&display=swap');

    .main {
        background-color: #f3f4f6;
        background-image: radial-gradient(#e5e7eb 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        color: #1f2937;
        font-weight: 600;
    }

    .title-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 25px;
        margin-bottom: 25px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3), 0 4px 6px -2px rgba(16, 185, 129, 0.15);
    }
    
    .title-container h1 {
        color: white;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.5);
        box-shadow: 2px 0 20px rgba(0,0,0,0.02);
    }
    
    .stChatMessage {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        color: #10b981;
    }
    
    /* Input field styling */
    .stChatInput {
        border-radius: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid #e5e7eb !important;
    }

    /* Hide browser default password reveal eye icon to prevent double eyes */
    input[type="password"]::-ms-reveal,
    input[type="password"]::-ms-clear {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown('<div class="title-container"><h1>🌱 CropCare AI Assistant</h1></div>', unsafe_allow_html=True)

with col2:
    if st.session_state.get("authenticated", False):
        if st.button("New Chat", use_container_width=True):
            new_chat_id = str(uuid.uuid4())
            st.session_state.chat_id = new_chat_id
            st.session_state.messages = []
            st.session_state.uploader_key += 1
            create_chat(new_chat_id, st.session_state.user_id, "New Chat")
            st.rerun()


if "chat_id" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chat_id = chat_id
    # Only create the chat if we are already authenticated
    if st.session_state.get("authenticated"):
        create_chat(chat_id, st.session_state.user_id, "New Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <style>
        /* Full page background */
        .stApp {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        }
        
        /* Centered login card */
        .login-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 20px 40px rgba(0,0,0,0.05);
            max-width: 450px;
            margin: 60px auto;
            text-align: center;
        }
        
        .login-header h1 {
            color: #065f46;
            font-size: 2.2rem;
            margin-bottom: 8px;
            font-weight: 700;
        }
        
        .login-subtitle {
            color: #059669;
            font-size: 1rem;
            margin-bottom: 30px;
            opacity: 0.8;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            justify-content: center;
            border-bottom: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            background-color: transparent !important;
            border-radius: 8px !important;
            padding: 0 24px !important;
            font-weight: 600 !important;
            border: none !important;
            color: #6b7280 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #10b981 !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            border-radius: 12px !important;
            padding: 12px !important;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            margin-top: 10px;
        }
        </style>
        
        <div class="login-card">
            <div class="login-header">
                <h1>🌱 CropCare AI</h1>
                <div class="login-subtitle">Intelligent Agriculture Companion</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Place tabs inside a container to align with the styled card
    _, container_col, _ = st.columns([1, 2, 1])
    
    with container_col:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            login_user = st.text_input("Username", key="l_user", placeholder="Enter your username")
            login_pass = st.text_input("Password", type="password", key="l_pass", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login", key="login_btn"):
                user_id = authenticate_user(login_user, login_pass)
                if user_id:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_id
                    st.session_state.username = login_user
                    # Always start with a FRESH chat_id on login to avoid sharing from previous session
                    st.session_state.chat_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    
                    create_chat(st.session_state.chat_id, user_id, "New Chat")
                    logger.info(f"User '{login_user}' logged in successfully. New chat started: {st.session_state.chat_id}")
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    logger.warning(f"Failed login attempt for user '{login_user}'.")
                    st.error("Invalid credentials")
                    
        with tab2:
            new_user = st.text_input("Choose Username", key="s_user", placeholder="e.g. amirtha123")
            new_pass = st.text_input("Set Password", type="password", key="s_pass", placeholder="Min. 6 characters")
            confirm_pass = st.text_input("Confirm Password", type="password", key="s_confirm")
            app_secret_input = st.text_input("App Access Key", type="password", key="s_secret", placeholder="Enter shared secret")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account", key="signup_btn"):
                if app_secret_input != os.getenv("APP_SECRET"):
                    st.error("Invalid App Access Key. You cannot create an account.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match")
                elif len(new_pass) < 6:
                    st.error("Password too short")
                else:
                    if create_user(new_user, new_pass):
                        logger.info(f"New user account created: '{new_user}'")
                        st.success("Success! You can now log in.")
                    else:
                        logger.warning(f"Failed account creation for '{new_user}' (possibly exists).")
                        st.error("Username taken")
    st.stop()

# Main App Sidebar
with st.sidebar:
    st.title(f"👤 {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
    st.divider()

st.sidebar.title("💬 Settings")
selected_lang_name = st.sidebar.selectbox(

    "Preferred Language / மொழி / भाषा",
    options=list(LANGUAGES.keys()),
    index=0
)
selected_lang_code = LANGUAGES[selected_lang_name]

st.sidebar.title("💬 Chat History")


chats = get_all_chats_with_titles(st.session_state.user_id)

for chat in chats:
    chat_id = chat["chat_id"]
    title = chat["title"] or f"Chat {chat_id[:6]}"

    
    with st.sidebar.container():
        col1, col2 = st.sidebar.columns([4, 1])

        with col1:
            if st.button(f"📄 {title}", key=f"chat_{chat_id}"):
                st.session_state.chat_id = chat_id
                st.session_state.messages = get_chat_messages(chat_id)
                st.session_state.uploader_key += 1  # reset uploader
                st.rerun()

        with col2:
            if st.button("📝", key=f"rename_btn_{chat_id}", help="Rename chat"):
                st.session_state[f"rename_mode_{chat_id}"] = True

    
    if st.session_state.get(f"rename_mode_{chat_id}", False):
        with st.sidebar.container():
            new_title = st.text_input(
                "New title:",
                value=title,
                key=f"title_input_{chat_id}",
                max_chars=50
            )
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("Save", key=f"save_{chat_id}"):
                    update_chat_title(chat_id, new_title)
                    st.session_state[f"rename_mode_{chat_id}"] = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_{chat_id}"):
                    st.session_state[f"rename_mode_{chat_id}"] = False
                    st.rerun()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        display_content = msg["content"]
        if msg.get("audio_content") and msg["role"] == "user":
            display_content = f"🎙️ {display_content}"
        st.markdown(display_content, unsafe_allow_html=True)
        if msg.get("audio_content"):
            try:
                st.audio(base64.b64decode(msg["audio_content"]))
            except Exception as e:
                st.error(f"Error playing audio: {str(e)}")


st.markdown("---")

uploaded_file = st.file_uploader(
    "📎 Upload Image",
    type=["jpg", "png"],
    key=st.session_state.uploader_key
)

# Voice Recording
st.write("Click the mic to speak:")
audio_bytes = audio_recorder(
    text="",
    recording_color="#e75480",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="2x",
)

audio_input = None
# Check if we have new audio
if audio_bytes and audio_bytes != st.session_state.get('last_audio'):
    with st.spinner("Transcribing..."):
        audio_input = transcribe_audio(audio_bytes, selected_lang_code)
        st.session_state.last_audio = audio_bytes
        st.session_state.is_voice_interaction = True
else:
    st.session_state.is_voice_interaction = False

user_input = st.chat_input("Ask about your crop...")


def format_list(data):
    if not data:
        return "No data available"

    formatted = []
    for item in data:
        if isinstance(item, str):
            formatted.append(item)
        elif isinstance(item, dict):
            formatted.append(
                item.get("step") or
                item.get("text") or
                item.get("description") or
                str(item)
            )
        else:
            formatted.append(str(item))

    return "\n- " + "\n- ".join(formatted)


if user_input or uploaded_file or audio_input:
    # Rate Limiting Check
    allowed, wait_time = limiter.is_allowed()
    if not allowed:
        st.error(f"Rate limit reached. Please wait {wait_time} seconds before your next query.")
        st.stop()
        
    logger.info("New user interaction detected.")

    # Prioritize user_input, then audio_input, then image
    effective_input = user_input or audio_input
    
    # Safety Check
    if effective_input and not safety_interceptor.is_agricultural_query(effective_input):
        st.warning("I am sorry, but I can only assist with agricultural queries related to crops, plants, and farming.")
    else:
        # Track if this specific turn is a voice turn
        is_voice_turn = bool(audio_input) and not user_input and not uploaded_file
        
        user_msg = effective_input if effective_input else " 📷 Image uploaded"

        # Store audio ONLY if this was a voice-driven turn
        user_audio_b64 = None
        if is_voice_turn and audio_bytes:
            user_audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        save_message(st.session_state.chat_id, "user", user_msg, user_audio_b64)
        st.session_state.messages.append({"role": "user", "content": user_msg, "audio_content": user_audio_b64})

        past_msgs = get_chat_messages(st.session_state.chat_id)

        if len(past_msgs) == 1:  
            title = generate_chat_title(user_msg)
            update_chat_title(st.session_state.chat_id, title)

        with st.chat_message("user"):
            st.write(f"🎙️ {user_msg}" if user_audio_b64 else user_msg)

        if uploaded_file is not None:
            logger.info(f"Image uploaded: {uploaded_file.name}")
            image_path = f"temp_{uploaded_file.name}"

            with open(image_path, "wb") as f:
                f.write(uploaded_file.read())

            from src.regional_agent import detect_location_from_text
            detected_location = detect_location_from_text(effective_input or "")

            try:
                import time
                with st.status("🌿 CropCare AI: Executing Hybrid Multimodal Pipeline...", expanded=True) as status:
                    st.write("🔍 Initializing PyTorch Perception Layers...")
                    time.sleep(0.4)
                    st.write("👁️ Phase 1: Running Local CV Model (MobileNetV2)...")
                    
                    result = orchestrate_pipeline(image_path, effective_input or "", detected_location)
                    
                    st.write("📝 Phase 2: Analyzing physical leaf symptoms...")
                    st.write("🔬 Phase 3: Consulting Pathfinder Reasoning Layer & ChromaDB RAG...")
                    st.write("💊 Phase 4: Prescribing clinical treatments & safety precautions...")
                    if detected_location:
                        st.write(f"🌍 Phase 5: Assessing local agricultural threats for {detected_location}...")
                    
                    time.sleep(0.3)
                    status.update(label="✅ Analysis Succeeded!", state="complete", expanded=False)
                
                if "error" in result:
                    logger.error(f"Orchestration pipeline failed: {result['error']}")
                    st.error(f"Analysis failed: {result['error']}")
                    st.stop()
            except Exception as e:
                logger.error(f"Unexpected error in image analysis: {e}", exc_info=True)
                st.error("An unexpected error occurred during plant analysis. Please try again with a clearer image.")
                st.stop()

            treatment_steps = result.get("treatment_info", {}).get("treatment_steps", [])
            precautions = result.get("treatment_info", {}).get("safety_precautions", [])
            
            disease_info = result['disease_info']

            # Construct Visual Badge & Warning Alert Card
            pred_source = disease_info.get("prediction_source", "Fallback Mode: Gemini Vision Analysis")
            cv_conf = disease_info.get("cv_confidence")
            
            if cv_conf is not None:
                conf_pct = round(cv_conf * 100, 2)
                conf_display = f"{conf_pct}%"
                if cv_conf < 0.75:
                    conf_color = "#e07a5f"
                    warning_alert = f"""
<div style='background-color: #fffbeb; border: 1px solid #fef3c7; border-left: 5px solid #d97706; padding: 15px; border-radius: 12px; margin-top: 15px;'>
    <span style='font-size: 1.2rem; margin-right: 8px;'>⚠️</span>
    <b style='color: #b45309;'>Low Classifier Confidence ({conf_display})</b>
    <p style='color: #78350f; font-size: 0.9rem; margin: 4px 0 0 0;'>
        The deep learning classifier indicates high uncertainty. CropCare's AI Pathfinder and RAG reasoning pipeline is executing a deep verification of symptoms.
    </p>
</div>
"""
                else:
                    conf_color = "#10b981"
                    warning_alert = ""
            else:
                conf_display = str(disease_info.get("confidence", "high")).upper()
                conf_color = "#10b981" if conf_display == "HIGH" else "#cda250"
                warning_alert = ""

            badge_html = f"""
<div style='background: linear-gradient(135deg, #ffffff 0%, #f7f9f6 100%); padding: 20px; border-radius: 16px; border: 1px solid rgba(27,77,62,0.1); box-shadow: 0 4px 20px rgba(0,0,0,0.02); margin-bottom: 20px;'>
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
        <span style='background-color: rgba(16,185,129,0.1); color: #065f46; font-size: 0.75rem; font-weight: 600; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; font-family: "Outfit", sans-serif;'>
            {pred_source}
        </span>
        <span style='font-size: 0.85rem; color: #6b7280; font-weight: 500;'>
            Confidence: <b style='color: {conf_color};'>{conf_display}</b>
        </span>
    </div>
    <div style='display: flex; gap: 15px; align-items: center;'>
        <span style='font-size: 2.2rem;'>🍃</span>
        <div>
            <div style='font-size: 0.8rem; text-transform: uppercase; color: #9ca3af; letter-spacing: 0.5px;'>Pathfinder Diagnosis</div>
            <div style='font-size: 1.4rem; font-weight: 700; color: #1f2937; font-family: "Outfit", sans-serif;'>{disease_info['disease_name']}</div>
            <div style='font-size: 0.9rem; color: #4b5563; margin-top: 2px;'>Crop Species: <b>{result['crop_info']['crop']}</b></div>
        </div>
    </div>
    {warning_alert}
</div>
"""

            # Get timing metrics
            metrics = result.get("performance_metrics", {})
            cv_time = metrics.get("cv_inference_sec", 0.0)
            symptom_time = metrics.get("symptom_analysis_sec", 0.0)
            reasoning_time = metrics.get("disease_reasoning_sec", 0.0)
            treatment_time = metrics.get("treatment_generation_sec", 0.0)
            regional_time = metrics.get("regional_analysis_sec", 0.0)
            total_time = metrics.get("total_pipeline_sec", 0.0)

            # Determine Inference Engine details
            if cv_conf is not None:
                inference_engine = "MobileNetV2 + Groq Llama 3.1"
                fallback_status = "Inactive"
                fallback_color = "#10b981"
            else:
                inference_engine = "Gemini Vision (Fallback)"
                fallback_status = "Active"
                fallback_color = "#e07a5f"

            metrics_html = f"""
<div style='background: linear-gradient(135deg, #1b3d33 0%, #0d1f1a 100%); padding: 22px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin-bottom: 20px; color: #ffffff; font-family: "Outfit", sans-serif;'>
    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;'>
        <span style='font-size: 1.3rem;'>⚡</span>
        <span style='font-weight: 700; font-size: 1.1rem; letter-spacing: 0.5px; color: #10b981;'>System Performance Metrics</span>
    </div>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; margin-bottom: 15px;'>
        <div>
            <div style='font-size: 0.75rem; text-transform: uppercase; color: #9ca3af; letter-spacing: 0.5px;'>🧠 Inference Engine</div>
            <div style='font-size: 0.9rem; font-weight: 600; color: #e5e7eb; margin-top: 4px;'>{inference_engine}</div>
        </div>
        <div>
            <div style='font-size: 0.75rem; text-transform: uppercase; color: #9ca3af; letter-spacing: 0.5px;'>📊 Confidence</div>
            <div style='font-size: 0.9rem; font-weight: 600; color: {conf_color}; margin-top: 4px;'>{conf_display}</div>
        </div>
        <div>
            <div style='font-size: 0.75rem; text-transform: uppercase; color: #9ca3af; letter-spacing: 0.5px;'>🔄 Fallback Mode</div>
            <div style='font-size: 0.9rem; font-weight: 600; color: {fallback_color}; margin-top: 4px;'>{fallback_status}</div>
        </div>
    </div>
    <div style='padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05);'>
        <div style='font-size: 0.8rem; font-weight: 700; color: #10b981; margin-bottom: 8px;'>⏱️ Pipeline Stage Latencies:</div>
        <div style='display: flex; flex-direction: column; gap: 6px; font-size: 0.85rem; color: #d1d5db;'>
            <div style='display: flex; justify-content: space-between;'>
                <span>👁️ CV Perception Inference:</span>
                <span style='font-family: monospace; font-weight: 600;'>{cv_time} sec</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>📝 Symptom Analysis Extraction:</span>
                <span style='font-family: monospace; font-weight: 600;'>{symptom_time} sec</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>🔬 Disease Pathfinder (RAG Verification):</span>
                <span style='font-family: monospace; font-weight: 600;'>{reasoning_time} sec</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>💊 Treatment Prescription Formulation:</span>
                <span style='font-family: monospace; font-weight: 600;'>{treatment_time} sec</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>🌍 Regional Environmental Intelligence:</span>
                <span style='font-family: monospace; font-weight: 600;'>{regional_time} sec</span>
            </div>
            <div style='display: flex; justify-content: space-between; font-weight: 700; color: #ffffff; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 6px; margin-top: 4px;'>
                <span>⏱️ Total End-to-End Latency:</span>
                <span style='font-family: monospace; color: #10b981;'>{total_time} sec</span>
            </div>
        </div>
    </div>
</div>
"""

            response = badge_html + metrics_html + f"""
🌿 **Crop:** {result['crop_info']['crop']}

🦠 **Disease:** {disease_info['disease_name']}

🔍 **Symptoms:**  
{result['symptoms']}
"""

            if disease_info.get('detailed_info'):
                detailed = disease_info['detailed_info']
                if 'Causes:' in detailed:
                    causes = detailed.split('Causes:')[1].split('Conditions:')[0].strip()
                    response += f"\n🧬 **Causes:** {causes[:200]}..."

                if 'Prevention:' in detailed:
                    prevention = detailed.split('Prevention:')[1].split('Treatments:')[0].strip()
                    response += f"\n🛡️ **Prevention:** {prevention[:300]}..."
            
            response += f"""

💊 **Treatment Steps:**  
{format_list(treatment_steps)}

⚠️ **Safety Precautions:**  
{format_list(precautions)}
"""

            if disease_info.get('treatments'):
                treatments = disease_info['treatments']
                if 'Treatments:' in treatments:
                    treatment_section = treatments.split('Treatments:')[1].strip()
                    response += f"\n\n📋 **Recommended Treatments:**\n{treatment_section[:500]}..."

            if result.get('regional_advice'):
                regional = result['regional_advice']
                response += f"""

🌍  **Regional Advice for {regional.get('region', detected_location)}:**

🌾 **Best Crops:** {', '.join(regional.get('best_crops', []))}

📅 **Seasonal Advice:** {regional.get('seasonal_advice', 'N/A')}

🌤️ **Climate Considerations:** {regional.get('climate_considerations', 'N/A')}

💡 **Recommended Practices:**  
{format_list(regional.get('recommended_practices', []))}

💧 **Water Management:** {regional.get('water_management', 'N/A')}

🐛 **Pest/Disease Alerts:**  
{format_list(regional.get('pest_disease_alerts', []))}
"""

            if disease_info.get('regional_risks'):
                response += f"\n\n⚠️ **Regional Disease Risks:** {disease_info['regional_risks']}"
            
            if selected_lang_name != "English":
                with st.spinner(f"Translating to {selected_lang_name}..."):
                    response = translate_response(response, selected_lang_name)

            st.session_state.uploader_key += 1

        else:
            # Aggressively truncate history to protect Groq 6000 TPM limit
            recent_msgs = past_msgs[-5:] # Only take the last 5 messages
            history_lines = []
            import re
            for m in recent_msgs:
                content = m['content']
                # Strip out the giant HTML metrics/badges to save tokens
                content = re.sub(r'<div.*?>.*?</div>', '', content, flags=re.DOTALL)
                
                # Truncate remaining text if it's still too long
                if len(content) > 600:
                    content = content[:600] + "\n... [Content Truncated for Context Limit]"
                history_lines.append(f"{m['role'].upper()}: {content.strip()}")
            history = "\n".join(history_lines)

            from src.regional_agent import detect_location_from_text, get_regional_advice

            detected_location = detect_location_from_text(effective_input)
            is_agricultural_query = effective_input and any(keyword in effective_input.lower() for keyword in [
                'crop', 'plant', 'farm', 'agriculture', 'season', 'climate', 'soil',
                'water', 'pest', 'disease', 'fertilizer', 'harvest', 'planting'
            ])

            if detected_location and is_agricultural_query:
                regional_advice = get_regional_advice(detected_location, "", effective_input)

                response = f"""
🌍  **Regional Agricultural Advice for {detected_location}**

Based on your query: "{user_input}"

🌾 **Best Crops:** {', '.join(regional_advice.get('best_crops', []))}

📅 **Seasonal Advice:** {regional_advice.get('seasonal_advice', 'N/A')}

🌤️ **Climate Considerations:** {regional_advice.get('climate_considerations', 'N/A')}

💡 **Recommended Practices:**  
{format_list(regional_advice.get('recommended_practices', []))}

💧 **Water Management:** {regional_advice.get('water_management', 'N/A')}

🐛 **Pest/Disease Alerts:**  
{format_list(regional_advice.get('pest_disease_alerts', []))}
"""
            else:
                detected_lang = "English"
                if any('\u0B80' <= c <= '\u0BFF' for c in effective_input): detected_lang = "Tamil"
                elif any('\u0900' <= c <= '\u097F' for c in effective_input): detected_lang = "Hindi"

                prompt = f"""
You are a helpful agricultural assistant chatbot.
The user's preferred language is {selected_lang_name}.

STRICT REQUIREMENT: You MUST respond in {selected_lang_name} only.
- If English is selected, respond in English.
- If Hindi is selected, respond in Hindi using Devanagari script.
- If Tamil is selected, respond in Tamil script.

You can use the conversation history below for context, but you are also allowed to use your general agricultural knowledge to answer helpfully.

Conversation History:
{history}

User's current question: {effective_input}

Answer clearly and helpfully in {selected_lang_name}.
"""
                with st.spinner("Thinking..."):
                    response = llm.invoke(prompt).content

        assistant_audio_b64 = None
        if is_voice_turn:
            with st.spinner("Generating voice response..."):
                reply_audio = text_to_speech(response, selected_lang_code)
                if reply_audio:
                    assistant_audio_b64 = base64.b64encode(reply_audio).decode("utf-8")
        
        save_message(st.session_state.chat_id, "assistant", response, assistant_audio_b64)
        st.session_state.messages.append({"role": "assistant", "content": response, "audio_content": assistant_audio_b64})
        
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
            if assistant_audio_b64:
                st.audio(base64.b64decode(assistant_audio_b64))






