import os
from datetime import date, time, datetime

import requests
import streamlit as st

# Optional auto refresh
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH = True
except Exception:
    AUTO_REFRESH = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OMNI AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_state():

    defaults = {
        "reminders": [],
        "meetings": [],
        "learning": [],
        "tasks": [],
        "wellness": [],
        "expenses": [],
        "communications": [],
        "robotics": [],
        "drones": [],
        "fired_notifications": set(),
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


initialize_state()


# ============================================================
# SAFE DATA FUNCTIONS
# ============================================================

def safe_get(item, key, default="Not specified"):

    if not isinstance(item, dict):
        return default

    value = item.get(key, default)

    if value is None:
        return default

    return value


def safe_date(item, key="due_date"):

    return safe_get(
        item,
        key,
        "Not set"
    )


def safe_time(item, key="due_time"):

    return safe_get(
        item,
        key,
        "Not set"
    )


def notification_enabled(item):

    return bool(
        safe_get(
            item,
            "notification",
            False
        )
    )


# ============================================================
# HEADER / BANNER
# ============================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #111827, #1f2937);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #374151;
    ">

        <div style="
            font-size: 45px;
            font-weight: 700;
            color: white;
        ">
            🤖 OMNI AI
        </div>

        <div style="
            font-size: 25px;
            font-weight: 600;
            color: #d1d5db;
            margin-top: 8px;
        ">
            Omni-Agentic Intelligent Automation System
        </div>

        <div style="
            font-size: 16px;
            color: #9ca3af;
            margin-top: 12px;
        ">
            10 AI Agents • Demo Mode • Grok API Mode
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# AGENTS
# ============================================================

AGENTS = {

    "🧠 AI Orchestrator":
        "Central agent that analyzes requests and routes them.",

    "⏰ Daily Reminder Agent":
        "Reminders, alarms, deadlines and routines.",

    "❤️ Health & Wellness Agent":
        "Wellness routines, fitness activities and appointments.",

    "📅 Calendar & Schedule Agent":
        "Meetings, appointments, classes and events.",

    "📚 Learning & Education Agent":
        "Learning plans, study schedules and educational activities.",

    "📝 Productivity & Task Agent":
        "Tasks, priorities, checklists and project activities.",

    "💰 Finance & Expense Agent":
        "Expenses, budgets, payments and financial organization.",

    "🌐 Information & Communication Agent":
        "Emails, reports, notices, announcements and messages.",

    "🤖 Robotics Agent":
        "Robotics, controllers, sensors, components and automation.",

    "🚁 Drones & Autonomous Systems Agent":
        "Drones, UAVs, autonomous platforms and navigation."
}


# ============================================================
# API KEY
# ============================================================

def get_api_key():

    try:

        key = st.secrets.get(
            "XAI_API_KEY",
            ""
        )

        if key:
            return key

    except Exception:
        pass

    return os.getenv(
        "XAI_API_KEY",
        ""
    )


api_key = get_api_key()


# ============================================================
# GROK API FUNCTION
# ============================================================

def call_grok(
    user_message,
    agent_name
):

    if not api_key:

        raise RuntimeError(
            "XAI_API_KEY is not configured."
        )

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    system_message = (
        "You are the "
        + agent_name
        + " inside OMNI AI, an "
        "Omni-Agentic Intelligent "
        "Automation System. "
        "Provide practical, structured "
        "and concise assistance. "
        "Do not claim that a reminder, "
        "meeting, alarm or external "
        "action was actually created "
        "unless the application has "
        "explicitly performed it."
    )

    payload = {

        "model": "grok-3-mini",

        "messages": [

            {
                "role": "system",
                "content": system_message
            },

            {
                "role": "user",
                "content": user_message
            }
        ],

        "temperature": 0.3
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90
    )

    if response.status_code != 200:

        raise RuntimeError(
            "Grok API Error "
            + str(response.status_code)
            + ": "
            + response.text
        )

    data = response.json()

    return (
        data["choices"][0]["message"]["content"]
    )


# ============================================================
# DEMO AI RESPONSE
# ============================================================

def demo_ai_response(
    agent_name,
    question
):

    responses = {

        "🧠 AI Orchestrator":
            """
### 🧠 Demo Orchestrator

Your request was received.

I would analyze the intent and route
it to the appropriate specialist
agent.

Available specialist areas include:

- Reminders
- Calendar
- Learning
- Tasks
- Wellness
- Finance
- Communication
- Robotics
- Drones
""",

        "⏰ Daily Reminder Agent":
            """
### ⏰ Demo Reminder Assistant

I can help with:

- Alarms
- Reminders
- Due dates
- Due times
- Recurring routines
- Deadlines
- Notification planning

Use the form above to actually create
a reminder in this Demo application.
""",

        "📅 Calendar & Schedule Agent":
            """
### 📅 Demo Calendar Assistant

I can help organize:

- Meetings
- Classes
- Appointments
- Events
- Participants
- Locations
- Meeting notifications

Use the calendar form to create a
demo calendar record.
""",

        "📚 Learning & Education Agent":
            """
### 📚 Demo Learning Assistant

I can help create:

- Study plans
- Python learning plans
- AI learning plans
- Revision schedules
- Course activities
- Daily learning targets
""",

        "📝 Productivity & Task Agent":
            """
### 📝 Demo Productivity Assistant

I can help manage:

- Tasks
- Priorities
- Deadlines
- Checklists
- Project activities
- Productivity routines
""",

        "❤️ Health & Wellness Agent":
            """
### ❤️ Demo Wellness Assistant

I can help organize:

- Exercise
- Walking
- Hydration
- Meditation
- Wellness activities
- Appointments
- Fitness routines

This is organizational assistance,
not medical diagnosis.
""",

        "💰 Finance & Expense Agent":
            """
### 💰 Demo Finance Assistant

I can help organize:

- Expenses
- Categories
- Budgets
- Payment dates
- Financial summaries
- Expense records
""",

        "🌐 Information & Communication Agent":
            """
### 🌐 Demo Communication Assistant

I can create:

- Emails
- Messages
- Reports
- Announcements
- Notices
- Official communication drafts
""",

        "🤖 Robotics Agent":
            """
### 🤖 Demo Robotics Assistant

I can assist with:

- Arduino
- ESP32
- Raspberry Pi
- Controllers
- Sensors
- Components
- Motors
- Actuators
- Communication
- Automation
- Computer vision
""",

        "🚁 Drones & Autonomous Systems Agent":
            """
### 🚁 Demo Autonomous Systems Assistant

I can assist with:

- UAVs
- Drones
- Pixhawk
- ArduPilot
- PX4
- GPS
- IMU
- LiDAR
- Computer vision
- Navigation
- SLAM
- Autonomous missions
"""
    }

    answer = responses.get(
        agent_name,
        "Demo assistant is ready."
    )

    return answer + (
        "\n\n**Your question:**\n\n"
        + question
    )


# ============================================================
# AGENT CHATBOT
# ============================================================

def agent_chatbot(
    agent_name,
    context=""
):

    st.divider()

    st.subheader(
        "💬 " + agent_name + " — AI Assistant"
    )

    st.caption(
        "Ask this specialist agent for assistance."
    )

    key_base = (
        agent_name
        .replace(" ", "_")
        .replace("🤖", "robot")
        .replace("🧠", "orchestrator")
        .replace("⏰", "reminder")
        .replace("❤️", "wellness")
        .replace("📅", "calendar")
        .replace("📚", "learning")
        .replace("📝", "tasks")
        .replace("💰", "finance")
        .replace("🌐", "communication")
        .replace("🚁", "drone")
    )

    history_key = (
        "chat_history_"
        + key_base
    )

    if history_key not in st.session_state:

        st.session_state[history_key] = []

    # Show previous messages
    for message in st.session_state[history_key]:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask "
        + agent_name
        + "...",
        key="chat_input_" + key_base
    )

    if question:

        st.session_state[history_key].append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        if mode == "🎮 Demo Mode":

            answer = demo_ai_response(
                agent_name,
                question
            )

        else:

            if not api_key:

                answer = """
### 🔑 Grok API Key Missing

Grok API Mode is selected but
`XAI_API_KEY` was not found.

Add it in Streamlit Secrets:

```toml
XAI_API_KEY = "YOUR_GROK_API_KEY"
