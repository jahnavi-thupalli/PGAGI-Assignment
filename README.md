# PGAGI Assignment - TalentScout: Intelligent Hiring Assistant

TalentScout is an AI-powered recruitment chatbot designed to streamline the top-of-funnel hiring process for a tech recruitment agency. It acts as an automated first-round interviewer by gathering essential candidate information and conducting a dynamic, context-aware technical screening based on the candidate's specific tech stack, desired position, and years of experience.

### Key Features
* **Stateful Conversation Flow:** Uses a structured state machine to guide the candidate through Information Gathering and Technical Interview phases smoothly.
* **Dynamic Question Generation:** Leverages the Llama 3.1 LLM to generate highly relevant technical questions tailored to the candidate's exact profile.
* **Step-by-Step Interviewing:** Presents technical questions one at a time, waiting for the candidate's response before proceeding.
* **Data Validation:** Ensures data integrity by verifying email and phone number formats before moving forward.
* **Graceful Termination & Persistence:** Recognizes exit keywords (e.g., "quit", "bye") and securely saves the candidate's profile to a local JSON database.

---

## Project Structure
```text
TalentScout-Hiring-Assistant/
├── app.py              # Main Streamlit application and conversation state machine
├── prompts.py          # Centralized LLM system prompts and dynamic prompt generators
├── utils.py            # Helper functions (data validation, JSON saving, exit checks)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for necessary environment variables
└── README.md           # Project documentation
```

---

## Installation and Set Up
**Prerequisites:** Python 3.8+, a Groq API key

1. **Clone the repository:**
   `git clone <your-repository-url>`
   `cd TalentScout-Hiring-Assistant`

2. **Install dependencies:**
   `pip install -r requirements.txt`

3. **Environment Setup:**
   Create a `.env` file in the root directory based on the `.env.example` template:
   `GROQ_API_KEY=your_groq_api_key_here`

5. **Run the Application:**
   `streamlit run app.py`

---

## Usage Guide
1. Launch the Streamlit app in your browser using the local host link or Ngrok URL.
2. The bot will greet you and ask for your details one by one (Name, Email, Phone, Experience, Position, Location).
3. Provide your Tech Stack (e.g., "Python, AWS, React").
4. The bot will instantly generate 3-5 technical questions and ask them sequentially.
5. Answer the questions naturally. 
6. Type an exit keyword like "exit" or "quit" at any time to end the session and save your application data to `candidates.json`.

---

## Technical Details & Architecture
* **Frontend UI:** Streamlit handles the conversational UI and manages `st.session_state` to track the interview phases without losing context.
* **LLM Provider:** Groq Cloud is used for ultra-low latency inference, ensuring a real-time chat experience.
* **Model:** `llama-3.1-8b-instant` for high-quality, fast technical question generation.
* **Data Handling:** Standard Python `json` library for local storage, combined with `validators` and `re` (Regex) modules for data sanitization.

---

## Prompt Design
The intelligence of the assistant relies on structured prompt engineering, housed in `prompts.py`:

1. **System Persona (`SYSTEM_PROMPT`):** Establishes the bot as an "expert technical recruiter" and enforces strict behavioral rules.
2. **Dynamic Context Injection:** The `generate_questions_prompt` dynamically injects the tech stack, years of experience, and desired position to adjust the difficulty and relevance of the technical questions.
3. **Few-Shot Formatting:** To ensure the Streamlit app can accurately parse the LLM's output into an iterable list, the prompt explicitly demands a specific format (starting every line with `Q:`) and forbids conversational filler.

---

## Challenges & Solutions
* **Challenge 1: Managing Conversation Continuity (State Machine)**
  * *Issue:* The chatbot initially struggled to distinguish between gathering basic information and conducting the technical interview, leading to looping fallback prompts.
  * *Solution:* Implemented a strict `st.session_state.step` counter. The app only triggers the LLM API call exactly at Step 6 (after the tech stack is provided) and then shifts the UI logic to iterate through a cached list of questions.
* **Challenge 2: Unpredictable LLM Output Parsing**
  * *Issue:* The LLM occasionally included conversational filler, breaking the one-by-one question delivery system.
  * *Solution:* Refined the prompt formatting constraints and built a robust fallback parser in `app.py` that splits text by the forced `Q:` prefix, or falls back to line-length parsing if the prefix is dropped.

---

## Data Privacy 
In compliance with standard data privacy practices, no API keys are hardcoded into the repository. Candidate data is sanitized, validated, and stored locally in a simulated backend (`candidates.json`) rather than being printed to open console logs.
