import streamlit as st
import requests
import os
from datetime import datetime, date

# ============================================================
# OMNI AI
# Omni-Agentic Intelligent Automation System
# ============================================================

st.set_page_config(
    page_title="OMNI AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #020617 100%
        );
        color: white;
    }

    /* Hide Streamlit default menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Header */
    .omni-header {
        background: linear-gradient(
            135deg,
            #111827,
            #1e293b
        );

        border: 1px solid #334155;
        border-radius: 18px;

        padding: 30px;
        margin-bottom: 25px;

        text-align: center;

        box-shadow:
            0 10px 35px rgba(0,0,0,0.35);
    }

    .omni-title {
        color: white;
        font-size: 42px;
        font-weight: 800;
        margin: 0;
    }

    .omni-subtitle {
        color: #38bdf8;
        font-size: 22px;
        margin-top: 8px;
        font-weight: 600;
    }

    .omni-description {
        color: #cbd5e1;
        font-size: 16px;
        margin-top: 12px;
    }

    /* Cards */
    .agent-card {
        background: rgba(30,41,59,0.85);
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        min-height: 145px;
    }

    .agent-card h3 {
        color: #38bdf8;
        margin-top: 0;
    }

    .agent-card p {
        color: #cbd5e1;
    }

    /* Metric cards */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }

    .metric-number {
        color: #38bdf8;
        font-size: 30px;
        font-weight: bold;
    }

    .metric-label {
        color: #cbd5e1;
        font-size: 14px;
    }

    /* Status */
    .status-online {
        color: #22c55e;
        font-weight: bold;
    }

    .status-demo {
        color: #f59e0b;
        font-weight: bold;
    }

    /* Footer */
    .omni-footer {
        text-align: center;
        color: #64748b;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #334155;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "reminders" not in st.session_state:
    st.session_state.reminders = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "calendar" not in st.session_state:
    st.session_state.calendar = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# GROK API FUNCTION
# ============================================================

def ask_grok(prompt):

    api_key = None

    try:
        api_key = st.secrets.get("XAI_API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        return (
            "Grok API key is not configured.\n\n"
            "You are currently using OMNI AI Demo Mode."
        )

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-3-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are OMNI AI, an intelligent multi-agent "
                    "automation assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:

            result = response.json()

            return result["choices"][0]["message"]["content"]

        return (
            f"Grok API Error: {response.status_code}\n"
            f"{response.text}"
        )

    except Exception as e:

        return f"Grok connection error: {str(e)}"


# ============================================================
# AGENTS
# ============================================================

agents = {

    "🎯 AI Orchestrator": {
        "description":
            "Understands the user's request and routes it to the appropriate AI capability."
    },

    "⏰ Reminder Agent": {
        "description":
            "Manages reminders, notifications and daily schedules."
    },

    "📅 Calendar Agent": {
        "description":
            "Helps organize meetings, events and important dates."
    },

    "📚 Learning Agent": {
        "description":
            "Supports learning, courses, study planning and knowledge development."
    },

    "✅ Productivity Agent": {
        "description":
            "Manages tasks, priorities and daily productivity."
    },

    "❤️ Wellness Agent": {
        "description":
            "Supports general wellness, routines and healthy lifestyle organization."
    },

    "💰 Finance Agent": {
        "description":
            "Helps organize budgets, expenses and financial planning information."
    },

    "💬 Communication Agent": {
        "description":
            "Helps draft messages, emails and communication content."
    },

    "🤖 Robotics Agent": {
        "description":
            "Supports robotics, automation, sensors and intelligent systems."
    },

    "🚁 Autonomous Systems Agent": {
        "description":
            "Supports drones, autonomous systems and intelligent machine concepts."
    }
}


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="omni-header">

    <div class="omni-title">
        🤖 OMNI AI
    </div>

    <div class="omni-subtitle">
        Omni-Agentic Intelligent Automation System
    </div>

    <div class="omni-description">
        Multi-Agent AI Assistant • Demo Mode • Grok API Mode
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 OMNI AI")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎯 AI Orchestrator",
        "⏰ Reminders",
        "📅 Calendar",
        "📚 Learning",
        "✅ Productivity",
        "❤️ Wellness",
        "💰 Finance",
        "💬 Communication",
        "🤖 Robotics",
        "🚁 Autonomous Systems"
    ]
)

st.sidebar.markdown("---")

