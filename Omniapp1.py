import os
import time as pytime
from datetime import date, time, datetime

import requests
import streamlit as st


# ============================================================
# OPTIONAL AUTO REFRESH
# ============================================================

try:
    from streamlit_autorefresh import st_autorefresh

    AUTO_REFRESH_AVAILABLE = True

except Exception:
    AUTO_REFRESH_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OMNI AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

def init_state():

    defaults = {

        "meetings": [],
        "reminders": [],
        "tasks": [],
        "learning": [],
        "wellness": [],
        "expenses": [],
        "communications": [],
        "robotics": [],
        "drones": [],

        "chat_history": [],
        "chat_messages": [],

        "fired_notifications": set(),

        "workflow_running": False,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


init_state()


# ============================================================
# SAFE DATA HELPERS
# ============================================================

def safe_value(item, key, default="Not specified"):

    if not isinstance(item, dict):
        return default

    value = item.get(key, default)

    if value is None:
        return default

    return value


def safe_date(
    item,
    key="due_date",
    default="Not set",
):

    return safe_value(
        item,
        key,
        default,
    )


def safe_time(
    item,
    key="due_time",
    default="Not set",
):

    return safe_value(
        item,
        key,
        default,
    )


def safe_bool(
    item,
    key="notification",
    default=False,
):

    value = safe_value(
        item,
        key,
        default,
    )

    return bool(value)


def delete_item(
    collection_name,
    index,
):

    items = st.session_state.get(
        collection_name,
        [],
    )

    if 0 <= index < len(items):

        items.pop(index)

        st.session_state[
            collection_name
        ] = items

    st.rerun()


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [3, 1],
    vertical_alignment="center",
)

with header_col1:

    st.title("🤖 OMNI AI")

    st.subheader(
        "Omni-Agentic Intelligent Automation System"
    )

    st.caption(
        "Multi-Agent AI • Daily Automation • "
        "Productivity • Robotics • Autonomous Systems"
    )


with header_col2:

    st.metric(
        "AI Agents",
        "10",
    )


st.divider()


# ============================================================
# AGENTS
# ============================================================

AGENTS = {

    "🧠 AI Orchestrator":
        "Routes user requests to the appropriate specialist.",

    "⏰ Daily Reminder Agent":
        "Manages reminders, alarms, deadlines and routines.",

    "❤️ Health & Wellness Agent":
        "Manages wellness activities and appointments.",

    "📅 Calendar & Schedule Agent":
        "Manages meetings, classes, appointments and events.",

    "📚 Learning & Education Agent":
        "Creates study plans and learning activities.",

    "📝 Productivity & Task Agent":
        "Manages tasks, priorities and checklists.",

    "💰 Finance & Expense Agent":
        "Organizes expenses, budgets and payment reminders.",

    "🌐 Information & Communication Agent":
        "Creates emails, reports, announcements and messages.",

    "🤖 Robotics Agent":
        "Supports robotics, controllers, sensors and automation.",

    "🚁 Drones & Autonomous Systems Agent":
        "Supports UAVs, navigation and autonomous systems.",
}


# ============================================================
# AGENT ALIASES
# ============================================================

AGENT_ALIASES = {

    "orchestrator":
        "🧠 AI Orchestrator",

    "master":
        "🧠 AI Orchestrator",

    "ai":
        "🧠 AI Orchestrator",

    "reminder":
        "⏰ Daily Reminder Agent",

    "reminders":
        "⏰ Daily Reminder Agent",

    "alarm":
        "⏰ Daily Reminder Agent",

    "health":
        "❤️ Health & Wellness Agent",

    "wellness":
        "❤️ Health & Wellness Agent",

    "fitness":
        "❤️ Health & Wellness Agent",

    "calendar":
        "📅 Calendar & Schedule Agent",

    "schedule":
        "📅 Calendar & Schedule Agent",

    "meeting":
        "📅 Calendar & Schedule Agent",

    "meetings":
        "📅 Calendar & Schedule Agent",

    "learning":
        "📚 Learning & Education Agent",

    "education":
        "📚 Learning & Education Agent",

    "study":
        "📚 Learning & Education Agent",

    "task":
        "📝 Productivity & Task Agent",

    "tasks":
        "📝 Productivity & Task Agent",

    "productivity":
        "📝 Productivity & Task Agent",

    "finance":
        "💰 Finance & Expense Agent",

    "expense":
        "💰 Finance & Expense Agent",

    "expenses":
        "💰 Finance & Expense Agent",

    "communication":
        "🌐 Information & Communication Agent",

    "communications":
        "🌐 Information & Communication Agent",

    "email":
        "🌐 Information & Communication Agent",

    "message":
        "🌐 Information & Communication Agent",

    "robotics":
        "🤖 Robotics Agent",

    "robot":
        "🤖 Robotics Agent",

    "arduino":
        "🤖 Robotics Agent",

    "esp32":
        "🤖 Robotics Agent",

    "raspberry":
        "🤖 Robotics Agent",

    "drone":
        "🚁 Drones & Autonomous Systems Agent",

    "drones":
        "🚁 Drones & Autonomous Systems Agent",

    "uav":
        "🚁 Drones & Autonomous Systems Agent",

    "autonomous":
        "🚁 Drones & Autonomous Systems Agent",

}


