import os
from datetime import datetime, date, time

import requests
import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False


# ============================================================
# PAGE CONFIGURATION
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

def initialize_state():

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
        "fired_notifications": set(),
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            if isinstance(value, list):
                st.session_state[key] = []

            elif isinstance(value, set):
                st.session_state[key] = set()

            else:
                st.session_state[key] = value


initialize_state()


# ============================================================
# HEADER / BANNER
# ============================================================

st.markdown(
    """
    <div style="
        padding:28px;
        border-radius:20px;
        margin-bottom:20px;
        background:linear-gradient(135deg,#111827,#1f2937);
        border:1px solid #374151;
        text-align:center;
    ">

        <h1 style="
            color:white;
            margin:0;
            font-size:42px;
        ">
            🤖 OMNI AI
        </h1>

        <h2 style="
            color:#d1d5db;
            margin-top:8px;
        ">
            Omni-Agentic Intelligent Automation System
        </h2>

        <p style="
            color:#9ca3af;
            font-size:17px;
        ">
            Multi-Agent AI Assistant • Demo Mode • Grok API Mode
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENT DIRECTORY
# ============================================================

AGENTS = {

    "🧠 AI Orchestrator":
        "Central intelligence that analyzes requests and selects the appropriate agent.",

    "⏰ Daily Reminder Agent":
        "Reminders, alarms, deadlines and recurring activities.",

    "❤️ Health & Wellness Agent":
        "Wellness routines, fitness activities and appointments.",

    "📅 Calendar & Schedule Agent":
        "Meetings, classes, events and appointments.",

    "📚 Learning & Education Agent":
        "Study plans, courses, revision and educational activities.",

    "📝 Productivity & Task Agent":
        "Tasks, priorities, projects and checklists.",

    "💰 Finance & Expense Agent":
        "Expenses, budgets and payment reminders.",

    "🌐 Information & Communication Agent":
        "Emails, announcements, reports and messages.",

    "🤖 Robotics Agent":
        "Controllers, sensors, components, actuators and robotics architecture.",

    "🚁 Drones & Autonomous Systems Agent":
        "UAVs, autonomous systems, navigation and computer vision.",
}


# ============================================================
# SAFE DATA HELPER
# ============================================================

def safe_get(item, key, default="Not specified"):

    if not isinstance(item, dict):
        return default

    return item.get(key, default)


# ============================================================
# NOTIFICATION ID
# ============================================================

def make_notification_id(
    category,
    title,
    due_date,
    due_time
):

    return (
        str(category)
        + "|"
        + str(title)
        + "|"
        + str(due_date)
        + "|"
        + str(due_time)
    )


# ============================================================
# BROWSER NOTIFICATION
# ============================================================

def send_browser_notification(message):

    safe_message = (
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

                if (Notification.permission === "default") {{
                    Notification.requestPermission();
                }}

                if (Notification.permission === "granted") {{

                    new Notification(
                        "🤖 OMNI AI Reminder",
                        {{
                            body: '{safe_message}'
                        }}
                    );

                }}

            }}

        }} catch(error) {{

            console.log(error);

        }}

        </script>
        """,
        height=0,
    )


# ============================================================
# DUE DATE / TIME CHECK
# ============================================================

def check_notifications(
    items,
    category,
    title_key,
    date_key,
    time_key,
    notification_key,
    icon,
    notifications
):

    now = datetime.now()

    today = now.date()

    current_time = now.time().replace(
        second=0,
        microsecond=0
    )

    for item in items:

        if not isinstance(item, dict):
            continue

        enabled = item.get(
            notification_key,
            False
        )

        if not enabled:
            continue

        due_date = item.get(date_key)

        due_time = item.get(time_key)

        title = item.get(
            title_key,
            category
        )

        if due_date != today:
            continue

        if due_time is None:
            continue

        try:

            if due_time <= current_time:

                notification_id = make_notification_id(
                    category,
                    title,
                    due_date,
                    due_time
                )

                if notification_id not in st.session_state.fired_notifications:

                    st.session_state.fired_notifications.add(
                        notification_id
                    )

                    notifications.append(
                        f"{icon} {title} is due now."
                    )

        except Exception:
            continue


# ============================================================
# NOTIFICATION ENGINE
# ============================================================

