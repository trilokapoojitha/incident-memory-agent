import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Incident Memory Agent",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 Incident Memory Agent")

st.subheader("AI-powered Production Incident Diagnosis")

st.success("🟢 AI Incident Response System is Online")

st.caption(
    "Memory-powered incident diagnosis • "
    "Historical evidence • Engineer feedback"
)

st.write(
    "Describe a production incident and the agent will "
    "search its memory for similar past incidents."
)
st.info(
    "🔄 How it works: "
    "New Incident → Recall Past Incidents → AI Diagnosis → "
    "Evidence & Pattern Detection → Engineer Feedback → Learning"
)
# --------------------------------------------------
# NEW INCIDENT / DIAGNOSIS
# --------------------------------------------------

st.divider()

st.header("🚨 Diagnose a New Incident")

example_incident = st.selectbox(
    "Choose an example incident:",
    [
        "Custom incident",
        "Redis timeout / cache problem",
        "Database connection timeout",
        "API latency spike"
    ]
)

if example_incident == "Redis timeout / cache problem":
    default_description = (
        "API response times are spiking and "
        "we're seeing timeouts talking to Redis"
    )

elif example_incident == "Database connection timeout":
    default_description = (
        "Our API is experiencing database "
        "connection timeouts and requests are failing."
    )

elif example_incident == "API latency spike":
    default_description = (
        "The API response time has suddenly increased "
        "and requests are becoming slow."
    )

else:
    default_description = ""

description = st.text_area(
    "Describe the production incident:",
    value=default_description,
    placeholder=(
        "Example: API response times are spiking "
        "and we're seeing timeouts talking to Redis"
    ),
    height=150
)

if st.button("🔍 Diagnose Incident"):

    if description.strip():

        response = requests.post(
            "http://127.0.0.1:8000/incidents/diagnose",
            json={"description": description}
        )

        if response.status_code == 200:

            result = response.json()

            # ------------------------------------------
            # REAL EVIDENCE COUNT
            # ------------------------------------------

            evidence_count = len(
                result["similar_past_incidents"]
            )

            # ------------------------------------------
            # DASHBOARD METRICS
            # ------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🧠 Memory",
                    "Active"
                )

            with col2:
                st.metric(
                    "🔍 Diagnosis",
                    "AI Powered"
                )

            with col3:
                st.metric(
                    "📚 Evidence",
                    evidence_count
                )

            st.success("Diagnosis completed!")

            # ------------------------------------------
            # SIMILAR PAST INCIDENTS
            # ------------------------------------------

            st.subheader("🔍 Similar Past Incidents")

            for incident in result["similar_past_incidents"]:
                st.write("• " + incident)

            # ------------------------------------------
            # EVIDENCE
            # ------------------------------------------

            st.subheader("📚 Evidence")

            st.write(
                f"The diagnosis was based on "
                f"**{evidence_count}** "
                f"similar historical incident records."
            )

            # ------------------------------------------
            # INCIDENT PATTERN
            # ------------------------------------------

            st.subheader("🕵️ Incident Pattern")

            if evidence_count >= 3:

                st.success(
                    "🔁 Recurring incident pattern detected."
                )

                st.write(
                    f"**Why?** The system found "
                    f"**{evidence_count} historical records** "
                    f"with similar symptoms."
                )

                st.write(
                    "This suggests the current incident may "
                    "be related to a previously observed "
                    "production problem."
                )

            elif evidence_count > 0:

                st.info(
                    "🟡 Similar historical incident found."
                )

                st.write(
                    f"**Evidence:** "
                    f"{evidence_count} similar historical "
                    f"record(s)."
                )

                st.write(
                    "The incident has some historical "
                    "similarity, but there is not enough "
                    "evidence to identify a recurring pattern."
                )

            else:

                st.warning(
                    "🆕 No historical pattern found."
                )

                st.write(
                    "No similar incident records were found "
                    "in memory. This may represent a new "
                    "incident pattern."
                )

            # ------------------------------------------
            # INCIDENT CLASSIFICATION
            # ------------------------------------------

            st.divider()

            st.subheader("📌 Incident Classification")

            if evidence_count >= 3:

                st.success(
                    "🟠 KNOWN RECURRING INCIDENT — "
                    "A similar problem has occurred multiple times."
                )

            elif evidence_count > 0:

                st.info(
                    "🟡 KNOWN INCIDENT TYPE — "
                    "A similar historical incident was found."
                )

            else:

                st.warning(
                    "🆕 NEW INCIDENT — "
                    "No similar historical incident was found."
                )

            # ------------------------------------------
            # AI DIAGNOSIS
            # ------------------------------------------

            st.subheader("🧠 AI Diagnosis")

            with st.container(border=True):
                st.write(
                    result["suggested_fix"]
                )

            # ------------------------------------------
            # RECOMMENDED ACTION
            # ------------------------------------------

            st.subheader("💡 Recommended Action")

            st.write(
                "Use the proven resolution from the most "
                "similar past incident."
            )

            # ------------------------------------------
            # ENGINEER FEEDBACK
            # ------------------------------------------

            st.subheader("👨‍💻 Engineer Feedback")

            st.write(
                "Was this diagnosis useful?"
            )

            feedback_col1, feedback_col2 = st.columns(2)

            with feedback_col1:

                if st.button("👍 Yes, helpful"):

                    feedback_response = requests.post(
                        "http://127.0.0.1:8000/feedback",
                        json={
                            "description": description,
                            "useful": True
                        }
                    )

                    if feedback_response.status_code == 200:

                        st.success(
                            "✅ Feedback saved!"
                        )

                    else:

                        st.error(
                            "Could not save feedback."
                        )

            with feedback_col2:

                if st.button("👎 Not helpful"):

                    feedback_response = requests.post(
                        "http://127.0.0.1:8000/feedback",
                        json={
                            "description": description,
                            "useful": False
                        }
                    )

                    if feedback_response.status_code == 200:

                        st.warning(
                            "📝 Feedback saved. "
                            "We'll use this feedback "
                            "to improve the agent."
                        )

                    else:

                        st.error(
                            "Could not save feedback."
                        )

        else:

            st.error(
                "Something went wrong with the backend."
            )

    else:

        st.warning(
            "Please describe an incident first."
        )


