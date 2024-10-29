import os
import base64
from gtts import gTTS
import streamlit as st
from io import BytesIO
from googletrans import Translator
import speech_recognition as sr
import google.generativeai as gen

# Set the page configuration
st.set_page_config(
    page_title="AgriGEN - Farmer's ChatBot",
    page_icon=":farmer:",  # Favicon emoji
)

GOOGLE_API_KEY = "AIzaSyAnFkiejM1yn6aZ6qu1RY56hgVnujYzZgk"

# Set up Google Gemini-Pro AI model
gen.configure(api_key=GOOGLE_API_KEY)
model = gen.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You should only provide answers to questions related to agriculture. Any other question will be said please ask questions related to agriculture.If any Problem is asked by user then the message should be in this format:Reason:explain in short and precise\nsolution:explain in short and precise\ntreatment:explain in short with exact dosage",
)

# Function to translate text with caching
@st.cache_data
def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

# Function to translate the entire app's text elements
def translate_app_texts(texts, dest_lang):
    translated_texts = {}
    for key, text in texts.items():
        translated_texts[key] = translate_text(text, dest_lang)
    return translated_texts

# Define the text elements in the app
app_texts = {
    "title": "AgriGEN - Farmer's ChatBot",
    "language_select": "Select Language",
    "ask_here": "Ask here...",
    "speak_button": "Speak",
    "listening": "Listening...",
    "could_not_understand": "Google Speech Recognition could not understand audio",
    "request_error": "Could not request results from Google Speech Recognition service",
    "you_said": "You said: ",
}

# Add a dropdown menu for language selection in the sidebar
language = st.sidebar.selectbox(
    app_texts["language_select"],
    ("English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam")
)

# Map the selected language to the corresponding language code
language_code = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml"
}[language]

# Translate the app's text elements to the selected language
translated_texts = translate_app_texts(app_texts, language_code)

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Function to convert text to speech and play in browser
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    audio_data = audio_fp.read()
    audio_base64 = base64.b64encode(audio_data).decode()
    audio_html = f"""
    <audio id="response_audio" autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    <script>
        var audio = document.getElementById('response_audio');
        audio.play();
    </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Function to recognize speech and convert it to text
def recognize_speech(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(translated_texts["listening"])
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=language_code)
            st.success(f"{translated_texts['you_said']} {text}")
            return text
        except sr.UnknownValueError:
            st.error(translated_texts["could_not_understand"])
        except sr.RequestError as e:
            st.error(f"{translated_texts['request_error']}; {e}")
    return ""

# JavaScript to stop the audio
stop_audio_js = """
<script>
function stopAudio() {
    var audio = document.getElementById('response_audio');
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
    }
}
</script>
"""
st.markdown(stop_audio_js, unsafe_allow_html=True)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title(translated_texts["title"])

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input(translated_texts["ask_here"])

# Button to capture speech
if st.button(translated_texts["speak_button"]):
    st.markdown("<script>stopAudio();</script>", unsafe_allow_html=True)
    user_prompt = recognize_speech(language_code)

if user_prompt:
    st.markdown("<script>stopAudio();</script>", unsafe_allow_html=True)
    # Translate user's prompt to the selected language if necessary
    if language_code != "en":
        user_prompt_translated = translate_text(user_prompt, dest_lang=language_code)
    else:
        user_prompt_translated = user_prompt

    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt_translated)

    # Translate Gemini-Pro's response to the selected language if necessary
    if language_code != "en":
        gemini_response_translated = translate_text(gemini_response.text, dest_lang=language_code)
    else:
        gemini_response_translated = gemini_response.text

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response_translated)
    
    # Convert Gemini-Pro's response to speech and play in browser
    text_to_speech(gemini_response_translated, lang=language_code)