mode = st.sidebar.radio(
    "AI Mode",
    [
        "🧪 Demo Mode",
        "⚡ Grok API Mode"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "OMNI AI combines multiple intelligent agents "
    "under one central AI assistant."
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header("🏠 OMNI AI Dashboard")

    st.write(
        "Welcome to OMNI AI — your centralized "
        "multi-agent intelligent automation system."
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">10</div>
            <div class="metric-label">AI Agents</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(st.session_state.tasks)}</div>
            <div class="metric-label">Tasks</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(st.session_state.reminders)}</div>
            <div class="metric-label">Reminders</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        status = "DEMO" if "Demo" in mode else "GROK"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{status}</div>
            <div class="metric-label">AI Mode</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("🧠 Available AI Agents")

    columns = st.columns(2)

    for index, (name, info) in enumerate(agents.items()):

        with columns[index % 2]:

            st.markdown(
                f"""
                <div class="agent-card">

                    <h3>{name}</h3>

                    <p>
                        {info["description"]}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# AI ORCHESTRATOR
# ============================================================

elif page == "🎯 AI Orchestrator":

    st.header("🎯 AI Orchestrator")

    st.write(
        "Enter any request. OMNI AI will process the request "
        "through the central intelligence layer."
    )

    prompt = st.text_area(
        "What would you like OMNI AI to do?",
        placeholder=
        "Example: Create a study plan for Python programming..."
    )

    if st.button("🚀 Run OMNI AI", use_container_width=True):

        if not prompt.strip():

            st.warning("Please enter a request.")

        else:

            if "Demo" in mode:

                response = (
                    "🧪 DEMO MODE\n\n"
                    "Your request has been received by "
                    "the OMNI AI Orchestrator.\n\n"
                    f"Request:\n{prompt}\n\n"
                    "In Grok API Mode, this request can be "
                    "processed by the Grok AI model."
                )

            else:

                with st.spinner("OMNI AI is thinking..."):

                    response = ask_grok(prompt)

            st.markdown("### 🤖 OMNI AI Response")

            st.write(response)


# ============================================================
# REMINDERS
# ============================================================

elif page == "⏰ Reminders":

    st.header("⏰ Reminder Agent")

    reminder = st.text_input(
        "Enter reminder"
    )

    reminder_date = st.date_input(
        "Reminder Date",
        value=date.today()
    )

    if st.button("➕ Add Reminder"):

        if reminder.strip():

            st.session_state.reminders.append(
                {
                    "text": reminder,
                    "date": str(reminder_date)
                }
            )

            st.success("Reminder added successfully.")

    st.subheader("📋 Current Reminders")

    if st.session_state.reminders:

        for item in st.session_state.reminders:

            st.write(
                f"⏰ **{item['text']}** — {item['date']}"
            )

    else:

        st.info("No reminders available.")


# ============================================================
# CALENDAR
# ============================================================

elif page == "📅 Calendar":

    st.header("📅 Calendar Agent")

    event = st.text_input(
        "Event Name"
    )

    event_date = st.date_input(
        "Event Date",
        value=date.today()
    )

    event_time = st.time_input(
        "Event Time"
    )

    if st.button("📅 Add Event"):

        if event.strip():

            st.session_state.calendar.append(
                {
                    "event": event,
                    "date": str(event_date),
                    "time": str(event_time)
                }
            )

            st.success("Event added.")


    st.subheader("📋 Calendar Events")

    for item in st.session_state.calendar:

        st.write(
            f"📅 **{item['event']}** | "
            f"{item['date']} | {item['time']}"
        )


# ============================================================
# LEARNING
# ============================================================

elif page == "📚 Learning":

    st.header("📚 Learning Agent")

    topic = st.text_input(
        "What do you want to learn?"
    )

    level = st.selectbox(
        "Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    if st.button("📚 Generate Learning Plan"):

        if not topic.strip():

            st.warning("Enter a learning topic.")

        else:

            prompt = f"""
Create a learning plan for:

Topic: {topic}
Level: {level}

Include:
1. Fundamentals
2. Practical exercises
3. Projects
4. Recommended learning sequence
5. Assessment
"""

            if "Demo" in mode:

                response = f"""
### 📚 Learning Plan

**Topic:** {topic}

**Level:** {level}

Week 1:
Fundamentals of {topic}

Week 2:
Practical exercises

Week 3:
Mini project

Week 4:
Final project and assessment
"""

            else:

                response = ask_grok(prompt)

            st.write(response)


# ============================================================
# PRODUCTIVITY
# ============================================================

elif page == "✅ Productivity":

    st.header("✅ Productivity Agent")

    task = st.text_input(
        "Enter a task"
    )

    priority = st.selectbox(
        "Priority",
        [
            "High",
            "Medium",
            "Low"
        ]
    )

    if st.button("➕ Add Task"):

        if task.strip():

            st.session_state.tasks.append(
                {
                    "task": task,
                    "priority": priority
                }
            )

            st.success("Task added.")

    st.subheader("📋 Tasks")

    if st.session_state.tasks:

        for index, item in enumerate(
            st.session_state.tasks,
            start=1
        ):

            st.write(
                f"{index}. **{item['task']}** "
                f"— Priority: {item['priority']}"
            )

    else:

        st.info("No tasks available.")


# ============================================================
# WELLNESS
# ============================================================

elif page == "❤️ Wellness":

    st.header("❤️ Wellness Agent")

    st.write(
        "Use this section for general routine "
        "and wellness organization."
    )

    sleep = st.slider(
        "Sleep Hours",
        0,
        12,
        7
    )

    water = st.slider(
        "Water Glasses",
        0,
        15,
        6
    )

    activity = st.slider(
        "Physical Activity (minutes)",
        0,
        180,
        30
    )

    if st.button("📊 Generate Wellness Summary"):

        st.success(
            f"""
Your routine summary:

Sleep: {sleep} hours
Water: {water} glasses
Activity: {activity} minutes

Keep monitoring your daily routine.
"""
        )


# ============================================================
# FINANCE
# ============================================================

elif page == "💰 Finance":

    st.header("💰 Finance Agent")

    income = st.number_input(
        "Monthly Income",
        min_value=0.0
    )

    expenses = st.number_input(
        "Monthly Expenses",
        min_value=0.0
    )

    if st.button("📊 Calculate"):

        balance = income - expenses

        st.metric(
            "Remaining Balance",
            f"{balance:,.2f}"
        )

        if balance >= 0:

            st.success(
                "Income is greater than or equal to expenses."
            )

        else:

            st.warning(
                "Expenses are greater than income."
            )


# ============================================================
# COMMUNICATION
# ============================================================

elif page == "💬 Communication":

    st.header("💬 Communication Agent")

    message_type = st.selectbox(
        "Message Type",
        [
            "Professional Email",
            "Meeting Message",
            "Leave Request",
            "Project Update",
            "General Message"
        ]
    )

    topic = st.text_area(
        "Enter your message topic"
    )

    if st.button("✍️ Generate Message"):

        if not topic.strip():

            st.warning("Enter a topic first.")

        else:

            prompt = f"""
Write a professional {message_type}.

Topic:
{topic}
"""

            if "Demo" in mode:

                response = f"""
Subject: {message_type}

Dear Sir/Madam,

I am writing regarding:

{topic}

Kindly consider the above matter.

Regards,
OMNI AI
"""

            else:

                response = ask_grok(prompt)

            st.text_area(
                "Generated Message",
                response,
                height=250
            )


# ============================================================
# ROBOTICS
# ============================================================

elif page == "🤖 Robotics":

    st.header("🤖 Robotics Agent")

    st.write(
        "Intelligent robotics and automation assistant."
    )

    robotics_question = st.text_area(
        "Ask a robotics question",
        placeholder=
        "Example: Design a simple Arduino obstacle detection system."
    )

    if st.button("🤖 Ask Robotics Agent"):

        if robotics_question.strip():

            if "Demo" in mode:

                response = (
                    "🧪 Demo Robotics Agent\n\n"
                    "Your robotics request has been received.\n\n"
                    f"{robotics_question}"
                )

            else:

                response = ask_grok(
                    robotics_question
                )

            st.write(response)


# ============================================================
# AUTONOMOUS SYSTEMS
# ============================================================

elif page == "🚁 Autonomous Systems":

    st.header("🚁 Autonomous Systems Agent")

    system_type = st.selectbox(
        "System Type",
        [
            "Drone",
            "Autonomous Vehicle",
            "Robot",
            "IoT System",
            "Smart Factory",
            "Other"
        ]
    )

    requirement = st.text_area(
        "Describe your requirement"
    )

    if st.button("🚀 Generate Solution"):

        if not requirement.strip():

            st.warning("Enter your requirement.")

        else:

            prompt = f"""
Design a conceptual autonomous system.

System:
{system_type}

Requirement:
{requirement}

Explain:
1. Architecture
2. Sensors
3. Controller
4. AI
5. Communication
6. Automation
7. Safety considerations
"""

            if "Demo" in mode:

                response = f"""
### 🚁 Autonomous System

System Type:
{system_type}

Requirement:
{requirement}

Suggested Architecture:

Sensors
   ↓
Controller
   ↓
AI Decision Layer
   ↓
Actuators
   ↓
Monitoring System
"""

            else:

                response = ask_grok(prompt)

            st.write(response)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="omni-footer">

    🤖 <b>OMNI AI</b><br>

    Omni-Agentic Intelligent Automation System<br>

    Multi-Agent AI • Streamlit • Grok API

</div>
""", unsafe_allow_html=True)