# --------------------------------------------------
# TEACH THE AGENT
# --------------------------------------------------

st.divider()

st.header("🧠 Teach the Agent")

st.caption(
    "Add resolved incidents so future engineers "
    "can benefit from past solutions."
)

st.write(
    "Add a resolved production incident so the agent "
    "can remember it and use it for future diagnoses."
)

title = st.text_input(
    "Incident Title"
)

symptoms = st.text_area(
    "Symptoms",
    placeholder="What was happening?"
)

root_cause = st.text_area(
    "Root Cause",
    placeholder="Why did the problem happen?"
)

resolution = st.text_area(
    "Resolution",
    placeholder="How was the problem fixed?"
)

if st.button("💾 Teach Agent"):

    if title and symptoms and root_cause and resolution:

        response = requests.post(
            "http://127.0.0.1:8000/incidents",
            json={
                "title": title,
                "symptoms": symptoms,
                "root_cause": root_cause,
                "resolution": resolution
            }
        )

        if response.status_code == 200:

            st.success(
                "✅ Incident remembered! "
                "The agent can use this knowledge "
                "in future diagnoses."
            )

        else:

            st.error(
                "Something went wrong while saving "
                "the incident."
            )

    else:

        st.warning(
            "Please fill in all the fields."
        )


# --------------------------------------------------
# INCIDENT HISTORY
# --------------------------------------------------

st.divider()

st.header("📜 Incident History")

if st.button("🔄 Load Incident History"):

    response = requests.get(
        "http://127.0.0.1:8000/incidents/history"
    )

    if response.status_code == 200:

        history = response.json()["incidents"]

        if history:

            for incident in reversed(history):

                with st.expander(
                    "🚨 " + incident["title"]
                ):

                    st.write("**Symptoms:**")

                    st.write(
                        incident["symptoms"]
                    )

                    st.write("**Root Cause:**")

                    st.write(
                        incident["root_cause"]
                    )

                    st.write("**Resolution:**")

                    st.write(
                        incident["resolution"]
                    )

        else:

            st.info(
                "No incidents have been added yet."
            )

    else:

        st.error(
            "Could not load incident history."
        )
