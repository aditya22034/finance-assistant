## 🎥 Demo Video (Watch This First!)

🔗 [Click here to watch the full demo video](https://drive.google.com/file/d/1-xwKQ4mKdtxT80FnPW4khKFV0P6XkVgO/view?usp=sharing)

> 💡 This video walks through:
> - 🔊 Voice-to-text using Whisper
> - 🧠 Query execution and summarization via LLM (Mistral on Ollama)
> - 🤖 Full end-to-end conversation flow from voice input to AI-generated summary

⚠️ Note: Full functionality requires local Ollama running. See setup instructions below.


🚀 Deployed App: [Try it here](https://finance-assistant-ieywnvvlgvapjvz6msdw3t.streamlit.app/)

🧠 Note: To get full functionality (voice-to-text, AI answers), clone this repo and:
- Install [Ollama](https://ollama.com/)
- Run: `ollama run mistral`
- Update `lang_agent` URLs in the code to point to your local Ollama (e.g. `localhost:11434`)

---

## ⚠️ Important: Running This App Locally with Full Functionality

This Streamlit app (`https://finance-assistant-ieywnvvlgvapjvz6msdw3t.streamlit.app/`) is **UI-only** — backend services like voice recognition, LLM summarization, and TTS are not available in the hosted environment.

To run the full assistant locally:

### 🧱 Prerequisites

1. **Install Docker & Docker Compose**
2. **Install Ollama** and run `ollama run mistral`

### 🚀 Start All Services

Clone the repo and run:

docker-compose up --build


<!-- Finance Voice Assistant -->
A modular, multi-agent voice assistant that provides a morning financial market brief using real-time data, document retrieval, and a locally hosted Large Language Model (LLM) via Ollama.

<!-- Project Overview -->
This project demonstrates a containerized, agent-based architecture to answer questions like:

"What’s our risk exposure in Asia tech stocks today, and are there any earnings surprises?"

Using voice input, the system transcribes speech, retrieves data and documents, summarizes them using an LLM, and replies via both text and voice.

<!-- Project Structure -->

finance-voice-assistant/
├── agents/                    # All AI agents & orchestrator
│   ├── api_agent/             # Fetches allocation and earnings data
│   ├── lang_agent/            # LLM-based summarization using Ollama
│   ├── retriever_agent/       # Retrieves relevant documents
│   ├── scraper_agent/         # (Optional) Web scraping agent
│   ├── voice_agent/           # STT & TTS using Whisper & TTS libraries
│   └── orchestrator/          # Manages multi-agent workflow
│
├── streamlit_app/             # Frontend app for voice interaction
├── docs/                      # AI tool usage logs, architecture diagrams, etc.
├── docker-compose.yml         # Container orchestration
├── .env                       # Environment config (if used)
└── README.md                  # Project overview and setup instructions

<!-- Setup & Deployment -->
<!-- Prerequisites -->
Docker & Docker Compose

Python 3.10+ (for manual runs)

Ollama installed locally with the mistral model downloaded:

ollama run mistral

<!-- Run Locally with Docker -->

git clone https://github.com/<your-username>/finance-voice-assistant.git
cd finance-voice-assistant

# Start all containers
docker compose up --build

The Streamlit UI will be available at: http://localhost:8501

<!-- How It Works (Flow) -->
User uploads audio via Streamlit

voice_agent → Transcribes to text

orchestrator → Calls:

api_agent for data

retriever_agent for context

lang_agent (LLM) for summarization

voice_agent → Converts summary to speech

Streamlit → Plays both text & audio response

 <!-- Tools & Frameworks -->
Component	Tool/Library Used
LLM	= mistral via Ollama
STT = 	Whisper (open-source)
TTS	= gTTS.
UI	= Streamlit
Containerization	= Docker + Docker Compose
Agent Routing	= FastAPI


<!-- Deployment Notes -->

this project uses a local Ollama LLM. To run it fully, install Ollama on your machine and download the mistral model before launching.


<!-- LLM Setup (Ollama) -->
This project uses Ollama to run a local LLM (mistral) for cost-free, offline inference.

🛠️ Steps to Run Locally:
Install Ollama
Follow the instructions for your OS: https://ollama.com/download

Start the Mistral Model
Once installed, pull and start the model:
ollama run mistral

Ensure Correct Network Access in Docker
Your lang_agent connects to Ollama via:

llm = ChatOllama(base_url="http://host.docker.internal:11434", model="mistral", temperature=4)

This uses host.docker.internal so that services running inside Docker can access the Ollama server running on your local machine.
If you're not using Docker, change the URL to:
base_url="http://localhost:11434"




