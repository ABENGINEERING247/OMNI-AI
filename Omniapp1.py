import os
import requests
from datetime import datetime, date, time, timedelta

import streamlit as st
import streamlit.components.v1 as components

try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False


# ==========================================================
# OMNI AI
# Omni-Agentic Intelligent Automation System
# ==========================================================

st.set_page_config(
    page_title="OMNI AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_STATE = {
    "meetings": [],
    "reminders": [],
    "tasks": [],
    "expenses": [],
    "learning": [],
    "wellness": [],
    "communications": [],
    "robotics": [],
    "drones": [],
    "chat_history": [],
    "fired_notifications": set()
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        if isinstance(value, list):
            st.session_state[key] = []
        elif isinstance(value, set):
            st.session_state[key] = set()


# ==========================================================
# AUTO REFRESH
# ==========================================================

if AUTO_REFRESH_AVAILABLE:
    st_autorefresh(
        interval=15000,
        key="omni_auto_refresh"
    )


# ==========================================================
# AGENT DEFINITIONS
# ==========================================================

AGENTS = {
    "⏰ Daily Reminder Agent":
        "Reminders, alarms, deadlines and recurring routines.",

    "❤️ Health & Wellness Agent":
        "Wellness activities, fitness, appointments and routines.",

    "📅 Calendar & Schedule Agent":
        "Meetings, classes, appointments and events.",

    "📚 Learning & Education Agent":
        "Courses, study plans, learning activities and revision.",

    "📝 Productivity & Task Management Agent":
        "Tasks, priorities, projects and checklists.",

    "💰 Finance & Expense Management Agent":
        "Expenses, budgets, payments and financial organization.",

    "🌐 Information & Communication Agent":
        "Emails, messages, announcements and reports.",

    "🤖 Robotics Agent":
        "Robotics, embedded systems, sensors and automation.",

    "🚁 Drones & Autonomous Systems Agent":
        "UAVs, drones, navigation and autonomous systems."
}


# ==========================================================
# HEADER
# ==========================================================

st.title("🤖 OMNI AI")

st.subheader(
    "Omni-Agentic Intelligent Automation System"
)

st.write(
    "Grok-Powered Multi-Agent Intelligent Assistant"
)

st.caption(
    "10 AI Agents  •  Demo Mode  •  Grok API Mode  •  "
    "Calendar  •  Reminders  •  Tasks  •  Notifications"
)

st.divider()


# ==========================================================
# NOTIFICATION HELPERS
# ==========================================================

def notification_key(category, title, due_date, due_time):
    return (
        category
        + "|"
        + str(title)
        + "|"
        + str(due_date)
        + "|"
        + str(due_time)
    )


def browser_notification(message):
    safe_message = (
        str(message)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    components.html(
        """
        <script>
        try {
            if ("Notification" in window) {

                if (Notification.permission === "default") {
                    Notification.requestPermission();
                }

                if (Notification.permission === "granted") {
                    new Notification(
                        "OMNI AI Reminder",
                        {
                            body: '"""
        + safe_message
        + """',
                            icon:
                            "https://streamlit.io/images/brand/streamlit-mark-color.png"
                        }
                    );
                }
            }
        } catch (e) {
            console.log(e);
        }
        </script>
        """,
        height=0
    )


def add_notification(
    notifications,
    category,
    title,
    due_date,
    due_time,
    icon
):

    key = notification_key(
        category,
        title,
        due_date,
        due_time
    )

    if key not in st.session_state.fired_notifications:

        message = (
            icon
            + " "
            + str(title)
            + " is due now."
        )

        notifications.append(message)

        st.session_state.fired_notifications.add(key)


# ==========================================================
# NOTIFICATION ENGINE
# ==========================================================

def notification_engine():

    now = datetime.now()

    current_date = now.date()

    current_time = now.time().replace(
        second=0,
        microsecond=0
    )

    notifications = []

    # ------------------------------------------------------
    # REMINDERS
    # ------------------------------------------------------

    for item in st.session_state.reminders:

        if not item.get("notification", True):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Reminder",
                    item.get("title", "Reminder"),
                    due_date,
                    due_time,
                    "⏰"
                )

    # ------------------------------------------------------
    # MEETINGS
    # ------------------------------------------------------

    for item in st.session_state.meetings:

        if not item.get("notification", True):
            continue

        due_date = item.get("date")
        due_time = item.get("time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Meeting",
                    item.get("title", "Meeting"),
                    due_date,
                    due_time,
                    "📅"
                )

    # ------------------------------------------------------
    # TASKS
    # ------------------------------------------------------

    for item in st.session_state.tasks:

        if item.get("completed", False):
            continue

        if not item.get("notification", True):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Task",
                    item.get("task", "Task"),
                    due_date,
                    due_time,
                    "📝"
                )

    # ------------------------------------------------------
    # LEARNING
    # ------------------------------------------------------

    for item in st.session_state.learning:

        if not item.get("notification", True):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Learning",
                    item.get("subject", "Learning Activity"),
                    due_date,
                    due_time,
                    "📚"
                )

    # ------------------------------------------------------
    # WELLNESS
    # ------------------------------------------------------

    for item in st.session_state.wellness:

        if not item.get("notification", True):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Wellness",
                    item.get("activity", "Wellness Activity"),
                    due_date,
                    due_time,
                    "❤️"
                )

    # ------------------------------------------------------
    # FINANCE
    # ------------------------------------------------------

    for item in st.session_state.expenses:

        if not item.get("notification", False):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Finance",
                    item.get("description", "Payment"),
                    due_date,
                    due_time,
                    "💰"
                )

    # ------------------------------------------------------
    # COMMUNICATION
    # ------------------------------------------------------

    for item in st.session_state.communications:

        if not item.get("notification", False):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Communication",
                    item.get("subject", "Communication"),
                    due_date,
                    due_time,
                    "🌐"
                )

    # ------------------------------------------------------
    # ROBOTICS
    # ------------------------------------------------------

    for item in st.session_state.robotics:

        if not item.get("notification", False):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Robotics",
                    item.get("project", "Robotics Project"),
                    due_date,
                    due_time,
                    "🤖"
                )

    # ------------------------------------------------------
    # DRONES
    # ------------------------------------------------------

    for item in st.session_state.drones:

        if not item.get("notification", False):
            continue

        due_date = item.get("due_date")
        due_time = item.get("due_time")

        if due_date == current_date:

            if due_time and due_time <= current_time:

                add_notification(
                    notifications,
                    "Drone",
                    item.get("project", "Drone Mission"),
                    due_date,
                    due_time,
                    "🚁"
                )

    # ------------------------------------------------------
    # DISPLAY
    # ------------------------------------------------------

    if notifications:

        for message in notifications:

            st.toast(
                message,
                icon="🔔"
            )

            browser_notification(message)

        st.warning(
            "🔔 OMNI AI NOTIFICATION\n\n"
            + "\n\n".join(
                "- " + x
                for x in notifications
            )
        )


