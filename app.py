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


load_dotenv()




llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


from db import save_message, get_all_chats, get_chat_messages, create_chat, get_chat_title, get_all_chats_with_titles, update_chat_title


from src.orchestrator import orchestrate_pipeline

def generate_chat_title(message):
    """Generate a meaningful chat title from the first message"""
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

def transcribe_audio(audio_bytes, language_code):
    """Transcribe audio bytes using Groq Whisper with explicit language"""
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

def text_to_speech(text, lang):
    """Convert text to speech and return a clickable audio player"""
    try:
        # Use provided lang code for gTTS
        
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

def translate_response(text, target_lang_hint):
    """Translate the final response to the target language if necessary"""
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
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown('<div class="title-container"><h1>🌱 CropCare AI Assistant</h1></div>', unsafe_allow_html=True)

with col2:
    if st.button("New Chat", use_container_width=True):
        new_chat_id = str(uuid.uuid4())
        st.session_state.chat_id = new_chat_id
        st.session_state.messages = []
        st.session_state.uploader_key += 1
        create_chat(new_chat_id, "New Chat")
        st.rerun()


if "chat_id" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chat_id = chat_id
    create_chat(chat_id, "New Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


st.sidebar.title("💬 Settings")
selected_lang_name = st.sidebar.selectbox(
    "Preferred Language / மொழி / भाषा",
    options=list(LANGUAGES.keys()),
    index=0
)
selected_lang_code = LANGUAGES[selected_lang_name]

st.sidebar.title("💬 Chat History")


chats = get_all_chats_with_titles()

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
        st.write(display_content)
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

    # Prioritize user_input, then audio_input, then image
    effective_input = user_input or audio_input
    
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
        image_path = f"temp_{uploaded_file.name}"

        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        
        from src.regional_agent import detect_location_from_text
        detected_location = detect_location_from_text(effective_input or "")

        with st.spinner("Analyzing plant... 🌿"):
            result = orchestrate_pipeline(image_path, effective_input or "", detected_location)

        treatment_steps = result.get("treatment_info", {}).get("treatment_steps", [])
        precautions = result.get("treatment_info", {}).get("safety_precautions", [])

        
        disease_info = result['disease_info']

        response = f"""
🌿 **Crop:** {result['crop_info']['crop']}

🦠  **Disease:** {disease_info['disease_name']}

📊 **Confidence:** {disease_info['confidence']}

🔍 **Symptoms:**  
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

🌍 **Regional Advice for {regional.get('region', detected_location)}:**

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
        # Translate response if input was not English
        if selected_lang_name != "English":
            with st.spinner(f"Translating to {selected_lang_name}..."):
                response = translate_response(response, selected_lang_name)

        
        st.session_state.uploader_key += 1

    
    else:
        past_msgs = get_chat_messages(st.session_state.chat_id)

        # Limit history to last 5 messages to avoid Groq token limits
        history = "\n".join([
            f"{m['role'].upper()}: {m['content'][:500]}..." if len(m['content']) > 500 else f"{m['role'].upper()}: {m['content']}"
            for m in past_msgs[-5:]
        ])

        
        from src.regional_agent import detect_location_from_text, get_regional_advice

        detected_location = detect_location_from_text(effective_input)
        is_agricultural_query = effective_input and any(keyword in effective_input.lower() for keyword in [
            'crop', 'plant', 'farm', 'agriculture', 'season', 'climate', 'soil',
            'water', 'pest', 'disease', 'fertilizer', 'harvest', 'planting'
        ])

        if detected_location and is_agricultural_query:
         
            regional_advice = get_regional_advice(detected_location, "", effective_input)

            response = f"""
🌍 **Regional Agricultural Advice for {detected_location}**

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
            
            # Explicitly detect language of the current message
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

       
    # Generate audio only if it was a voice-only interaction
    assistant_audio_b64 = None
    if is_voice_turn:
        with st.spinner("Generating voice response..."):
            reply_audio = text_to_speech(response, selected_lang_code)
            if reply_audio:
                assistant_audio_b64 = base64.b64encode(reply_audio).decode("utf-8")
    
    save_message(st.session_state.chat_id, "assistant", response, assistant_audio_b64)
    st.session_state.messages.append({"role": "assistant", "content": response, "audio_content": assistant_audio_b64})
    
    with st.chat_message("assistant"):
        st.write(response)
        if assistant_audio_b64:
            st.audio(base64.b64decode(assistant_audio_b64))





