# 🧠 Incident Memory Agent

AI-powered production incident diagnosis using persistent memory with Hindsight.

## 🚨 The Problem

When a production incident happens, engineers often ask:

> "Have we seen this problem before?"

The answer may already exist in old incident reports, debugging notes, or previous resolutions. But finding that knowledge quickly can be difficult.

A normal AI assistant can suggest a solution, but it does not automatically have access to an organization's history of resolved incidents.

## 💡 The Idea

Incident Memory Agent gives an AI agent persistent memory of previous production incidents.

Instead of starting from zero every time, the system can:

1. Receive a new production incident.
2. Recall relevant historical incidents.
3. Use previous resolutions as evidence.
4. Suggest a diagnosis and recommended action.
5. Accept engineer feedback.
6. Store new resolved incidents for future use.

The goal is simple:

**Turn past incident experience into reusable organizational memory.**

## 🏗️ Architecture

```text
Engineer
   │
   ▼
Streamlit UI
   │
   ▼
FastAPI Backend
   │
   ▼
Hindsight Memory
   │
   ├── Recall relevant incidents
   │
   └── Reflect on historical evidence
   │
   ▼
AI Diagnosis
   │
   ▼
Recommended Action
   │
   ▼
Engineer Feedback
   │
   ▼
New Incident Memory
```

## 🔄 How It Works

### 1. Retain

When an engineer resolves an incident, the incident details are stored in Hindsight.

Each incident contains:

- Symptoms
- Root cause
- Resolution

### 2. Recall

When a new incident arrives, the system searches its historical memory for relevant incidents.

### 3. Diagnose

If relevant historical evidence exists, the system uses it to suggest a likely diagnosis and previously successful resolution.

### 4. New Incident Detection

If no sufficiently relevant historical incident is found, the system does not treat unrelated incidents as evidence.

Instead, it identifies the situation as a **new incident pattern** and recommends investigation using application logs, metrics, and recent changes.

### 5. Engineer Feedback

Engineers can provide feedback on whether a diagnosis was useful. This feedback is stored as additional memory.

## 🧪 Example

### Known Incident

A new incident reports:

```text
API response times are spiking and we're seeing timeouts talking to Redis.
```

The system can recall a previous Redis cache-related incident and use its stored resolution as evidence.

The diagnosis can recommend the previously successful fix, such as adding jitter to cache expiration.

### New Incident

A completely different incident such as:

```text
Users are randomly getting logged out of the application.
```

If there is no sufficiently relevant historical evidence, the system reports that no similar incident was found instead of presenting unrelated incidents as evidence.

This distinction is important because an incident memory system should know when it **doesn't have relevant experience**.

## ✨ Key Features

- Persistent incident memory
- Historical incident recall
- Evidence-based diagnosis
- New incident detection
- Engineer feedback
- Teach-the-agent workflow
- Incident history
- Streamlit dashboard
- FastAPI backend
- Hindsight integration

## 🛠️ Technology Stack

- Python
- FastAPI
- Streamlit
- Hindsight
- Pydantic
- Requests
- Python-dotenv

## 🚀 Running the Project

### 1. Clone the repository

```bash
git clone <https://github.com/trilokapoojitha/incident-memory-agent.git>
cd incident-memory-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Hindsight

Create a `.env` file:

```env
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_api_key_here
```

Never commit the real `.env` file or API key.

### 5. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### 6. Start the Streamlit interface

Open another terminal and run:

```bash
streamlit run app.py
```

## 🔐 Security

The Hindsight API key is stored in `.env` and excluded from Git using `.gitignore`.

Only `.env.example` is included in the repository.

Never publish your real API key.

## 🧠 Why Hindsight?

The important part of this project is not simply generating another AI response.

The system gives the agent access to persistent incident experience.

Instead of asking:

> "What might fix this?"

the workflow becomes:

> "Have we experienced something similar, what happened, and what worked?"

That makes previous engineering experience reusable.

## 🔮 Future Improvements

Possible future improvements include:

- Stronger semantic relevance filtering
- Incident metadata and categorization
- Integration with monitoring and alerting systems
- Authentication and role-based access
- Automated incident ingestion
- Larger evaluation datasets
- Measuring whether incident memory reduces diagnosis time

## 📚 Hindsight

Hindsight is the memory layer used by this project.

- GitHub: https://github.com/vectorize-io/hindsight
- Documentation: https://hindsight.vectorize.io/
- Vectorize Agent Memory: https://vectorize.io/what-is-agent-memory

## 👩‍💻 Project

**Incident Memory Agent**

Built to explore how persistent memory can make AI-assisted incident response more useful by reusing previous engineering experience.
```