# ============================================================
# EXPLICIT AGENT DETECTION
# ============================================================

def detect_explicit_agent(request):

    if not request:
        return None

    text = request.lower().strip()

    for alias, agent in AGENT_ALIASES.items():

        if (
            f"@{alias}" in text
            or text.startswith(alias + " ")
            or text.startswith(alias + ":")
        ):

            return agent

    return None


# ============================================================
# AGENT DETECTION
# ============================================================

def detect_agent(request):

    explicit_agent = detect_explicit_agent(
        request
    )

    if explicit_agent:

        return explicit_agent

    text = request.lower()

    rules = [

        (
            [
                "reminder",
                "alarm",
                "remind",
                "deadline",
            ],
            "⏰ Daily Reminder Agent",
        ),

        (
            [
                "health",
                "wellness",
                "fitness",
                "exercise",
                "workout",
                "hydration",
                "meditation",
            ],
            "❤️ Health & Wellness Agent",
        ),

        (
            [
                "calendar",
                "meeting",
                "meet",
                "schedule",
                "appointment",
                "event",
                "class",
            ],
            "📅 Calendar & Schedule Agent",
        ),

        (
            [
                "learn",
                "learning",
                "study",
                "education",
                "course",
                "python",
                "exam",
            ],
            "📚 Learning & Education Agent",
        ),

        (
            [
                "task",
                "todo",
                "to-do",
                "productivity",
                "checklist",
            ],
            "📝 Productivity & Task Agent",
        ),

        (
            [
                "expense",
                "finance",
                "budget",
                "money",
                "payment",
                "spending",
                "bill",
            ],
            "💰 Finance & Expense Agent",
        ),

        (
            [
                "email",
                "message",
                "announcement",
                "report",
                "letter",
                "notice",
            ],
            "🌐 Information & Communication Agent",
        ),

        (
            [
                "robot",
                "robotics",
                "arduino",
                "esp32",
                "esp8266",
                "raspberry",
                "sensor",
                "motor",
                "embedded",
                "plc",
            ],
            "🤖 Robotics Agent",
        ),

        (
            [
                "drone",
                "drones",
                "uav",
                "autonomous",
                "navigation",
                "quadcopter",
                "flight",
                "pixhawk",
                "ardupilot",
                "px4",
            ],
            "🚁 Drones & Autonomous Systems Agent",
        ),

    ]

    for keywords, agent in rules:

        if any(
            word in text
            for word in keywords
        ):

            return agent

    return "🧠 AI Orchestrator"


# ============================================================
# NOTIFICATION SYSTEM
# ============================================================

def notification_id(
    category,
    title,
    due_date,
    due_time,
):

    return (
        f"{category}|"
        f"{title}|"
        f"{due_date}|"
        f"{due_time}"
    )


