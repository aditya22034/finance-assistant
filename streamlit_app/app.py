import streamlit as st
import requests
import base64

st.set_page_config(page_title="Finance Voice Assistant", layout="centered")

st.title("🎙️ Morning Market Brief - Voice Assistant")
st.markdown("Ask a question like: *'What’s our risk exposure in Asia tech stocks today, and any earnings surprises?'*")

audio_file = st.file_uploader("Upload your question (WAV/MP3)", type=["wav", "mp3"])

if audio_file:
    st.audio(audio_file, format="audio/wav")
    st.write("Transcribing...")

    try:
        files = {"file": (audio_file.name, audio_file.read())}
        stt_response = requests.post("http://voice_agent:8004/stt", files=files, timeout=200)
        # stt_response = requests.post("http://localhost:8004/stt", files=files, timeout=200)
        transcript_json = stt_response.json()
        transcript = transcript_json.get("transcript", "")
        if not transcript:
            raise ValueError("No transcript returned.")
        st.session_state["transcript"] = transcript
        st.success(f"🗣️ You said: {transcript}")
    except Exception as e:
        st.error(f" STT failed: {str(e)}")
        st.stop()

    st.write(" Calling orchestrator...")
    try:
        # orchestrator_resp = requests.get("http://orchestrator:8000/morning_brief", timeout=200)
        # # orchestrator_resp = requests.get("http://localhost:8006/morning_brief", timeout=200)
        # brief_json = orchestrator_resp.json()
        orchestrator_resp = requests.post("http://orchestrator:8000/ask", json={"query": transcript}, timeout=200)
# orchestrator_resp = requests.post("http://localhost:8006/ask", json={"query": transcript}, timeout=200)
        brief_json = orchestrator_resp.json()

        summary = brief_json.get("text", "")
        if not summary:
            raise ValueError("No summary returned.")
        st.session_state["summary"] = summary
        st.write("Market Brief:")
        st.markdown(f"> {summary}")
    except Exception as e:
        st.error(f"Orchestrator failed: {str(e)}")
        st.stop()

    if summary.startswith("LLM failed") or not summary.strip():
        st.warning("Skipping TTS due to LLM failure or empty response.")
    else:
        st.write(" Converting to audio...")
        try:
            tts_response = requests.get("http://voice_agent:8004/tts", params={"text": summary}, timeout=200)
            # tts_response = requests.get("http://localhost:8004/tts", params={"text": summary}, timeout=60)
            if tts_response.status_code != 200:
                raise ValueError(f"TTS failed with status {tts_response.status_code}")
            audio_data = tts_response.content
            b64 = base64.b64encode(audio_data).decode()
            st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
        except Exception as e:
            st.error(f" TTS failed: {str(e)}")
