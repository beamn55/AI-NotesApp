import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Notes App", page_icon="✨", layout="centered"
)

if "dark_mode" not in st.session_state:
  st.session_state.dark_mode = False

EMBEDDED_API_KEY = "AQ.Ab8RN6JSxDlxoNh-CTJEAIgn1Al5m5HPV0pOdoPp2z1fkSkrYg"

css_light = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #FFDBDB;
        color: #4A3B32;
        font-family: 'Fredoka', sans-serif;
    }
    h1, h2, h3, p, label, div {
        font-family: 'Fredoka', sans-serif !important;
    }
    .custom-app-title {
        color: #FF5C89;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: left;
        letter-spacing: 0.5px;
        margin-bottom: 0px;
        text-shadow: 1px 1px 0px #FFFFFF;
    }
    .custom-subtitle {
        text-align: left;
        color: #FB8CAC;
        font-weight: 600;
        margin-bottom: 25px;
        font-size: 1.1rem;
    }
    .note-card-pink {
        background-color: #FDA8BF;
        border: 2px solid #FF5C89;
        color: #FFFFFF !important;
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(255, 92, 137, 0.2);
    }
    .note-card-blue {
        background-color: #FDC3D1;
        border: 2px solid #FB8CAC;
        color: #4A3B32 !important;
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(251, 140, 172, 0.2);
    }
    p, label, .stRadio div, .stMarkdown {
        color: #4A3B32 !important;
    }
    .stButton>button {
        background-color: #FF5C89 !important;
        color: white !important;
        border-radius: 20px;
        border: none;
        font-weight: 700;
        padding: 12px 24px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 92, 137, 0.4);
    }
    .stButton>button:hover {
        background-color: #FB8CAC !important;
        color: white !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FDC3D1;
        border-right: 2px solid #FDA8BF;
    }
    [data-testid="stSidebar"] * {
        color: #4A3B32 !important;
    }
</style>
"""

css_dark = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');

    .stApp {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Fredoka', sans-serif;
    }
    h1, h2, h3, p, label, div {
        font-family: 'Fredoka', sans-serif !important;
    }
    .custom-app-title {
        color: #F2B0CD;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: left;
        letter-spacing: 0.5px;
        margin-bottom: 0px;
    }
    .custom-subtitle {
        text-align: left;
        color: #A0A0A0;
        font-weight: 600;
        margin-bottom: 25px;
        font-size: 1.1rem;
    }
    .note-card-pink {
        background-color: #1E1E1E;
        border: 1px solid #FF5C89;
        color: #FFFFFF !important;
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    .note-card-blue {
        background-color: #1E1E1E;
        border: 1px solid #FB8CAC;
        color: #FFFFFF !important;
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    p, label, .stRadio div, .stMarkdown {
        color: #FFFFFF !important;
    }
    .stButton>button {
        background-color: #FF5C89 !important;
        color: #121212 !important;
        border-radius: 20px;
        border: none;
        font-weight: 700;
        width: 100%;
    }
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
        border-right: 1px solid #333333;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
</style>
"""

if st.session_state.dark_mode:
  st.markdown(css_dark, unsafe_allow_html=True)
else:
  st.markdown(css_light, unsafe_allow_html=True)

st.sidebar.header("✨ Settings & Profile")
st.session_state.dark_mode = st.sidebar.toggle(
    "Dark Mode", value=st.session_state.dark_mode
)

username = st.sidebar.text_input("Username:", placeholder="Enter username")
password = st.sidebar.text_input(
    "Password:", type="password", placeholder="Enter password"
)

if st.sidebar.button("Save Settings 💾"):
  st.sidebar.success("Settings saved!")

st.markdown('<div class="custom-app-title">AI Notes App</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="custom-subtitle">✦ Let’s organize your notes today! ✨</div>',
    unsafe_allow_html=True,
)
st.write(
    "Upload audio, record via microphone, or type your notes, and Gemini will"
    " automatically generate a summary and smart tags!"
)

client = genai.Client(api_key=EMBEDDED_API_KEY)

input_mode = st.radio(
    "Select note creation method:",
    (
        "Audio File Upload (MP3/WAV)",
        "Live Microphone Recording 🎙️",
        "Text Input",
    ),
)

note_content = None
audio_file_path = "temp_uploaded_audio.wav"

if input_mode == "Audio File Upload (MP3/WAV)":
  uploaded_audio = st.file_uploader(
      "Upload your audio file:", type=["mp3", "wav", "m4a"]
  )

  if uploaded_audio is not None:
    st.audio(uploaded_audio)
    with open(audio_file_path, "wb") as f:
      f.write(uploaded_audio.getbuffer())

elif input_mode == "Live Microphone Recording 🎙️":
  recorded_audio = st.audio_input("Record your voice note:")

  if recorded_audio is not None:
    st.audio(recorded_audio)
    with open(audio_file_path, "wb") as f:
      f.write(recorded_audio.getbuffer())

else:
  note_content = st.text_area(
      "Type your notes here:",
      placeholder="Example: Meeting notes about the project deployment...",
      height=150,
  )

if st.button("Process Note with AI 💖", type="primary"):
  if (
      input_mode
      in ("Audio File Upload (MP3/WAV)", "Live Microphone Recording 🎙️")
      and os.path.exists(audio_file_path)
  ):
    with st.spinner("Analyzing audio with Gemini..."):
      try:
        uploaded_file = client.files.upload(file=audio_file_path)

        prompt = (
            "Listen to this audio recording carefully. The speaker may use"
            " English, Tagalog, or Taglish.\n\nPlease provide:\n1."
            " Transcription: The exact words spoken in the audio in the"
            " original spoken language (Tagalog/English/Taglish).\n2."
            " Summary: A clear and concise summary of the main points.\n3."
            " Tags: 3 to 5 relevant tags separated by commas."
        )

        response = client.models.generate_content(
            model="gemini-3.8-flash", contents=[uploaded_file, prompt]
        )

        st.success("Done!")

        st.markdown(
            f'<div class="note-card-pink"><h3>🌸 AI Analysis Result</h3>'
            f"<p>{response.text}</p></div>",
            unsafe_allow_html=True,
        )

        if os.path.exists(audio_file_path):
          os.remove(audio_file_path)

      except Exception as e:
        st.error(f"An error occurred: {e}")

  elif input_mode == "Text Input" and note_content:
    with st.spinner("Generating summary and tags..."):
      try:
        prompt = f"""
                Analyze the following note text (which may be in English, Tagalog, or Taglish):
                "{note_content}"
                
                Please provide:
                1. Summary: A clear and concise summary of the main points.
                2. Tags: 3 to 5 relevant tags separated by commas.
                """

        response = client.models.generate_content(
            model="gemini-3.8-flash", contents=prompt
        )

        st.success("Done!")

        st.markdown(
            f'<div class="note-card-blue"><h3>🦋 AI Analysis Result</h3>'
            f"<p>{response.text}</p></div>",
            unsafe_allow_html=True,
        )

      except Exception as e:
        st.error(f"An error occurred: {e}")
  else:
    st.warning("Please provide an audio file, record audio, or type notes first!")