def browser_notification(message):

    text = (
        str(message)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    st.components.v1.html(
        f"""
        <script>

        try {{

            if ("Notification" in window) {{

                if (
                    Notification.permission
                    === "default"
                ) {{

                    Notification.requestPermission();

                }}

                if (
                    Notification.permission
                    === "granted"
                ) {{

                    new Notification(
                        "🤖 OMNI AI Reminder",
                        {{
                            body: '{text}'
                        }}
                    );

                }}

            }}

        }} catch (e) {{}}

        </script>
        """,
        height=0,
    )


def check_items(
    items,
    category,
    title_key,
    date_key,
    time_key,
    icon,
    notifications,
):

    now = datetime.now()

    today = now.date()

    current_time = now.time().replace(
        second=0,
        microsecond=0,
    )

    for item in items:

        if not isinstance(item, dict):
            continue

        if not safe_bool(
            item,
            "notification",
            False,
        ):
            continue

        item_date = safe_value(
            item,
            date_key,
            None,
        )

        item_time = safe_value(
            item,
            time_key,
            None,
        )

        title = str(
            safe_value(
                item,
                title_key,
                category,
            )
        )

        if (
            item_date is None
            or item_time is None
        ):
            continue

        try:

            if (
                item_date == today
                and item_time <= current_time
            ):

                nid = notification_id(
                    category,
                    title,
                    item_date,
                    item_time,
                )

                if (
                    nid
                    not in st.session_state
                    .fired_notifications
                ):

                    st.session_state \
                        .fired_notifications \
                        .add(nid)

                    notifications.append(
                        f"{icon} {title} is due now."
                    )

        except Exception:

            continue


def run_notification_engine():

    notifications = []

    check_items(
        st.session_state.reminders,
        "Reminder",
        "title",
        "due_date",
        "due_time",
        "⏰",
        notifications,
    )

    check_items(
        st.session_state.meetings,
        "Meeting",
        "title",
        "date",
        "time",
        "📅",
        notifications,
    )

    check_items(
        st.session_state.tasks,
        "Task",
        "task",
        "due_date",
        "due_time",
        "📝",
        notifications,
    )

    check_items(
        st.session_state.learning,
        "Learning",
        "subject",
        "due_date",
        "due_time",
        "📚",
        notifications,
    )

    check_items(
        st.session_state.wellness,
        "Wellness",
        "activity",
        "due_date",
        "due_time",
        "❤️",
        notifications,
    )

    check_items(
        st.session_state.expenses,
        "Finance",
        "description",
        "due_date",
        "due_time",
        "💰",
        notifications,
    )

    check_items(
        st.session_state.communications,
        "Communication",
        "subject",
        "due_date",
        "due_time",
        "🌐",
        notifications,
    )

    check_items(
        st.session_state.robotics,
        "Robotics",
        "project",
        "due_date",
        "due_time",
        "🤖",
        notifications,
    )

    check_items(
        st.session_state.drones,
        "Drone",
        "project",
        "due_date",
        "due_time",
        "🚁",
        notifications,
    )

    for message in notifications:

        st.toast(
            message,
            icon="🔔",
        )

        browser_notification(
            message
        )

    if notifications:

        st.warning(
            "🔔 **OMNI AI NOTIFICATION**\n\n"
            + "\n\n".join(
                f"- {message}"
                for message in notifications
            )
        )


# ============================================================
# AUTO REFRESH
# ============================================================

if AUTO_REFRESH_AVAILABLE:

    st_autorefresh(
        interval=15000,
        key="omni_refresh",
    )


run_notification_engine()


# ============================================================
# GROK API
# ============================================================

def get_api_key():

    try:

        secret_key = st.secrets.get(
            "XAI_API_KEY",
            "",
        )

        if secret_key:

            return secret_key

    except Exception:

        pass

    return os.getenv(
        "XAI_API_KEY",
        "",
    )


def call_grok(
    request,
    agent,
    api_key,
):

    url = (
        "https://api.x.ai/v1/chat/completions"
    )

    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json",

    }

    payload = {

        "model":
            "grok-3-mini",

        "messages": [

            {
                "role":
                    "system",

                "content": (
                    "You are OMNI AI, a "
                    "multi-agent intelligent "
                    "assistant. "
                    "The selected specialist "
                    "is "
                    f"{agent}. "
                    "Provide practical, "
                    "structured, safe and "
                    "useful responses. "
                    "Explain actions clearly. "
                    "If the request belongs "
                    "to another specialist, "
                    "mention the appropriate "
                    "agent."
                ),
            },

            {
                "role":
                    "user",

                "content":
                    request,
            },

        ],

        "temperature":
            0.3,

    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90,
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Grok API Error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    try:

        return (
            data[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )

    except (
        KeyError,
        IndexError,
        TypeError,
    ):

        raise RuntimeError(
            "Unexpected response received "
            "from Grok API."
        )


# ============================================================
# DEMO RESPONSE
# ============================================================

def demo_response(
    request,
    agent,
):

    descriptions = {

        "⏰ Daily Reminder Agent":
            "Demo reminder/alarm workflow selected.",

        "❤️ Health & Wellness Agent":
            "Demo wellness workflow selected.",

        "📅 Calendar & Schedule Agent":
            "Demo calendar workflow selected.",

        "📚 Learning & Education Agent":
            "Demo learning workflow selected.",

        "📝 Productivity & Task Agent":
            "Demo productivity workflow selected.",

        "💰 Finance & Expense Agent":
            "Demo finance workflow selected.",

        "🌐 Information & Communication Agent":
            "Demo communication workflow selected.",

        "🤖 Robotics Agent":
            "Demo robotics workflow selected.",

        "🚁 Drones & Autonomous Systems Agent":
            "Demo autonomous-system workflow selected.",

        "🧠 AI Orchestrator":
            "Demo orchestration workflow selected.",
    }

    return f"""
## {agent}

**Request:**

{request}

### Demo Processing

1. Request received
2. Intent analyzed
3. Specialist agent selected
4. Agent workflow executed
5. Structured response generated

### Demo Result

{descriptions.get(
    agent,
    "Demo workflow completed."
)}

🟢 **Agent Status: Active**
"""


# ============================================================
# AGENT COMMUNICATION ENGINE
# ============================================================

def agent_communication(
    request,
    selected_agent,
):

    return [

        {
            "agent":
                "🧠 AI Orchestrator",

            "message":
                "Request received. "
                "Analyzing user intent.",

            "status":
                "completed",
        },

        {
            "agent":
                "🧠 AI Orchestrator",

            "message":
                f"Intent matched to "
                f"{selected_agent}.",

            "status":
                "completed",
        },

        {
            "agent":
                selected_agent,

            "message":
                "Specialist agent activated "
                "and request received.",

            "status":
                "completed",
        },

        {
            "agent":
                selected_agent,

            "message":
                "Specialist agent is analyzing "
                "the task and preparing an action.",

            "status":
                "completed",
        },

        {
            "agent":
                selected_agent,

            "message":
                "Specialist result generated "
                "and sent back to Orchestrator.",

            "status":
                "completed",
        },

        {
            "agent":
                "🧠 AI Orchestrator",

            "message":
                "Orchestrator validated the "
                "specialist response.",

            "status":
                "completed",
        },

        {
            "agent":
                "👤 User",

            "message":
                "Final response delivered.",

            "status":
                "completed",
        },

    ]


# ============================================================
# PLAY AGENTIC WORKFLOW
# ============================================================

def show_agent_workflow(
    request,
    selected_agent,
):

    st.subheader(
        "🔄 Live Agentic Workflow"
    )

    st.caption(
        "This demonstration shows how the "
        "AI Orchestrator communicates with "
        "a specialist agent."
    )

    workflow = agent_communication(
        request,
        selected_agent,
    )

    progress = st.progress(0)

    status_placeholder = st.empty()

    for index, step in enumerate(
        workflow
    ):

        percentage = int(
            (
                (index + 1)
                / len(workflow)
            )
            * 100
        )

        progress.progress(
            percentage
        )

        status_placeholder.info(
            f"⚙️ Processing Stage "
            f"{index + 1}/"
            f"{len(workflow)}"
        )

        if index == 0:

            icon = "🧠"

        elif index == 1:

            icon = "📡"

        elif index == 2:

            icon = "🤖"

        elif index == 3:

            icon = "⚙️"

        elif index == 4:

            icon = "📤"

        elif index == 5:

            icon = "🧠"

        else:

            icon = "👤"

        st.info(
            f"{icon} **{step['agent']}**\n\n"
            f"{step['message']}"
        )

        pytime.sleep(0.6)

    status_placeholder.success(
        "✅ Agentic workflow completed."
    )

    st.success(
        "🟢 Orchestrator successfully "
        "communicated with the specialist agent."
    )


# ============================================================
# CHATBOT DEMO RESPONSE
# ============================================================

def chatbot_demo_response(
    request,
    agent,
):

    responses = {

        "🧠 AI Orchestrator":
            (
                "I analyzed your request and "
                "routed it to the appropriate "
                "specialist agent."
            ),

        "⏰ Daily Reminder Agent":
            (
                "I can manage reminders, "
                "alarms, deadlines and "
                "recurring routines."
            ),

        "❤️ Health & Wellness Agent":
            (
                "I can organize wellness "
                "activities, exercise, "
                "hydration and appointments."
            ),

        "📅 Calendar & Schedule Agent":
            (
                "I can manage meetings, "
                "appointments, classes "
                "and scheduled events."
            ),

        "📚 Learning & Education Agent":
            (
                "I can create study plans, "
                "learning activities and "
                "educational schedules."
            ),

        "📝 Productivity & Task Agent":
            (
                "I can organize tasks, "
                "priorities, deadlines "
                "and checklists."
            ),

        "💰 Finance & Expense Agent":
            (
                "I can organize expenses, "
                "payment schedules, "
                "categories and reminders."
            ),

        "🌐 Information & Communication Agent":
            (
                "I can prepare emails, "
                "announcements, reports, "
                "notices and messages."
            ),

        "🤖 Robotics Agent":
            (
                "I can assist with Arduino, "
                "ESP32, Raspberry Pi, sensors, "
                "motors and robotics projects."
            ),

        "🚁 Drones & Autonomous Systems Agent":
            (
                "I can assist with UAVs, "
                "autonomous platforms, "
                "navigation and mission planning."
            ),
    }

    return f"""
## 🤖 {agent}

**Your Request**

> {request}

### Specialist Response

{responses.get(
    agent,
    "The specialist agent has processed "
    "your request."
)}

### Agentic Routing

```text
User
  ↓
🧠 AI Orchestrator
  ↓
{agent}
  ↓
Specialist Processing
  ↓
Response
