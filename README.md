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