def notification_engine():

    notifications = []

    check_notifications(
        st.session_state.reminders,
        "Reminder",
        "title",
        "due_date",
        "due_time",
        "notification",
        "⏰",
        notifications
    )

    check_notifications(
        st.session_state.meetings,
        "Meeting",
        "title",
        "date",
        "time",
        "notification",
        "📅",
        notifications
    )

    check_notifications(
        st.session_state.tasks,
        "Task",
        "task",
        "due_date",
        "due_time",
        "notification",
        "📝",
        notifications
    )

    check_notifications(
        st.session_state.learning,
        "Learning",
        "subject",
        "due_date",
        "due_time",
        "notification",
        "📚",
        notifications
    )

    check_notifications(
        st.session_state.wellness,
        "Wellness",
        "activity",
        "due_date",
        "due_time",
        "notification",
        "❤️",
        notifications
    )

    check_notifications(
        st.session_state.expenses,
        "Finance",
        "description",
        "due_date",
        "due_time",
        "notification",
        "💰",
        notifications
    )

    check_notifications(
        st.session_state.communications,
        "Communication",
        "subject",
        "due_date",
        "due_time",
        "notification",
        "🌐",
        notifications
    )

    check_notifications(
        st.session_state.robotics,
        "Robotics",
        "project",
        "due_date",
        "due_time",
        "notification",
        "🤖",
        notifications
    )

    check_notifications(
        st.session_state.drones,
        "Drone",
        "project",
        "due_date",
        "due_time",
        "notification",
        "🚁",
        notifications
    )

    for message in notifications:

        st.toast(
            message,
            icon="🔔"
        )

        send_browser_notification(
            message
        )

    if notifications:

        st.warning(
            "🔔 OMNI AI NOTIFICATION\n\n"
            + "\n\n".join(
                "- " + message
                for message in notifications
            )
        )


# ============================================================
# AUTO REFRESH
# ============================================================

if AUTO_REFRESH_AVAILABLE:

    st_autorefresh(
        interval=15000,
        key="omni_notification_refresh"
    )


notification_engine()


# ============================================================
# AGENT DETECTION
# ============================================================

def detect_agent(request):

    text = request.lower()

    rules = [

        (
            [
                "reminder",
                "alarm",
                "remind",
                "deadline"
            ],
            "⏰ Daily Reminder Agent"
        ),

        (
            [
                "health",
                "wellness",
                "fitness",
                "exercise",
                "workout"
            ],
            "❤️ Health & Wellness Agent"
        ),

        (
            [
                "calendar",
                "meeting",
                "schedule",
                "appointment",
                "event",
                "class"
            ],
            "📅 Calendar & Schedule Agent"
        ),

        (
            [
                "learn",
                "learning",
                "study",
                "education",
                "course",
                "python",
                "exam"
            ],
            "📚 Learning & Education Agent"
        ),

        (
            [
                "task",
                "todo",
                "to-do",
                "productivity",
                "project",
                "checklist"
            ],
            "📝 Productivity & Task Agent"
        ),

        (
            [
                "expense",
                "finance",
                "budget",
                "money",
                "payment",
                "spending"
            ],
            "💰 Finance & Expense Agent"
        ),

        (
            [
                "email",
                "message",
                "announcement",
                "report",
                "letter"
            ],
            "🌐 Information & Communication Agent"
        ),

        (
            [
                "robot",
                "robotics",
                "arduino",
                "esp32",
                "raspberry",
                "sensor",
                "motor",
                "embedded"
            ],
            "🤖 Robotics Agent"
        ),

        (
            [
                "drone",
                "uav",
                "autonomous",
                "navigation",
                "quadcopter",
                "flight"
            ],
            "🚁 Drones & Autonomous Systems Agent"
        ),
    ]

    for words, agent in rules:

        for word in words:

            if word in text:
                return agent

    return "🧠 AI Orchestrator"


# ============================================================
# DEMO AI RESPONSE
# ============================================================