# ==========================================================
# AGENT DETECTION
# ==========================================================

def detect_agent(request):

    text = request.lower()

    if any(x in text for x in [
        "reminder",
        "remind",
        "alarm",
        "deadline"
    ]):
        return "⏰ Daily Reminder Agent"

    if any(x in text for x in [
        "health",
        "fitness",
        "wellness",
        "exercise",
        "workout"
    ]):
        return "❤️ Health & Wellness Agent"

    if any(x in text for x in [
        "calendar",
        "meeting",
        "schedule",
        "appointment",
        "event",
        "class"
    ]):
        return "📅 Calendar & Schedule Agent"

    if any(x in text for x in [
        "learn",
        "learning",
        "study",
        "education",
        "python",
        "course",
        "exam",
        "revision",
        "training"
    ]):
        return "📚 Learning & Education Agent"

    if any(x in text for x in [
        "task",
        "todo",
        "to-do",
        "project",
        "productivity",
        "checklist",
        "priority"
    ]):
        return "📝 Productivity & Task Management Agent"

    if any(x in text for x in [
        "expense",
        "expenses",
        "budget",
        "finance",
        "money",
        "spending",
        "payment",
        "cost"
    ]):
        return "💰 Finance & Expense Management Agent"

    if any(x in text for x in [
        "email",
        "message",
        "announcement",
        "report",
        "letter",
        "communication"
    ]):
        return "🌐 Information & Communication Agent"

    if any(x in text for x in [
        "robot",
        "robotics",
        "arduino",
        "esp32",
        "raspberry pi",
        "sensor",
        "motor",
        "embedded"
    ]):
        return "🤖 Robotics Agent"

    if any(x in text for x in [
        "drone",
        "uav",
        "autonomous",
        "navigation",
        "quadcopter",
        "flight"
    ]):
        return "🚁 Drones & Autonomous Systems Agent"

    return "🧠 AI Orchestrator"


