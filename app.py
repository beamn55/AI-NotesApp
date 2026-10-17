import os
import time
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Voice & Text Notes", page_icon="🎙️", layout="centered"
)

st.title("AI-Powered Voice & Text Notes App")
st.write(
    "Record your voice (Tagalog/English) or type notes, and Gemini will"
    " automatically generate transcription, summary, and tags."
)

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if not api_key:
  st.warning("Please enter your Gemini API Key in the sidebar.")
else:
  client = genai.Client(api_key=api_key)

  input_mode = st.radio(
      "Select note creation method:",
      ("Voice Recording (Mic)", "Text Input"),
  )

  note_content = None

  if input_mode == "Voice Recording (Mic)":
    st.info(
        "Click the microphone icon below to speak. Click again to stop"
        " recording."
    )
    audio_data = st.audio_input("Speak now:")

    if audio_data is not None:
      st.write("Playback your recording:")
      st.audio(audio_data)

      audio_file_path = f"temp_audio_{int(time.time())}.wav"
      st.session_state["audio_file_path"] = audio_file_path
      with open(audio_file_path, "wb") as f:
        f.write(audio_data.getbuffer())

  else:
    note_content = st.text_area(
        "Type your notes here:",
        placeholder=(
            "Example: Meeting regarding the SmartFleet Palawan project"
            " deployment..."
        ),
        height=150,
    )

  if st.button("Process Note with AI", type="primary"):
    if (
        input_mode == "Voice Recording (Mic)"
        and "audio_file_path" in st.session_state
        and os.path.exists(st.session_state["audio_file_path"])
    ):
      audio_file_path = st.session_state["audio_file_path"]
      with st.spinner("Sending to Gemini for transcription and analysis"):
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

          st.success("Done.")
          st.subheader("AI Analysis Result")
          st.markdown(response.text)

          if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

        except Exception as e:
          st.error(f"An error occurred: {e}")

    elif input_mode == "Text Input" and note_content:
      with st.spinner("Generating summary and tags"):
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

          st.success("Done.")
          st.subheader("AI Analysis Result")
          st.markdown(response.text)

        except Exception as e:
          st.error(f"An error occurred: {e}")
    else:
      st.warning("Please record your voice or type notes first.")