def demo_response(
    request,
    agent
):

    descriptions = {

        "⏰ Daily Reminder Agent":
            "Creates reminders, alarms, deadlines and recurring routines.",

        "❤️ Health & Wellness Agent":
            "Organizes user-provided wellness activities and appointments.",

        "📅 Calendar & Schedule Agent":
            "Organizes meetings, events, classes and appointments.",

        "📚 Learning & Education Agent":
            "Creates structured learning and revision plans.",

        "📝 Productivity & Task Agent":
            "Converts activities into structured tasks and priorities.",

        "💰 Finance & Expense Agent":
            "Organizes user-entered expenses, categories and budgets.",

        "🌐 Information & Communication Agent":
            "Creates emails, reports, notices and announcements.",

        "🤖 Robotics Agent":
            "Supports controllers, sensors, components, actuators and automation.",

        "🚁 Drones & Autonomous Systems Agent":
            "Supports UAVs, autonomous platforms, navigation and computer vision.",

        "🧠 AI Orchestrator":
            "Analyzes the request and coordinates the appropriate specialist agent.",
    }

    return f"""
## {agent}

### User Request

> {request}

### Demo Processing

1. Request received
2. Natural-language intent analyzed
3. Appropriate agent selected
4. Specialized workflow executed
5. Result generated

### Demo Result

{descriptions.get(
    agent,
    "Demo processing completed."
)}

### Agent Status

🟢 **Active — Demo Mode**
"""


# ============================================================
# GROK API
# ============================================================

