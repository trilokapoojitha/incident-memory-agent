Perfect. 👍 We'll make the README **professional but human**, not like generic AI-generated documentation.

## STEP 4A — Open `README.md`

In VS Code:

1. Look at the **Explorer** on the left.
2. Click **`README.md`**.
3. You will probably see the default GitHub README content.
4. Press **Ctrl + A** inside the README editor.
5. Delete everything.

### Then paste this:

```markdown
# 🧠 Incident Memory Agent

AI-powered production incident diagnosis using persistent memory with Hindsight.

## 🚨 The Problem

When a production incident happens, engineers often ask:

> "Have we seen this problem before?"

The answer may already exist somewhere in old incident reports, debugging notes, or previous resolutions. But finding that knowledge quickly is difficult.

A normal AI assistant can suggest a solution, but it does not automatically have access to an organization's history of resolved incidents.

## 💡 The Idea

**Incident Memory Agent** gives an AI agent persistent memory of previous production incidents.

Instead of starting from zero every time, the system can:

1. Receive a new production incident.
2. Recall relevant historical incidents.
3. Use previous resolutions as evidence.
4. Suggest a diagnosis and recommended action.
5. Accept engineer feedback.
6. Store new resolved incidents for future use.

The goal is simple:

**Turn past incident experience into reusable organizational memory.**

## 🏗️ How It Works

```text
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    │  Engineer Interface  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │    Backend API      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      Hindsight      │
                    │   Incident Memory   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
          Recall past incidents       Reflect on evidence
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   AI Diagnosis      │
                    │ + Recommended Fix   │
                    └──────────┬──────────┘
                               │
                               ▼
                    Engineer Feedback
                               │
                               ▼
                         New Memory
```

## 🔄 Two Main Workflows

### 1. Diagnose an Incident

An engineer enters a new incident such as:

```text
API response times are spiking and we're seeing
timeouts talking to Redis.
```

The system searches its incident memory for relevant historical evidence.

If a similar incident exists, the system can surface the previous incident and its successful resolution.

For example:

```text
Past incident:
Redis cache stampede

Previous resolution:
Add jitter to cache expiration
```

The diagnosis can then use that historical experience instead of providing only a generic response.

### 2. Handle a New Incident

The system should not assume that every incident matches something in memory.

For example:

```text
Users are randomly getting logged out of the application.
```

If there is no sufficiently relevant historical evidence, the system identifies it as a new incident pattern and recommends investigation instead of presenting unrelated incidents as evidence.

This distinction is important:

**No evidence is better than misleading evidence.**

## 🧠 Hindsight Integration

Hindsight provides the persistent memory layer.

When an incident is resolved, the system stores information such as:

- Incident title
- Symptoms
- Root cause
- Resolution

A simplified retention operation looks like:

```python
await client.aretain(
    bank_id=BANK_ID,
    content=content,
    context="incident-log",
    retain_async=False,
)
```

When a new incident arrives, the system recalls relevant memories:

```python
matches = await client.arecall(
    bank_id=BANK_ID,
    query=query.description
)
```

The system can then use the recalled information as historical evidence for diagnosis.

Learn more about Hindsight:

- [Hindsight GitHub](https://github.com/vectorize-io/hindsight)
- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [What is Agent Memory?](https://vectorize.io/what-is-agent-memory)

## ✨ Key Features

### Persistent Incident Memory
Resolved incidents can be stored and reused later.

### Evidence-Based Diagnosis
The system can show historical incidents that support its diagnosis.

### New Incident Detection
If sufficiently relevant historical evidence is unavailable, the system treats the problem as a new incident pattern.

### Teach the Agent
Engineers can add a resolved incident to the system's memory.

### Engineer Feedback
Engineers can indicate whether a diagnosis was useful, allowing feedback to become part of the incident memory.

### Incident History
Previously entered incidents can be viewed through the dashboard.

## 🛠️ Technology Stack

- **Python**
- **FastAPI** — backend API
- **Streamlit** — dashboard interface
- **Hindsight** — persistent agent memory
- **Uvicorn** — FastAPI server
- **Pydantic** — request validation

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/trilokapoojitha/incident-memory-agent.git
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

```text
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_api_key_here
```

Replace the placeholder with your own Hindsight API key.

**Never commit `.env` to GitHub.**

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

### 6. Start the Streamlit dashboard

Open another terminal and run:

```bash
streamlit run app.py
```

## 🧪 Example Demo

A simple demo flow is:

### Before memory

Give the system a production incident without relevant historical evidence.

The system should avoid pretending that an unrelated incident is a match.

### With memory

Store a resolved Redis incident:

```text
Title:
Redis cache stampede

Symptoms:
API latency increased and Redis requests started timing out.

Root cause:
A large number of cache entries expired simultaneously.

Resolution:
Added jitter to cache expiration times.
```

Then diagnose:

```text
API response times are spiking and we're seeing
timeouts talking to Redis.
```

The system can recall the previous incident and surface the earlier resolution.

## 🔐 Security

The Hindsight API key is stored locally in `.env`.

The repository intentionally contains only:

```text
.env.example
```

The real `.env` file is excluded using `.gitignore`.

**Never publish your real API key.**

## 📁 Project Structure

```text
incident-memory-agent/
│
├── app.py              # Streamlit dashboard
├── main.py             # FastAPI backend
├── seed_data.py        # Example incident data
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

## 🎯 What I Learned

The interesting part of this project was not simply generating an AI response.

The bigger challenge was deciding **when the system actually had enough historical evidence to make a useful connection**.

An early version could return unrelated historical incidents for a completely different problem. That made the response look intelligent, but the evidence was misleading.

Adding a relevance check changed the behavior:

```text
Relevant memory found
        ↓
Use historical evidence
        ↓
Suggest diagnosis
```

versus:

```text
No relevant memory
        ↓
Treat as a new incident
        ↓
Ask an engineer to investigate
```

That distinction made the system more trustworthy.

## 🔮 Future Improvements

Possible next improvements include:

- Stronger semantic relevance filtering
- Incident metadata and categorization
- Authentication and role-based access
- Integration with monitoring and incident-management tools
- Larger evaluation datasets
- Measuring whether historical memory actually reduces incident diagnosis time