# ==========================================================
# DEMO AI RESPONSE
# ==========================================================

def demo_response(request, agent):

    if agent == "⏰ Daily Reminder Agent":

        return (
            "## ⏰ Daily Reminder Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Workflow\n\n"
            + "Request → Analyze → Set Due Date/Time → "
            + "Notification → Review\n\n"
            + "✅ Demo reminder processing completed."
        )

    if agent == "❤️ Health & Wellness Agent":

        return (
            "## ❤️ Health & Wellness Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Wellness Plan\n\n"
            + "- Exercise\n"
            + "- Hydration\n"
            + "- Rest\n"
            + "- Wellness activity\n"
            + "- Appointment reminder\n\n"
            + "✅ Demo wellness processing completed.\n\n"
            + "General wellness organization only."
        )

    if agent == "📅 Calendar & Schedule Agent":

        return (
            "## 📅 Calendar & Schedule Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Workflow\n\n"
            + "Create Event → Date → Time → "
            + "Participants → Notification\n\n"
            + "✅ Demo calendar processing completed."
        )

    if agent == "📚 Learning & Education Agent":

        return (
            "## 📚 Learning & Education Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Learning Roadmap\n\n"
            + "1. Fundamentals\n"
            + "2. Practical Exercises\n"
            + "3. Mini Project\n"
            + "4. Advanced Concepts\n"
            + "5. Final Project\n"
            + "6. Review\n\n"
            + "Each learning activity can have a due date, "
            + "due time and notification.\n\n"
            + "✅ Demo learning processing completed."
        )

    if agent == "📝 Productivity & Task Management Agent":

        return (
            "## 📝 Productivity & Task Management Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Workflow\n\n"
            + "Task → Priority → Due Date → Due Time → "
            + "Notification → Completion\n\n"
            + "✅ Demo productivity processing completed."
        )

    if agent == "💰 Finance & Expense Management Agent":

        return (
            "## 💰 Finance & Expense Management Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Capabilities\n\n"
            + "- Record expense\n"
            + "- Categorize expense\n"
            + "- Track payment date\n"
            + "- Set payment time\n"
            + "- Generate total\n"
            + "- Payment notification\n\n"
            + "⚠️ Demo financial data only.\n\n"
            + "✅ Demo finance processing completed."
        )

    if agent == "🌐 Information & Communication Agent":

        return (
            "## 🌐 Information & Communication Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Workflow\n\n"
            + "Understand → Draft → Review → Schedule → Notify\n\n"
            + "Example output:\n\n"
            + "Dear Team,\n\n"
            + "This is an OMNI AI demonstration message.\n\n"
            + "Regards,\n"
            + "OMNI AI\n\n"
            + "✅ Demo communication processing completed."
        )

    if agent == "🤖 Robotics Agent":

        return (
            "## 🤖 Robotics Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Architecture\n\n"
            + "Sensors\n"
            + "↓\n"
            + "ESP32 / Arduino / Raspberry Pi\n"
            + "↓\n"
            + "AI Processing\n"
            + "↓\n"
            + "Decision Making\n"
            + "↓\n"
            + "Motor Controller\n"
            + "↓\n"
            + "Actuators\n\n"
            + "Project reviews and maintenance can have "
            + "due dates and notifications.\n\n"
            + "✅ Demo robotics processing completed."
        )

    if agent == "🚁 Drones & Autonomous Systems Agent":

        return (
            "## 🚁 Drones & Autonomous Systems Agent\n\n"
            + "**Request:** "
            + request
            + "\n\n"
            + "### Demo Architecture\n\n"
            + "Sensors / Camera\n"
            + "↓\n"
            + "Computer Vision\n"
            + "↓\n"
            + "AI Decision\n"
            + "↓\n"
            + "Navigation\n"
            + "↓\n"
            + "Flight Controller\n"
            + "↓\n"
            + "Actuators\n\n"
            + "Mission schedules can include due dates, "
            + "times and notifications.\n\n"
            + "✅ Demo autonomous-system processing completed."
        )

    return (
        "## 🧠 AI Orchestrator\n\n"
        + "**Request:** "
        + request
        + "\n\n"
        + "Request analyzed and routed to: "
        + agent
        + "\n\n"
        + "✅ Demo orchestration completed."
    )