def call_grok(
    request,
    agent,
    api_key
):

    url = "https://api.x.ai/v1/chat/completions"

    headers = {

        "Authorization":
            "Bearer " + api_key,

        "Content-Type":
            "application/json",
    }

    payload = {

        "model":
            "grok-3-mini",

        "messages": [

            {
                "role": "system",

                "content":
                    f"""
You are OMNI AI, an intelligent
multi-agent assistant.

Selected Agent:
{agent}

Provide practical, structured,
clear answers.

Do not claim that an external
action was completed unless the
application actually performed it.
"""
            },

            {
                "role": "user",

                "content":
                    request
            }
        ],

        "temperature":
            0.3,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90
    )

    if response.status_code == 403:

        raise RuntimeError(
            "Grok API returned 403. "
            "Please check your XAI_API_KEY, "
            "account access and API availability."
        )

    if response.status_code != 200:

        raise RuntimeError(
            "Grok API Error "
            + str(response.status_code)
            + ": "
            + response.text
        )

    data = response.json()

    return data["choices"][0]["message"]["content"]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 OMNI AI")

    st.caption(
        "Agent Navigation"
    )

    pages = [

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

        "🚁 Drones & Autonomous",
    ]

    selected_page = st.radio(
        "Select Module",
        pages
    )

    st.divider()

    operating_mode = st.radio(
        "Operating Mode",
        [
            "🎮 Demo Mode",
            "🔑 Grok API Mode"
        ]
    )

    api_key = ""

    if operating_mode == "🔑 Grok API Mode":

        try:

            api_key = st.secrets[
                "XAI_API_KEY"
            ]

        except Exception:

            api_key = os.getenv(
                "XAI_API_KEY",
                ""
            )

        if api_key:

            st.success(
                "🔑 Grok API key detected."
            )

        else:

            st.warning(
                "XAI_API_KEY not configured."
            )

    st.divider()

    st.subheader(
        "📊 Statistics"
    )

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

    st.write(
        "🤖 Robotics:",
        len(st.session_state.robotics)
    )

    st.write(
        "🚁 Drones:",
        len(st.session_state.drones)
    )

    st.divider()

    if st.button(
        "🗑️ Clear All Demo Data"
    ):

        st.session_state.meetings = []
        st.session_state.reminders = []
        st.session_state.tasks = []
        st.session_state.learning = []
        st.session_state.wellness = []
        st.session_state.expenses = []
        st.session_state.communications = []
        st.session_state.robotics = []
        st.session_state.drones = []
        st.session_state.fired_notifications = set()

        st.success(
            "All demo data cleared."
        )

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if selected_page == "🏠 Dashboard":

    st.header(
        "📊 OMNI AI Dashboard"
    )

    st.write(
        """
        OMNI AI is a centralized multi-agent
        intelligent assistant powered by Streamlit
        with optional Grok API integration.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📅 Meetings",
        len(st.session_state.meetings)
    )

    col2.metric(
        "⏰ Reminders",
        len(st.session_state.reminders)
    )

    col3.metric(
        "📝 Tasks",
        len(st.session_state.tasks)
    )

    col4.metric(
        "🤖 Robotics",
        len(st.session_state.robotics)
    )

    st.divider()

    st.subheader(
        "🔄 OMNI AI Architecture"
    )

    st.code(
        """
User Request
     ↓
Streamlit Interface
     ↓
AI Orchestrator
     ↓
Agent Selection
     ↓
Specialized AI Agent
     ↓
Demo Engine / Grok API
     ↓
Task Processing
     ↓
Due Date + Due Time
     ↓
🔔 Notification
     ↓
User
        """,
        language="text"
    )

    st.subheader(
        "🤖 Available Agents"
    )

    for name, description in AGENTS.items():

        st.info(
            f"**{name}**\n\n"
            f"{description}"
        )


# ============================================================
# AI ORCHESTRATOR
# ============================================================

elif selected_page == "🧠 AI Orchestrator":

    st.header(
        "🧠 AI Orchestrator / Master Agent"
    )

    request = st.text_area(
        "💬 Enter your request",
        placeholder=(
            "Example: Schedule an AI project "
            "meeting tomorrow at 10 AM."
        ),
        height=150
    )

    if st.button(
        "🚀 Process Request"
    ):

        if not request.strip():

            st.warning(
                "Please enter a request."
            )

        else:

            agent = detect_agent(
                request
            )

            st.success(
                "🧠 Selected Agent: "
                + agent
            )

            if operating_mode == "🎮 Demo Mode":

                result = demo_response(
                    request,
                    agent
                )

                st.markdown(
                    result
                )

            else:

                if not api_key:

                    st.error(
                        "XAI_API_KEY is missing. "
                        "Add it in Streamlit Secrets."
                    )

                else:

                    try:

                        with st.spinner(
                            "🤖 Grok is processing..."
                        ):

                            result = call_grok(
                                request,
                                agent,
                                api_key
                            )

                        st.markdown(
                            result
                        )

                    except Exception as error:

                        st.error(
                            str(error)
                        )


# ============================================================
# REMINDERS & ALARMS
# ============================================================

elif selected_page == "⏰ Reminders & Alarms":

    st.header(
        "⏰ Daily Reminder Agent"
    )

    with st.form(
        "reminder_form"
    ):

        title = st.text_input(
            "Reminder / Alarm Title"
        )

        col1, col2 = st.columns(2)

        due_date = col1.date_input(
            "📅 Due Date",
            value=date.today()
        )

        due_time = col2.time_input(
            "⏰ Alarm Time",
            value=time(9, 0)
        )

        notification = st.checkbox(
            "🔔 Enable Alarm / Notification",
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
            "➕ Schedule Alarm"
        )

        if submitted:

            if title.strip():

                st.session_state.reminders.append({

                    "title":
                        title,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "notification":
                        notification,

                    "repeat":
                        repeat,

                    "priority":
                        priority,

                    "notes":
                        notes,
                })

                st.success(
                    "✅ Alarm / reminder scheduled."
                )

            else:

                st.warning(
                    "Enter reminder title."
                )

    st.divider()

    if not st.session_state.reminders:

        st.info(
            "No reminders scheduled."
        )

    for index, item in enumerate(
        st.session_state.reminders
    ):

        st.info(
            f"""
⏰ **{safe_get(item, 'title')}**

📅 Date: {safe_get(item, 'due_date')}

🕐 Time: {safe_get(item, 'due_time')}

🔔 Notification:
{'ON' if item.get('notification', False) else 'OFF'}

🔁 Repeat: {safe_get(item, 'repeat')}

⚡ Priority: {safe_get(item, 'priority')}

📝 Notes: {safe_get(item, 'notes')}
"""
        )

        if st.button(
            "🗑️ Delete",
            key=f"delete_reminder_{index}"
        ):

            st.session_state.reminders.pop(
                index
            )

            st.rerun()


# ============================================================
# CALENDAR
# ============================================================

elif selected_page == "📅 Calendar & Meetings":

    st.header(
        "📅 Calendar & Schedule Agent"
    )

    with st.form(
        "meeting_form"
    ):

        title = st.text_input(
            "Meeting / Event Title"
        )

        col1, col2 = st.columns(2)

        meeting_date = col1.date_input(
            "📅 Date",
            value=date.today()
        )

        meeting_time = col2.time_input(
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
            "🏷️ Event Type",
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

                st.session_state.meetings.append({

                    "title":
                        title,

                    "date":
                        meeting_date,

                    "time":
                        meeting_time,

                    "duration":
                        duration,

                    "location":
                        location,

                    "participants":
                        participants,

                    "type":
                        meeting_type,

                    "notification":
                        notification,
                })

                st.success(
                    "✅ Meeting added to calendar."
                )

            else:

                st.warning(
                    "Enter meeting title."
                )

    st.divider()

    for index, item in enumerate(
        st.session_state.meetings
    ):

        st.info(
            f"""
📅 **{safe_get(item, 'title')}**

📅 Date: {safe_get(item, 'date')}

⏰ Time: {safe_get(item, 'time')}

⏱️ Duration:
{safe_get(item, 'duration')} minutes

📍 Location:
{safe_get(item, 'location')}

👥 Participants:
{safe_get(item, 'participants')}

🔔 Notification:
{'ON' if item.get('notification', False) else 'OFF'}
"""
        )

        if st.button(
            "🗑️ Delete Meeting",
            key=f"delete_meeting_{index}"
        ):

            st.session_state.meetings.pop(
                index
            )

            st.rerun()


# ============================================================
# LEARNING
# ============================================================

elif selected_page == "📚 Learning":

    st.header(
        "📚 Learning & Education Agent"
    )

    with st.form(
        "learning_form"
    ):

        subject = st.text_input(
            "📚 Subject / Course"
        )

        goal = st.text_area(
            "🎯 Learning Goal"
        )

        col1, col2 = st.columns(2)

        due_date = col1.date_input(
            "📅 Study Date",
            value=date.today()
        )

        due_time = col2.time_input(
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

        if submitted:

            if subject.strip():

                st.session_state.learning.append({

                    "subject":
                        subject,

                    "goal":
                        goal,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "notification":
                        notification,
                })

                st.success(
                    "✅ Learning activity added."
                )

    for item in st.session_state.learning:

        st.info(
            f"""
📚 **{safe_get(item, 'subject')}**

🎯 Goal:
{safe_get(item, 'goal')}

📅 {safe_get(item, 'due_date')}

⏰ {safe_get(item, 'due_time')}

🔔 Notification:
{'ON' if item.get('notification', False) else 'OFF'}
"""
        )


# ============================================================
# TASK MANAGEMENT
# ============================================================

elif selected_page == "📝 Tasks & Productivity":

    st.header(
        "📝 Productivity & Task Management Agent"
    )

    with st.form(
        "task_form"
    ):

        task = st.text_input(
            "📝 Task"
        )

        col1, col2 = st.columns(2)

        due_date = col1.date_input(
            "📅 Due Date",
            value=date.today()
        )

        due_time = col2.time_input(
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

                st.session_state.tasks.append({

                    "task":
                        task,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "priority":
                        priority,

                    "notification":
                        notification,

                    "completed":
                        False,
                })

                st.success(
                    "✅ Task added."
                )

    for index, item in enumerate(
        st.session_state.tasks
    ):

        item["completed"] = st.checkbox(
            "✅ "
            + str(
                safe_get(
                    item,
                    "task"
                )
            ),

            value=item.get(
                "completed",
                False
            ),

            key=f"task_checkbox_{index}"
        )

        st.caption(
            "📅 "
            + str(
                safe_get(
                    item,
                    "due_date"
                )
            )
            + " | ⏰ "
            + str(
                safe_get(
                    item,
                    "due_time"
                )
            )
            + " | ⚡ "
            + str(
                safe_get(
                    item,
                    "priority"
                )
            )
            + " | 🔔 "
            + (
                "ON"
                if item.get(
                    "notification",
                    False
                )
                else "OFF"
            )
        )


# ============================================================
# WELLNESS
# ============================================================

elif selected_page == "❤️ Wellness":

    st.header(
        "❤️ Health & Wellness Agent"
    )

    with st.form(
        "wellness_form"
    ):

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

        due_date = col1.date_input(
            "📅 Date",
            value=date.today()
        )

        due_time = col2.time_input(
            "⏰ Time",
            value=time(7, 0)
        )

        notification = st.checkbox(
            "🔔 Wellness Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Schedule Wellness Activity"
        )

        if submitted:

            if activity.strip():

                st.session_state.wellness.append({

                    "activity":
                        activity,

                    "type":
                        activity_type,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "notification":
                        notification,
                })

                st.success(
                    "✅ Wellness activity scheduled."
                )

    for item in st.session_state.wellness:

        st.info(
            f"""
❤️ **{safe_get(item, 'activity')}**

Type:
{safe_get(item, 'type')}

📅 {safe_get(item, 'due_date')}

⏰ {safe_get(item, 'due_time')}

🔔 Notification:
{'ON' if item.get('notification', False) else 'OFF'}
"""
        )


# ============================================================
# FINANCE
# ============================================================

elif selected_page == "💰 Finance":

    st.header(
        "💰 Finance & Expense Management Agent"
    )

    with st.form(
        "finance_form"
    ):

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

        due_date = col1.date_input(
            "📅 Payment Date",
            value=date.today()
        )

        due_time = col2.time_input(
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

        if submitted:

            if description.strip():

                st.session_state.expenses.append({

                    "description":
                        description,

                    "amount":
                        amount,

                    "category":
                        category,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "notification":
                        notification,
                })

                st.success(
                    "✅ Expense added."
                )

    total = 0.0

    for item in st.session_state.expenses:

        try:

            total += float(
                item.get(
                    "amount",
                    0
                )
            )

        except Exception:
            pass

    st.metric(
        "💰 Total Expenses",
        f"{total:,.2f}"
    )

    for item in st.session_state.expenses:

        st.write(
            f"**{safe_get(item, 'description')}** — "
            f"{float(item.get('amount', 0)):,.2f} — "
            f"{safe_get(item, 'category')} — "
            f"📅 {safe_get(item, 'due_date')} — "
            f"⏰ {safe_get(item, 'due_time')}"
        )


# ============================================================
# COMMUNICATION
# ============================================================

elif selected_page == "🌐 Communication":

    st.header(
        "🌐 Information & Communication Agent"
    )

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
        "Message Content",
        height=150
    )

    col1, col2 = st.columns(2)

    due_date = col1.date_input(
        "📅 Schedule Date",
        value=date.today()
    )

    due_time = col2.time_input(
        "⏰ Schedule Time",
        value=time(10, 0)
    )

    notification = st.checkbox(
        "🔔 Communication Notification",
        value=False
    )

    if st.button(
        "✍️ Generate & Save"
    ):

        generated = (
            "Dear Team,\n\n"
            + content
            + "\n\nRegards,\nOMNI AI"
        )

        st.session_state.communications.append({

            "type":
                content_type,

            "recipient":
                recipient,

            "subject":
                subject or content_type,

            "content":
                generated,

            "due_date":
                due_date,

            "due_time":
                due_time,

            "notification":
                notification,
        })

        st.success(
            "✅ Communication saved."
        )

        st.text_area(
            "Generated Content",
            generated,
            height=180
        )


# ============================================================
# ROBOTICS
# ============================================================

elif selected_page == "🤖 Robotics":

    st.header(
        "🤖 Robotics Agent"
    )

    st.write(
        """
        Design and organize robotics projects using
        selectable controllers, components, sensors,
        actuators, communication modules and applications.
        """
    )

    # --------------------------------------------------------
    # CONTROLLERS
    # --------------------------------------------------------

    controllers = [

        "Arduino Uno",
        "Arduino Mega",
        "Arduino Nano",

        "ESP32",
        "ESP8266",

        "Raspberry Pi",
        "Raspberry Pi Pico",

        "STM32",

        "PLC",

        "Jetson Nano",
        "NVIDIA Jetson Orin",

        "BeagleBone",

        "Custom Controller",
    ]

    # --------------------------------------------------------
    # COMPONENTS
    # --------------------------------------------------------

    components = [

        "Ultrasonic Sensor HC-SR04",

        "IR Sensor",

        "PIR Motion Sensor",

        "LDR",

        "Temperature Sensor",

        "Humidity Sensor",

        "DHT11",

        "DHT22",

        "MPU6050 IMU",

        "MPU9250 IMU",

        "GPS Module",

        "RFID Module",

        "RFID Reader",

        "Camera Module",

        "ESP32-CAM",

        "Raspberry Pi Camera",

        "USB Camera",

        "LiDAR",

        "Encoder",

        "Load Cell",

        "Gas Sensor",

        "Soil Moisture Sensor",

        "Hall Effect Sensor",

        "Limit Switch",

        "Push Button",

        "OLED Display",

        "LCD Display",

        "7-Segment Display",

        "Buzzer",

        "LED",

        "Relay Module",

        "Servo Motor",

        "DC Motor",

        "Stepper Motor",

        "Motor Driver L298N",

        "Motor Driver L293D",

        "TB6612FNG Motor Driver",

        "PCA9685 Servo Driver",

        "Solenoid",

        "Bluetooth HC-05",

        "Bluetooth BLE",

        "Wi-Fi Module",

        "LoRa Module",

        "RF Module",

        "CAN Bus Module",

        "I2C Module",

        "SPI Module",

        "Ethernet Module",

        "Battery / Power Module",

        "Custom Component",
    ]

    # --------------------------------------------------------
    # SENSORS
    # --------------------------------------------------------

    sensors = [

        "No Sensor",

        "Ultrasonic",

        "IR",

        "PIR",

        "Camera",

        "Depth Camera",

        "IMU",

        "GPS",

        "LiDAR",

        "Temperature",

        "Humidity",

        "Temperature / Humidity",

        "Gas",

        "Soil Moisture",

        "Encoder",

        "RFID",

        "Hall Effect",

        "Load Cell",

        "Custom Sensor",
    ]

    # --------------------------------------------------------
    # ACTUATORS
    # --------------------------------------------------------

    actuators = [

        "No Actuator",

        "DC Motor",

        "Servo Motor",

        "Stepper Motor",

        "Relay",

        "Solenoid",

        "LED",

        "Buzzer",

        "Pneumatic Actuator",

        "Hydraulic Actuator",

        "Linear Actuator",

        "Custom Actuator",
    ]

    # --------------------------------------------------------
    # COMMUNICATION
    # --------------------------------------------------------

    communication = [

        "None",

        "Wi-Fi",

        "Bluetooth",

        "BLE",

        "LoRa",

        "RF",

        "CAN",

        "UART",

        "I2C",

        "SPI",

        "Ethernet",

        "MQTT",

        "Modbus",
    ]

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    applications = [

        "Line Following Robot",

        "Obstacle Avoidance Robot",

        "Smart Home Robot",

        "Industrial Automation",

        "Computer Vision Robot",

        "IoT Robot",

        "Agricultural Robot",

        "Security Robot",

        "Educational Robot",

        "Pick & Place Robot",

        "Autonomous Mobile Robot",

        "Humanoid Robot",

        "Medical Assistance Robot",

        "Custom Robotics Project",
    ]

    # --------------------------------------------------------
    # ROBOTICS FORM
    # --------------------------------------------------------

    with st.form(
        "robotics_form"
    ):

        project = st.text_input(
            "🤖 Project Name"
        )

        col1, col2 = st.columns(2)

        controller = col1.selectbox(
            "🎛️ Controller",
            controllers
        )

        component = col2.selectbox(
            "🧩 Main Component",
            components
        )

        col3, col4 = st.columns(2)

        sensor = col3.selectbox(
            "📡 Sensor",
            sensors
        )

        actuator = col4.selectbox(
            "⚙️ Actuator",
            actuators
        )

        col5, col6 = st.columns(2)

        communication_type = col5.selectbox(
            "📶 Communication",
            communication
        )

        application = col6.selectbox(
            "🎯 Application",
            applications
        )

        objective = st.text_area(
            "🎯 Project Objective",
            height=120
        )

        col7, col8 = st.columns(2)

        due_date = col7.date_input(
            "📅 Project / Review Date",
            value=date.today()
        )

        due_time = col8.time_input(
            "⏰ Project / Review Time",
            value=time(15, 0)
        )

        notification = st.checkbox(
            "🔔 Enable Robotics Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Add Robotics Project"
        )

        if submitted:

            if project.strip():

                st.session_state.robotics.append({

                    "project":
                        project,

                    "controller":
                        controller,

                    "component":
                        component,

                    "sensor":
                        sensor,

                    "actuator":
                        actuator,

                    "communication":
                        communication_type,

                    "application":
                        application,

                    "objective":
                        objective,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "notification":
                        notification,
                })

                st.success(
                    "✅ Robotics project added successfully."
                )

            else:

                st.warning(
                    "Please enter project name."
                )

    st.divider()

    st.subheader(
        "🤖 Robotics Projects"
    )

    if not st.session_state.robotics:

        st.info(
            "No robotics projects added yet."
        )

    for index, item in enumerate(
        st.session_state.robotics
    ):

        st.info(
            f"""
🤖 **{safe_get(item, 'project')}**

🎛️ Controller:
{safe_get(item, 'controller')}

🧩 Component:
{safe_get(item, 'component')}

📡 Sensor:
{safe_get(item, 'sensor')}

⚙️ Actuator:
{safe_get(item, 'actuator')}

📶 Communication:
{safe_get(item, 'communication')}

🎯 Application:
{safe_get(item, 'application')}

📝 Objective:
{safe_get(item, 'objective')}

📅 Date:
{safe_get(item, 'due_date')}

⏰ Time:
{safe_get(item, 'due_time')}

🔔 Notification:
{'ON' if item.get('notification', False) else 'OFF'}
"""
        )

        if st.button(
            "🗑️ Delete Robotics Project",
            key=f"delete_robotics_{index}"
        ):

            st.session_state.robotics.pop(
                index
            )

            st.rerun()


# ============================================================
# DRONES
# ============================================================

elif selected_page == "🚁 Drones & Autonomous":

    st.header(
        "🚁 Drones & Autonomous Systems Agent"
    )

    platforms = [

        "Quadcopter",

        "Hexacopter",

        "Octocopter",

        "Fixed Wing UAV",

        "VTOL UAV",

        "UGV",

        "Autonomous Vehicle",

        "Custom Autonomous Platform",
    ]

    sensors = [

        "RGB Camera",

        "Depth Camera",

        "Thermal Camera",

        "LiDAR",

        "GPS",

        "IMU",

        "Ultrasonic",

        "Computer Vision Camera",

        "Radar",

        "Custom Sensor",
    ]

    controllers = [

        "Pixhawk",

        "ArduPilot",

        "PX4",

        "Raspberry Pi",

        "Jetson",

        "ESP32",

        "Custom Flight Controller",
    ]

    with st.form(
        "drone_form"
    ):

        project = st.text_input(
            "🚁 Mission / Project"
        )

        col1, col2 = st.columns(2)

        platform = col1.selectbox(
            "🛩️ Platform",
            platforms
        )

        controller = col2.selectbox(
            "🎛️ Controller",
            controllers
        )

        col3, col4 = st.columns(2)

        sensor = col3.selectbox(
            "📡 Primary Sensor",
            sensors
        )

        navigation = col4.selectbox(
            "🧭 Navigation",
            [
                "GPS",
                "GPS + IMU",
                "Visual Navigation",
                "LiDAR Navigation",
                "SLAM",
                "Manual",
                "Custom"
            ]
        )

        objective = st.text_area(
            "🎯 Mission Objective"
        )

        col5, col6 = st.columns(2)

        due_date = col5.date_input(
            "📅 Mission Date",
            value=date.today()
        )

        due_time = col6.time_input(
            "⏰ Mission Time",
            value=time(16, 0)
        )

        notification = st.checkbox(
            "🔔 Mission Notification",
            value=True
        )

        submitted = st.form_submit_button(
            "➕ Add Mission"
        )

        if submitted:

            if project.strip():

                st.session_state.drones.append({

                    "project":
                        project,

                    "platform":
                        platform,

                    "controller":
                        controller,

                    "sensor":
                        sensor,

                    "navigation":
                        navigation,

                    "mission":
                        objective,

                    "due_date":
                        due_date,

                    "due_time":
                        due_time,

                    "notification":
                        notification,
                })

                st.success(
                    "✅ Autonomous mission added."
                )

            else:

                st.warning(
                    "Enter mission/project name."
                )

    st.divider()

    if not st.session_state.drones:

        st.info(
            "No autonomous missions added yet."
        )

    for index, item in enumerate(
        st.session_state.drones
    ):

        st.info(
            f"""
🚁 **{safe_get(item, 'project')}**

🛩️ Platform:
{safe_get(item, 'platform')}

🎛️ Controller:
{safe_get(item, 'controller')}

📡 Sensor:
{safe_get(item, 'sensor')}

🧭 Navigation:
{safe_get(item, 'navigation')}

🎯 Mission:
{safe_get(item, 'mission')}

📅 Date:
{safe_get(item, 'due_date')}

⏰ Time:
{safe_get(item, 'due_time')}

🔔 Notification:
{'ON' if item.get('notification', False) else 'OFF'}
"""
        )

        if st.button(
            "🗑️ Delete Mission",
            key=f"delete_drone_{index}"
        ):

            st.session_state.drones.pop(
                index
            )

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 OMNI AI | Omni-Agentic Intelligent Automation System | "
    "Demo + Grok API | Streamlit + Python | No Database Dependency"
)
