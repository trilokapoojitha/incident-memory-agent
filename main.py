import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_API_KEY = os.environ["HINDSIGHT_API_KEY"]
BANK_ID = "incident-agent"
incident_history = []

client = Hindsight(base_url=HINDSIGHT_BASE_URL, api_key=HINDSIGHT_API_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.acreate_bank(
            bank_id=BANK_ID,
            name="Incident Response Agent"
        )
    except Exception as e:
        print(f"Bank setup: {e}")

    yield

    await client.aclose()


app = FastAPI(title="Incident Memory Agent", lifespan=lifespan)


class Incident(BaseModel):
    title: str
    symptoms: str
    root_cause: str
    resolution: str


class Query(BaseModel):
    description: str


@app.post("/incidents")
async def log_incident(incident: Incident):
    """RETAIN: store a resolved incident in memory."""
    content = (
        f"Incident: {incident.title}\n"
        f"Symptoms: {incident.symptoms}\n"
        f"Root cause: {incident.root_cause}\n"
        f"Resolution: {incident.resolution}"
    )
    await client.aretain(
        bank_id=BANK_ID,
        content=content,
        context="incident-log",
        retain_async=False,
    )
    incident_history.append({
        "title": incident.title,
        "symptoms": incident.symptoms,
        "root_cause": incident.root_cause,
        "resolution": incident.resolution
    })
    return {"status": "retained", "title": incident.title}


@app.post("/incidents/diagnose")
async def diagnose(query: Query):

    # Search Hindsight memory
    matches = await client.arecall(
        bank_id=BANK_ID,
        query=query.description
    )

    # --------------------------------------------------
    # SIMPLE RELEVANCE FILTER
    # --------------------------------------------------

    stop_words = {
        "the", "and", "are", "is", "was", "were",
        "a", "an", "to", "of", "in", "on", "for",
        "with", "our", "we", "this", "that", "it",
        "users", "user", "system", "application"
    }

    query_words = {
        word.lower().strip(".,!?")
        for word in query.description.split()
        if len(word) > 3
        and word.lower().strip(".,!?") not in stop_words
    }

    relevant_incidents = []

    for result in matches.results:

        text = result.text

        memory_words = {
            word.lower().strip(".,!?")
            for word in text.split()
            if len(word) > 3
            and word.lower().strip(".,!?") not in stop_words
        }

        # Count meaningful words shared with the new incident
        overlap = query_words.intersection(memory_words)

        if len(overlap) >= 1:
            relevant_incidents.append(text)

    # --------------------------------------------------
    # NO RELEVANT MEMORY FOUND
    # --------------------------------------------------

    if not relevant_incidents:

        return {
            "similar_past_incidents": [],
            "suggested_fix": (
                "🆕 No sufficiently similar historical incident "
                "was found in memory. This appears to be a new "
                "incident pattern. An engineer should investigate "
                "the application logs, metrics, and recent changes "
                "before applying a fix."
            )
        }

    # --------------------------------------------------
    # USE AI REFLECTION ONLY WHEN RELEVANT MEMORY EXISTS
    # --------------------------------------------------

    suggestion = await client.areflect(
        bank_id=BANK_ID,
        query=(
            f"A new incident just came in: '{query.description}'. "
            "Use only relevant historical incidents from memory. "
            "Identify the most likely root cause and recommend "
            "the fix that was previously successful."
        ),
    )

    return {
        "similar_past_incidents": relevant_incidents,
        "suggested_fix": suggestion.text,
    }
class Feedback(BaseModel):
    description: str
    useful: bool


@app.post("/feedback")
async def save_feedback(feedback: Feedback):

    content = (
        f"Engineer feedback for incident: {feedback.description}\n"
        f"Was the diagnosis useful: {feedback.useful}"
    )

    await client.aretain(
        bank_id=BANK_ID,
        content=content,
        context="engineer-feedback",
        retain_async=False,
    )

    return {"status": "feedback_saved"}
@app.get("/incidents/history")
async def get_incident_history():
    return {
        "incidents": incident_history
    }
@app.get("/")
async def root():
    return {"message": "Incident Memory Agent is running. Visit /docs to try it."}