# ==========================================================
# GROK API
# ==========================================================

def grok_response(request, agent, api_key):

    url = "https://api.x.ai/v1/chat/completions"

    system_prompt = (
        "You are OMNI AI, an intelligent multi-agent "
        "automation platform.\n\n"
        "Selected agent: "
        + agent
        + "\n\n"
        "Provide practical and structured answers. "
        "Use headings, lists and tables when useful. "
        "Do not claim that a real-world action was completed "
        "unless an actual integration exists."
    )

    payload = {
        "model": "grok-3-mini",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": request
            }
        ],
        "temperature": 0.3
    }

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90
    )

    if response.status_code == 403:

        raise Exception(
            "Grok API access is currently unavailable. "
            "Your xAI team may have exhausted available "
            "credits or reached its spending limit. "
            "Check xAI billing/usage or use Demo Mode."
        )

    if response.status_code != 200:

        raise Exception(
            "Grok API Error "
            + str(response.status_code)
            + ": "
            + response.text
        )

    data = response.json()

    return data["choices"][0]["message"]["content"]


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🤖 OMNI AI")

    st.caption("Agent Navigation")

    st.divider()

    navigation = [
        "🏠 Dashboard",
        "🧠 AI Orchestrator",
        "⏰ Reminders & Alarms",
        "📅 Calendar & Meetings",
        "📚 Learning",
        "📝 Tasks & Productivity",
        "❤️ Wellness",
        "💰 Finance",
        "🌐 Communication",
        "🤖 Robotics",
        "🚁 Drones & Autonomous"
    ]

    selected = st.radio(
        "Select Module",
        navigation
    )

    st.divider()

    st.subheader("⚙️ Operating Mode")

    mode = st.radio(
        "Mode",
        [
            "🎮 Demo Mode",
            "🔑 Grok API Mode"
        ]
    )

    st.divider()

    st.subheader("📊 System Statistics")

    st.write(
        "📅 Meetings:",
        len(st.session_state.meetings)
    )

    st.write(
        "⏰ Reminders:",
        len(st.session_state.reminders)
    )

    st.write(
        "📝 Tasks:",
        len(st.session_state.tasks)
    )

    st.write(
        "📚 Learning:",
        len(st.session_state.learning)
    )

    st.write(
        "❤️ Wellness:",
        len(st.session_state.wellness)
    )

    st.write(
        "💰 Expenses:",
        len(st.session_state.expenses)
    )

    st.divider()

    if st.button("🗑️ Clear Demo Data"):

        st.session_state.meetings = []
        st.session_state.reminders = []
        st.session_state.tasks = []
        st.session_state.expenses = []
        st.session_state.learning = []
        st.session_state.wellness = []
        st.session_state.communications = []
        st.session_state.robotics = []
        st.session_state.drones = []
        st.session_state.fired_notifications = set()

        st.success(
            "Demo data cleared."
        )

        st.rerun()


# ==========================================================
# API KEY
# ==========================================================

api_key = ""

if mode == "🔑 Grok API Mode":

    try:
        api_key = st.secrets["XAI_API_KEY"]
    except Exception:
        api_key = os.getenv(
            "XAI_API_KEY",
            ""
        )


# ==========================================================
# RUN NOTIFICATION ENGINE
# ==========================================================

if mode == "🎮 Demo Mode":

    notification_engine()


# ==========================================================
# DASHBOARD
# ==========================================================

if selected == "🏠 Dashboard":

    st.header("📊 OMNI AI Dashboard")

    st.write(
        "Central dashboard for the Omni-Agentic "
        "Intelligent Automation System."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📅 Meetings",
            len(st.session_state.meetings)
        )

    with col2:
        st.metric(
            "⏰ Reminders",
            len(st.session_state.reminders)
        )

    with col3:
        st.metric(
            "📝 Tasks",
            len(st.session_state.tasks)
        )

    with col4:

        total_expense = sum(
            item.get("amount", 0)
            for item in st.session_state.expenses
        )

        st.metric(
            "💰 Expenses",
            f"{total_expense:,.0f}"
        )

    st.divider()

    st.subheader("🔄 OMNI AI Architecture")

    st.markdown(
        """
**User Request**

↓

**Streamlit Interface**

↓

**AI Orchestrator**

↓

**Specialized AI Agent**

↓

**Demo Engine / Grok AI**

↓

**Task / Result Processing**

↓

**Response + Notification**
"""
    )

    st.divider()

    st.subheader("🚀 Available Agents")

    agent_columns = st.columns(2)

    for index, agent_name in enumerate(AGENTS):

        with agent_columns[index % 2]:

            st.info(
                "**"
                + agent_name
                + "**\n\n"
                + AGENTS[agent_name]
            )


# ==========================================================
# AI ORCHESTRATOR
# ==========================================================

elif selected == "🧠 AI Orchestrator":

    st.header("🧠 AI Orchestrator / Master Agent")

    st.write(
        "Enter a natural-language request. "
        "OMNI AI identifies the appropriate specialized agent."
    )

    request = st.text_area(
        "💬 Your Request",
        placeholder=(
            "Example: Schedule a project meeting tomorrow "
            "at 10 AM and remind me at the meeting time."
        )
    )

    if st.button("🚀 Process Request"):

        if not request.strip():

            st.warning(
                "Please enter a request."
            )

        else:

            selected_agent = detect_agent(
                request
            )

            st.success(
                "🧠 Selected Agent: "
                + selected_agent
            )

            if mode == "🎮 Demo Mode":

                result = demo_response(
                    request,
                    selected_agent
                )

                st.markdown(result)

            else:

                if not api_key:

                    st.error(
                        "XAI_API_KEY is not configured."
                    )

                else:

                    try:

                        with st.spinner(
                            "🤖 Grok is processing..."
                        ):

                            result = grok_response(
                                request,
                                selected_agent,
                                api_key
                            )

                        st.markdown(result)

                    except Exception as error:

                        st.error(
                            str(error)
                        )


# ==========================================================
# REMINDERS & ALARMS
# ==========================================================

elif selected == "⏰ Reminders & Alarms":

    st.header("⏰ Reminders & Alarms")

    st.write(
        "Create reminders with exact due date, due time "
        "and notification."
    )

    with st.form("reminder_form"):

        title = st.text_input(
            "Reminder / Alarm Title",
            placeholder="Submit OMNI AI Project"
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Due Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Due Time",
                value=time(9, 0)
            )

        notification = st.checkbox(
            "🔔 Enable Notification / Alarm",
            value=True
        )

        repeat = st.selectbox(
            "🔁 Repeat",
            [
                "Once",
                "Daily",
                "Weekly",
                "Weekdays",
                "Monthly"
            ]
        )

        priority = st.selectbox(
            "⚡ Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        notes = st.text_area(
            "📝 Notes"
        )

        submitted = st.form_submit_button(
            "➕ Schedule Reminder"
        )

        if submitted:

            if title.strip():

                st.session_state.reminders.append(
                    {
                        "title": title,
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
                        "repeat": repeat,
                        "priority": priority,
                        "notes": notes
                    }
                )

                st.success(
                    "✅ Reminder scheduled."
                )

            else:

                st.warning(
                    "Enter a reminder title."
                )

    st.divider()

    st.subheader(
        "📋 Scheduled Reminders"
    )

    for index, item in enumerate(
        st.session_state.reminders
    ):

        st.info(
            "⏰ **"
            + item["title"]
            + "**\n\n"
            + "📅 Due Date: "
            + str(item["due_date"])
            + "\n\n"
            + "🕐 Due Time: "
            + str(item["due_time"])
            + "\n\n"
            + "🔔 Notification: "
            + ("ON" if item["notification"] else "OFF")
            + "\n\n"
            + "🔁 Repeat: "
            + item["repeat"]
            + "\n\n"
            + "⚡ Priority: "
            + item["priority"]
        )

        if st.button(
            "🗑️ Delete",
            key="delete_reminder_" + str(index)
        ):

            st.session_state.reminders.pop(index)

            st.rerun()


# ==========================================================
# CALENDAR & MEETINGS
# ==========================================================

elif selected == "📅 Calendar & Meetings":

    st.header("📅 Calendar & Meetings")

    st.write(
        "Create meetings and events with due date, "
        "time and notification."
    )

    with st.form("meeting_form"):

        title = st.text_input(
            "Meeting / Event Title"
        )

        col1, col2 = st.columns(2)

        with col1:

            meeting_date = st.date_input(
                "📅 Date",
                value=date.today()
            )

        with col2:

            meeting_time = st.time_input(
                "⏰ Time",
                value=time(10, 0)
            )

        duration = st.number_input(
            "Duration (minutes)",
            min_value=15,
            max_value=480,
            value=60,
            step=15
        )

        location = st.text_input(
            "📍 Location / Platform"
        )

        participants = st.text_input(
            "👥 Participants"
        )

        meeting_type = st.selectbox(
            "🏷️ Type",
            [
                "Meeting",
                "Class",
                "Appointment",
                "Event",
                "Project Review"
            ]
        )

        notification = st.checkbox(
            "🔔 Meeting Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Add to Calendar"
        )

        if submitted:

            if title.strip():

                st.session_state.meetings.append(
                    {
                        "title": title,
                        "date": meeting_date,
                        "time": meeting_time,
                        "duration": duration,
                        "location": location,
                        "participants": participants,
                        "type": meeting_type,
                        "notification": notification
                    }
                )

                st.success(
                    "✅ Meeting added to calendar."
                )

            else:

                st.warning(
                    "Enter meeting title."
                )

    st.divider()

    st.subheader("📆 Calendar")

    sorted_meetings = sorted(
        st.session_state.meetings,
        key=lambda x: (
            x["date"],
            x["time"]
        )
    )

    for index, item in enumerate(
        sorted_meetings
    ):

        st.info(
            "📅 **"
            + item["title"]
            + "**\n\n"
            + "📅 Date: "
            + str(item["date"])
            + "\n\n"
            + "⏰ Time: "
            + str(item["time"])
            + "\n\n"
            + "⏱️ Duration: "
            + str(item["duration"])
            + " minutes\n\n"
            + "📍 Location: "
            + (item["location"] or "Not specified")
            + "\n\n"
            + "👥 Participants: "
            + (item["participants"] or "Not specified")
            + "\n\n"
            + "🔔 Notification: "
            + ("ON" if item["notification"] else "OFF")
        )


# ==========================================================
# TASKS
# ==========================================================

elif selected == "📝 Tasks & Productivity":

    st.header("📝 Tasks & Productivity")

    with st.form("task_form"):

        task = st.text_input(
            "📝 Task"
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Due Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Due Time",
                value=time(17, 0)
            )

        priority = st.selectbox(
            "⚡ Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        notification = st.checkbox(
            "🔔 Enable Task Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Add Task"
        )

        if submitted:

            if task.strip():

                st.session_state.tasks.append(
                    {
                        "task": task,
                        "due_date": due_date,
                        "due_time": due_time,
                        "priority": priority,
                        "notification": notification,
                        "completed": False
                    }
                )

                st.success(
                    "✅ Task added."
                )

    st.divider()

    for index, item in enumerate(
        st.session_state.tasks
    ):

        item["completed"] = st.checkbox(
            "✅ " + item["task"],
            value=item["completed"],
            key="task_checkbox_" + str(index)
        )

        st.caption(
            "📅 "
            + str(item["due_date"])
            + "  ⏰ "
            + str(item["due_time"])
            + "  ⚡ "
            + item["priority"]
            + "  🔔 "
            + (
                "ON"
                if item["notification"]
                else "OFF"
            )
        )


# ==========================================================
# LEARNING
# ==========================================================

elif selected == "📚 Learning":

    st.header("📚 Learning & Education Agent")

    with st.form("learning_form"):

        subject = st.text_input(
            "📚 Subject / Course"
        )

        goal = st.text_area(
            "🎯 Learning Goal"
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Activity Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Study Time",
                value=time(18, 0)
            )

        notification = st.checkbox(
            "🔔 Study Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Add Learning Activity"
        )

        if submitted and subject.strip():

            st.session_state.learning.append(
                {
                    "subject": subject,
                    "goal": goal,
                    "due_date": due_date,
                    "due_time": due_time,
                    "notification": notification
                }
            )

            st.success(
                "✅ Learning activity added."
            )

    for item in st.session_state.learning:

        st.info(
            "📚 **"
            + item["subject"]
            + "**\n\n"
            + "🎯 "
            + item["goal"]
            + "\n\n"
            + "📅 "
            + str(item["due_date"])
            + "  ⏰ "
            + str(item["due_time"])
            + "\n\n"
            + "🔔 Notification: "
            + (
                "ON"
                if item["notification"]
                else "OFF"
            )
        )


# ==========================================================
# WELLNESS
# ==========================================================

elif selected == "❤️ Wellness":

    st.header("❤️ Health & Wellness Agent")

    with st.form("wellness_form"):

        activity = st.text_input(
            "❤️ Activity"
        )

        activity_type = st.selectbox(
            "Activity Type",
            [
                "Exercise",
                "Walking",
                "Hydration",
                "Meditation",
                "Appointment",
                "Other"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Time",
                value=time(7, 0)
            )

        notification = st.checkbox(
            "🔔 Wellness Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Add Wellness Activity"
        )

        if submitted and activity.strip():

            st.session_state.wellness.append(
                {
                    "activity": activity,
                    "type": activity_type,
                    "due_date": due_date,
                    "due_time": due_time,
                    "notification": notification
                }
            )

            st.success(
                "✅ Wellness activity scheduled."
            )

    for item in st.session_state.wellness:

        st.info(
            "❤️ **"
            + item["activity"]
            + "**\n\n"
            + "Type: "
            + item["type"]
            + "\n\n"
            + "📅 "
            + str(item["due_date"])
            + "  ⏰ "
            + str(item["due_time"])
            + "\n\n"
            + "🔔 Notification: "
            + (
                "ON"
                if item["notification"]
                else "OFF"
            )
        )


# ==========================================================
# FINANCE
# ==========================================================

elif selected == "💰 Finance":

    st.header("💰 Finance & Expense Management")

    with st.form("finance_form"):

        description = st.text_input(
            "Expense / Payment"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Education",
                "Utilities",
                "Shopping",
                "Bills",
                "Other"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Payment Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Payment Time",
                value=time(12, 0)
            )

        notification = st.checkbox(
            "🔔 Payment Notification",
            value=False
        )

        submitted = st.form_submit_button(
            "➕ Add Expense"
        )

        if submitted and description.strip():

            st.session_state.expenses.append(
                {
                    "description": description,
                    "amount": amount,
                    "category": category,
                    "due_date": due_date,
                    "due_time": due_time,
                    "notification": notification
                }
            )

            st.success(
                "✅ Expense added."
            )

    total = sum(
        item["amount"]
        for item in st.session_state.expenses
    )

    st.metric(
        "💰 Total Expenses",
        f"{total:,.2f}"
    )

    for item in st.session_state.expenses:

        st.write(
            "**"
            + item["description"]
            + "** — "
            + f"{item['amount']:,.2f}"
            + " — "
            + item["category"]
            + " — "
            + str(item["due_date"])
        )


# ==========================================================
# COMMUNICATION
# ==========================================================

elif selected == "🌐 Communication":

    st.header("🌐 Information & Communication Agent")

    content_type = st.selectbox(
        "Content Type",
        [
            "Email",
            "Announcement",
            "Report",
            "Message",
            "Notice"
        ]
    )

    recipient = st.text_input(
        "Recipient / Audience"
    )

    subject = st.text_input(
        "Subject"
    )

    content = st.text_area(
        "Message"
    )

    col1, col2 = st.columns(2)

    with col1:

        due_date = st.date_input(
            "📅 Schedule Date",
            value=date.today()
        )

    with col2:

        due_time = st.time_input(
            "⏰ Schedule Time",
            value=time(10, 0)
        )

    notification = st.checkbox(
        "🔔 Communication Notification",
        value=False
    )

    if st.button("✍️ Generate & Save Communication"):

        generated = (
            "Dear Team,\n\n"
            + content
            + "\n\n"
            + "Regards,\n"
            + "OMNI AI"
        )

        st.session_state.communications.append(
            {
                "type": content_type,
                "recipient": recipient,
                "subject": subject,
                "content": generated,
                "due_date": due_date,
                "due_time": due_time,
                "notification": notification
            }
        )

        st.success(
            "✅ Communication saved."
        )

        st.markdown(generated)


# ==========================================================
# ROBOTICS
# ==========================================================

elif selected == "🤖 Robotics":

    st.header("🤖 Robotics Agent")

    with st.form("robotics_form"):

        project = st.text_input(
            "🤖 Project Name"
        )

        controller = st.selectbox(
            "Controller",
            [
                "Arduino",
                "ESP32",
                "Raspberry Pi",
                "STM32"
            ]
        )

        sensor = st.text_input(
            "Sensor / Camera"
        )

        objective = st.text_area(
            "Project Objective"
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Project Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Review Time",
                value=time(15, 0)
            )

        notification = st.checkbox(
            "🔔 Project Notification",
            value=False
        )

        submitted = st.form_submit_button(
            "➕ Add Robotics Project"
        )

        if submitted and project.strip():

            st.session_state.robotics.append(
                {
                    "project": project,
                    "controller": controller,
                    "sensor": sensor,
                    "objective": objective,
                    "due_date": due_date,
                    "due_time": due_time,
                    "notification": notification
                }
            )

            st.success(
                "✅ Robotics project added."
            )

    for item in st.session_state.robotics:

        st.info(
            "🤖 **"
            + item["project"]
            + "**\n\n"
            + "Controller: "
            + item["controller"]
            + "\n\n"
            + "Sensor: "
            + item["sensor"]
            + "\n\n"
            + "Objective: "
            + item["objective"]
            + "\n\n"
            + "📅 "
            + str(item["due_date"])
            + "  ⏰ "
            + str(item["due_time"])
        )


# ==========================================================
# DRONES
# ==========================================================

elif selected == "🚁 Drones & Autonomous":

    st.header("🚁 Drones & Autonomous Systems Agent")

    with st.form("drone_form"):

        project = st.text_input(
            "🚁 Mission / Project"
        )

        platform = st.selectbox(
            "Platform",
            [
                "Quadcopter",
                "Fixed Wing UAV",
                "Ground Robot",
                "Autonomous Vehicle"
            ]
        )

        sensor = st.text_input(
            "Camera / Sensor"
        )

        mission = st.text_area(
            "Mission Objective"
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Mission Date",
                value=date.today()
            )

        with col2:

            due_time = st.time_input(
                "⏰ Mission Time",
                value=time(16, 0)
            )

        notification = st.checkbox(
            "🔔 Mission Notification",
            value=False
        )

        submitted = st.form_submit_button(
            "➕ Add Mission"
        )

        if submitted and project.strip():

            st.session_state.drones.append(
                {
                    "project": project,
                    "platform": platform,
                    "sensor": sensor,
                    "mission": mission,
                    "due_date": due_date,
                    "due_time": due_time,
                    "notification": notification
                }
            )

            st.success(
                "✅ Autonomous mission added."
            )

    for item in st.session_state.drones:

        st.info(
            "🚁 **"
            + item["project"]
            + "**\n\n"
            + "Platform: "
            + item["platform"]
            + "\n\n"
            + "Sensor: "
            + item["sensor"]
            + "\n\n"
            + "Mission: "
            + item["mission"]
            + "\n\n"
            + "📅 "
            + str(item["due_date"])
            + "  ⏰ "
            + str(item["due_time"])
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "🤖 OMNI AI | Omni-Agentic Intelligent Automation System | "
    "Demo + Grok API Mode | Calendar + Alarms + Notifications"
)
