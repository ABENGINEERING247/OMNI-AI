import os
from datetime import date, time, datetime

import requests
import streamlit as st

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
        "fired_notifications": set(),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# ============================================================
# SAFE DATA FUNCTIONS
# IMPORTANT: Prevents KeyError such as item["due_date"]
# ============================================================

def safe_value(item, key, default="Not specified"):
    if not isinstance(item, dict):
        return default

    value = item.get(key, default)

    if value is None:
        return default

    return value


def safe_date(item, key="due_date", default="Not set"):
    return safe_value(item, key, default)


def safe_time(item, key="due_time", default="Not set"):
    return safe_value(item, key, default)


def safe_bool(item, key="notification", default=False):
    return bool(safe_value(item, key, default))


# ============================================================
# OMNI AI HEADER
# ============================================================

st.markdown(
    """
    <div style="
        background:linear-gradient(135deg,#111827,#1f2937);
        padding:30px;
        border-radius:20px;
        margin-bottom:25px;
        text-align:center;
        border:1px solid #374151;
    ">

        <div style="
            font-size:46px;
            font-weight:700;
            color:white;
        ">
            🤖 OMNI AI
        </div>

        <div style="
            font-size:25px;
            font-weight:600;
            color:#d1d5db;
            margin-top:8px;
        ">
            Omni-Agentic Intelligent Automation System
        </div>

        <div style="
            font-size:16px;
            color:#9ca3af;
            margin-top:12px;
        ">
            10 AI Agents &nbsp;•&nbsp;
            Demo Mode &nbsp;•&nbsp;
            Grok API Mode
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


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
# NOTIFICATION ENGINE
# ============================================================

def notification_id(category, title, due_date, due_time):
    return f"{category}|{title}|{due_date}|{due_time}"


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

                if (Notification.permission === "default") {{
                    Notification.requestPermission();
                }}

                if (Notification.permission === "granted") {{
                    new Notification("🤖 OMNI AI Reminder", {{
                        body: '{text}'
                    }});
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

        if not safe_bool(
            item,
            "notification",
            False
        ):
            continue

        item_date = safe_value(
            item,
            date_key,
            None
        )

        item_time = safe_value(
            item,
            time_key,
            None
        )

        title = str(
            safe_value(
                item,
                title_key,
                category
            )
        )

        if item_date is None or item_time is None:
            continue

        try:

            if item_date == today and item_time <= current_time:

                nid = notification_id(
                    category,
                    title,
                    item_date,
                    item_time
                )

                if nid not in st.session_state.fired_notifications:

                    st.session_state.fired_notifications.add(nid)

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
        notifications
    )

    check_items(
        st.session_state.meetings,
        "Meeting",
        "title",
        "date",
        "time",
        "📅",
        notifications
    )

    check_items(
        st.session_state.tasks,
        "Task",
        "task",
        "due_date",
        "due_time",
        "📝",
        notifications
    )

    check_items(
        st.session_state.learning,
        "Learning",
        "subject",
        "due_date",
        "due_time",
        "📚",
        notifications
    )

    check_items(
        st.session_state.wellness,
        "Wellness",
        "activity",
        "due_date",
        "due_time",
        "❤️",
        notifications
    )

    check_items(
        st.session_state.expenses,
        "Finance",
        "description",
        "due_date",
        "due_time",
        "💰",
        notifications
    )

    check_items(
        st.session_state.communications,
        "Communication",
        "subject",
        "due_date",
        "due_time",
        "🌐",
        notifications
    )

    check_items(
        st.session_state.robotics,
        "Robotics",
        "project",
        "due_date",
        "due_time",
        "🤖",
        notifications
    )

    check_items(
        st.session_state.drones,
        "Drone",
        "project",
        "due_date",
        "due_time",
        "🚁",
        notifications
    )

    for message in notifications:

        st.toast(
            message,
            icon="🔔"
        )

        browser_notification(message)

    if notifications:

        st.warning(
            "🔔 **OMNI AI NOTIFICATION**\n\n"
            + "\n\n".join(
                f"- {x}"
                for x in notifications
            )
        )


# Refresh application every 15 seconds
if AUTO_REFRESH_AVAILABLE:

    st_autorefresh(
        interval=15000,
        key="omni_refresh"
    )

run_notification_engine()


# ============================================================
# GROK API
# ============================================================

def get_api_key():

    try:
        return st.secrets.get(
            "XAI_API_KEY",
            ""
        )

    except Exception:

        return os.getenv(
            "XAI_API_KEY",
            ""
        )


def call_grok(
    request,
    agent,
    api_key
):

    url = "https://api.x.ai/v1/chat/completions"

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
                "role": "system",

                "content": (
                    "You are OMNI AI, a "
                    "multi-agent intelligent "
                    "assistant. "

                    f"The selected specialist "
                    f"is {agent}. "

                    "Provide practical, "
                    "structured and useful "
                    "responses."
                ),
            },

            {
                "role": "user",
                "content": request,
            },
        ],

        "temperature": 0.3,
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

    return data[
        "choices"
    ][0][
        "message"
    ][
        "content"
    ]


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

    for keywords, agent in rules:

        if any(
            word in text
            for word in keywords
        ):

            return agent

    return "🧠 AI Orchestrator"


# ============================================================
# DEMO RESPONSE
# ============================================================

def demo_response(
    request,
    agent
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

**Request:** {request}

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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 OMNI AI")

    st.caption(
        "Agent Navigation"
    )

    page = st.radio(

        "Select Module",

        [
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
    )

    st.divider()

    mode = st.radio(

        "Operating Mode",

        [
            "🎮 Demo Mode",
            "🔑 Grok API Mode"
        ]
    )

    api_key = get_api_key()

    if mode == "🔑 Grok API Mode":

        if api_key:

            st.success(
                "🔑 XAI_API_KEY detected."
            )

        else:

            st.warning(
                "XAI_API_KEY not configured."
            )

    st.divider()

    st.subheader("📊 Data")

    counts = [

        (
            "Meetings",
            "meetings"
        ),

        (
            "Reminders",
            "reminders"
        ),

        (
            "Tasks",
            "tasks"
        ),

        (
            "Learning",
            "learning"
        ),

        (
            "Wellness",
            "wellness"
        ),

        (
            "Expenses",
            "expenses"
        ),

        (
            "Robotics",
            "robotics"
        ),

        (
            "Drones",
            "drones"
        ),
    ]

    for label, key in counts:

        st.write(
            f"{label}: "
            f"**{len(st.session_state[key])}**"
        )

    st.divider()

    if st.button(
        "🗑️ Clear All Demo Data"
    ):

        for key in [

            "meetings",
            "reminders",
            "tasks",
            "learning",
            "wellness",
            "expenses",
            "communications",
            "robotics",
            "drones",
        ]:

            st.session_state[key] = []

        st.session_state.fired_notifications = set()

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header(
        "📊 OMNI AI Dashboard"
    )

    st.write(
        "Centralized multi-agent "
        "AI assistant with Demo "
        "Mode and Grok API Mode."
    )

    cols = st.columns(4)

    cols[0].metric(
        "📅 Meetings",
        len(st.session_state.meetings)
    )

    cols[1].metric(
        "⏰ Reminders",
        len(st.session_state.reminders)
    )

    cols[2].metric(
        "📝 Tasks",
        len(st.session_state.tasks)
    )

    cols[3].metric(
        "🤖 Robotics",
        len(st.session_state.robotics)
    )

    st.divider()

    st.subheader(
        "🔄 Architecture"
    )

    st.code(
        """User Request
      ↓
Streamlit UI
      ↓
AI Orchestrator
      ↓
Specialized Agent
      ↓
Demo Engine / Grok API
      ↓
Task / Schedule Data
      ↓
Due Date + Due Time
      ↓
🔔 Notification
      ↓
User""",
        language="text"
    )

    st.subheader(
        "🤖 AI Agents"
    )

    for name, description in AGENTS.items():

        st.info(
            f"**{name}** — "
            f"{description}"
        )


# ============================================================
# AI ORCHESTRATOR
# ============================================================

elif page == "🧠 AI Orchestrator":

    st.header(
        "🧠 AI Orchestrator / Master Agent"
    )

    request = st.text_area(

        "💬 Ask OMNI AI",

        placeholder=(
            "Example: Create a meeting "
            "tomorrow at 10 AM and "
            "remind me."
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
                f"Selected Agent: {agent}"
            )

            if mode == "🎮 Demo Mode":

                st.markdown(
                    demo_response(
                        request,
                        agent
                    )
                )

            else:

                if not api_key:

                    st.error(
                        "Add XAI_API_KEY "
                        "in Streamlit Secrets."
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

                    except Exception as e:

                        st.error(
                            str(e)
                        )


# ============================================================
# REMINDERS & ALARMS
# ============================================================

elif page == "⏰ Reminders & Alarms":

    st.header(
        "⏰ Daily Reminder Agent"
    )

    with st.form(
        "reminder_form"
    ):

        title = st.text_input(
            "Reminder / Alarm Title"
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Due Date",
            value=date.today()
        )

        due_time = c2.time_input(
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

        submit = st.form_submit_button(
            "➕ Schedule Alarm"
        )

        if submit:

            if title.strip():

                st.session_state.reminders.append(

                    {
                        "title": title,

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
                    }
                )

                st.success(
                    "✅ Alarm scheduled."
                )

            else:

                st.warning(
                    "Enter a reminder title."
                )

    st.divider()

    if not st.session_state.reminders:

        st.info(
            "No reminders scheduled."
        )

    for i, item in enumerate(
        st.session_state.reminders
    ):

        st.info(

            f"⏰ **{safe_value(item, 'title')}**\n\n"

            f"📅 {safe_date(item)}  |  "

            f"🕐 {safe_time(item)}  |  "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}\n\n"

            f"🔁 "
            f"{safe_value(item, 'repeat')}  |  "

            f"⚡ "
            f"{safe_value(item, 'priority')}\n\n"

            f"📝 "
            f"{safe_value(item, 'notes', '')}"
        )

        if st.button(
            "🗑️ Delete",
            key=f"rem_{i}"
        ):

            st.session_state.reminders.pop(i)

            st.rerun()


# ============================================================
# CALENDAR & MEETINGS
# ============================================================

elif page == "📅 Calendar & Meetings":

    st.header(
        "📅 Calendar & Schedule Agent"
    )

    with st.form(
        "meeting_form"
    ):

        title = st.text_input(
            "Meeting / Event Title"
        )

        c1, c2 = st.columns(2)

        meeting_date = c1.date_input(
            "📅 Date",
            value=date.today()
        )

        meeting_time = c2.time_input(
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

        event_type = st.selectbox(
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

        submit = st.form_submit_button(
            "➕ Add to Calendar"
        )

        if submit:

            if title.strip():

                st.session_state.meetings.append(

                    {
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
                            event_type,

                        "notification":
                            notification,
                    }
                )

                st.success(
                    "✅ Meeting added."
                )

            else:

                st.warning(
                    "Enter a meeting title."
                )

    st.divider()

    if not st.session_state.meetings:

        st.info(
            "No meetings scheduled."
        )

    for i, item in enumerate(
        st.session_state.meetings
    ):

        st.info(

            f"📅 **{safe_value(item, 'title')}**\n\n"

            f"📅 "
            f"{safe_value(item, 'date')}  |  "

            f"⏰ "
            f"{safe_value(item, 'time')}\n\n"

            f"⏱️ "
            f"{safe_value(item, 'duration')} minutes  |  "

            f"📍 "
            f"{safe_value(item, 'location', '')}\n\n"

            f"👥 "
            f"{safe_value(item, 'participants', '')}  |  "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Meeting",
            key=f"meeting_{i}"
        ):

            st.session_state.meetings.pop(i)

            st.rerun()


# ============================================================
# LEARNING
# ============================================================

elif page == "📚 Learning":

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

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Study Date",
            value=date.today()
        )

        due_time = c2.time_input(
            "⏰ Study Time",
            value=time(18, 0)
        )

        notification = st.checkbox(
            "🔔 Study Notification",
            value=True
        )

        submit = st.form_submit_button(
            "➕ Add Learning Activity"
        )

        if submit:

            if subject.strip():

                st.session_state.learning.append(

                    {
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
                    }
                )

                st.success(
                    "✅ Learning activity added."
                )

            else:

                st.warning(
                    "Enter a subject."
                )

    for item in st.session_state.learning:

        st.info(

            f"📚 **"
            f"{safe_value(item, 'subject')}"
            f"**\n\n"

            f"🎯 "
            f"{safe_value(item, 'goal', '')}\n\n"

            f"📅 "
            f"{safe_date(item)}  |  "

            f"⏰ "
            f"{safe_time(item)}  |  "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}"
        )


# ============================================================
# TASKS
# ============================================================

elif page == "📝 Tasks & Productivity":

    st.header(
        "📝 Productivity & Task Management Agent"
    )

    with st.form(
        "task_form"
    ):

        task = st.text_input(
            "📝 Task"
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Due Date",
            value=date.today()
        )

        due_time = c2.time_input(
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

        submit = st.form_submit_button(
            "➕ Add Task"
        )

        if submit:

            if task.strip():

                st.session_state.tasks.append(

                    {
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
                    }
                )

                st.success(
                    "✅ Task added."
                )

            else:

                st.warning(
                    "Enter a task."
                )

    for i, item in enumerate(
        st.session_state.tasks
    ):

        item["completed"] = st.checkbox(

            f"✅ "
            f"{safe_value(item, 'task')}",

            value=bool(
                item.get(
                    "completed",
                    False
                )
            ),

            key=f"task_{i}"
        )

        st.caption(

            f"📅 "
            f"{safe_date(item)} | "

            f"⏰ "
            f"{safe_time(item)} | "

            f"⚡ "
            f"{safe_value(item, 'priority')} | "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}"
        )


# ============================================================
# WELLNESS
# ============================================================

elif page == "❤️ Wellness":

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

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Date",
            value=date.today()
        )

        due_time = c2.time_input(
            "⏰ Time",
            value=time(7, 0)
        )

        notification = st.checkbox(
            "🔔 Wellness Notification",
            value=True
        )

        submit = st.form_submit_button(
            "➕ Schedule Wellness Activity"
        )

        if submit:

            if activity.strip():

                st.session_state.wellness.append(

                    {
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
                    }
                )

                st.success(
                    "✅ Wellness activity scheduled."
                )

            else:

                st.warning(
                    "Enter an activity."
                )

    for item in st.session_state.wellness:

        st.info(

            f"❤️ **"
            f"{safe_value(item, 'activity')}"
            f"**\n\n"

            f"Type: "
            f"{safe_value(item, 'type')}\n\n"

            f"📅 "
            f"{safe_date(item)}  |  "

            f"⏰ "
            f"{safe_time(item)}  |  "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}"
        )


# ============================================================
# FINANCE
# ============================================================

elif page == "💰 Finance":

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

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Payment Date",
            value=date.today()
        )

        due_time = c2.time_input(
            "⏰ Payment Time",
            value=time(12, 0)
        )

        notification = st.checkbox(
            "🔔 Payment Notification",
            value=False
        )

        submit = st.form_submit_button(
            "➕ Add Expense"
        )

        if submit:

            if description.strip():

                st.session_state.expenses.append(

                    {
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
                    }
                )

                st.success(
                    "✅ Expense added."
                )

            else:

                st.warning(
                    "Enter a description."
                )

    total = sum(

        float(
            item.get(
                "amount",
                0
            ) or 0
        )

        for item in
        st.session_state.expenses

        if isinstance(item, dict)
    )

    st.metric(
        "💰 Total Expenses",
        f"{total:,.2f}"
    )

    for item in st.session_state.expenses:

        st.write(

            f"**"
            f"{safe_value(item, 'description')}"
            f"** — "

            f"{float(item.get('amount', 0) or 0):,.2f}"
            f" — "

            f"{safe_value(item, 'category')}"
            f" — "

            f"📅 "
            f"{safe_date(item)}"
            f" — "

            f"⏰ "
            f"{safe_time(item)}"
        )


# ============================================================
# COMMUNICATION
# ============================================================

elif page == "🌐 Communication":

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

    c1, c2 = st.columns(2)

    due_date = c1.date_input(
        "📅 Schedule Date",
        value=date.today()
    )

    due_time = c2.time_input(
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
            f"Dear Team,\n\n"
            f"{content}\n\n"
            f"Regards,\n"
            f"OMNI AI"
        )

        st.session_state.communications.append(

            {
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
            }
        )

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

elif page == "🤖 Robotics":

    st.header(
        "🤖 Robotics Agent"
    )

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

    components = [

        "Ultrasonic HC-SR04",
        "IR Sensor",
        "PIR Sensor",
        "LDR",
        "DHT11",
        "DHT22",
        "MPU6050",
        "MPU9250",
        "GPS Module",
        "RFID Reader",
        "Camera",
        "ESP32-CAM",
        "Raspberry Pi Camera",
        "LiDAR",
        "Encoder",
        "Load Cell",
        "Gas Sensor",
        "Soil Moisture Sensor",
        "OLED",
        "LCD",
        "Relay",
        "Servo Motor",
        "DC Motor",
        "Stepper Motor",
        "L298N",
        "L293D",
        "TB6612FNG",
        "PCA9685",
        "Bluetooth HC-05",
        "Bluetooth BLE",
        "Wi-Fi",
        "LoRa",
        "CAN Bus",
        "I2C",
        "SPI",
        "Ethernet",
        "Battery / Power Module",
        "Custom Component",
    ]

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
        "Gas",
        "Soil Moisture",
        "Encoder",
        "RFID",
        "Hall Effect",
        "Load Cell",
        "Custom Sensor",
    ]

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

    with st.form(
        "robotics_form"
    ):

        project = st.text_input(
            "🤖 Project Name"
        )

        c1, c2 = st.columns(2)

        controller = c1.selectbox(
            "🎛️ Controller",
            controllers
        )

        component = c2.selectbox(
            "🧩 Main Component",
            components
        )

        c3, c4 = st.columns(2)

        sensor = c3.selectbox(
            "📡 Sensor",
            sensors
        )

        actuator = c4.selectbox(
            "⚙️ Actuator",
            actuators
        )

        c5, c6 = st.columns(2)

        communication_type = c5.selectbox(
            "📶 Communication",
            communication
        )

        application = c6.selectbox(
            "🎯 Application",
            applications
        )

        objective = st.text_area(
            "🎯 Project Objective"
        )

        c7, c8 = st.columns(2)

        due_date = c7.date_input(
            "📅 Project / Review Date",
            value=date.today()
        )

        due_time = c8.time_input(
            "⏰ Project / Review Time",
            value=time(15, 0)
        )

        notification = st.checkbox(
            "🔔 Enable Robotics Notification",
            value=True
        )

        submit = st.form_submit_button(
            "➕ Add Robotics Project"
        )

        if submit:

            if project.strip():

                st.session_state.robotics.append(

                    {
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
                    }
                )

                st.success(
                    "✅ Robotics project added."
                )

            else:

                st.warning(
                    "Enter a project name."
                )

    st.divider()

    if not st.session_state.robotics:

        st.info(
            "No robotics projects added yet."
        )

    for i, item in enumerate(
        st.session_state.robotics
    ):

        st.info(

            f"🤖 **"
            f"{safe_value(item, 'project')}"
            f"**\n\n"

            f"🎛️ Controller: "
            f"{safe_value(item, 'controller')}\n\n"

            f"🧩 Component: "
            f"{safe_value(item, 'component')}\n\n"

            f"📡 Sensor: "
            f"{safe_value(item, 'sensor')}\n\n"

            f"⚙️ Actuator: "
            f"{safe_value(item, 'actuator')}\n\n"

            f"📶 Communication: "
            f"{safe_value(item, 'communication')}\n\n"

            f"🎯 Application: "
            f"{safe_value(item, 'application')}\n\n"

            f"📝 Objective: "
            f"{safe_value(item, 'objective', '')}\n\n"

            f"📅 Date: "
            f"{safe_date(item)}  |  "

            f"⏰ Time: "
            f"{safe_time(item)}  |  "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Robotics Project",
            key=f"robotics_{i}"
        ):

            st.session_state.robotics.pop(i)

            st.rerun()


# ============================================================
# DRONES & AUTONOMOUS SYSTEMS
# ============================================================

elif page == "🚁 Drones & Autonomous":

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

    controllers = [

        "Pixhawk",
        "ArduPilot",
        "PX4",
        "Raspberry Pi",
        "Jetson",
        "ESP32",
        "Custom Flight Controller",
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

    with st.form(
        "drone_form"
    ):

        project = st.text_input(
            "🚁 Mission / Project"
        )

        c1, c2 = st.columns(2)

        platform = c1.selectbox(
            "🛩️ Platform",
            platforms
        )

        controller = c2.selectbox(
            "🎛️ Controller",
            controllers
        )

        c3, c4 = st.columns(2)

        sensor = c3.selectbox(
            "📡 Primary Sensor",
            sensors
        )

        navigation = c4.selectbox(
            "🧭 Navigation",
            [
                "GPS",
                "GPS + IMU",
                "Visual Navigation",
                "LiDAR Navigation",
                "SLAM",
                "Manual",
                "Custom",
            ]
        )

        mission = st.text_area(
            "🎯 Mission Objective"
        )

        c5, c6 = st.columns(2)

        due_date = c5.date_input(
            "📅 Mission Date",
            value=date.today()
        )

        due_time = c6.time_input(
            "⏰ Mission Time",
            value=time(16, 0)
        )

        notification = st.checkbox(
            "🔔 Mission Notification",
            value=True
        )

        submit = st.form_submit_button(
            "➕ Add Mission"
        )

        if submit:

            if project.strip():

                st.session_state.drones.append(

                    {
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
                            mission,

                        "due_date":
                            due_date,

                        "due_time":
                            due_time,

                        "notification":
                            notification,
                    }
                )

                st.success(
                    "✅ Mission added."
                )

            else:

                st.warning(
                    "Enter a mission/project name."
                )

    st.divider()

    if not st.session_state.drones:

        st.info(
            "No autonomous missions added yet."
        )

    for i, item in enumerate(
        st.session_state.drones
    ):

        st.info(

            f"🚁 **"
            f"{safe_value(item, 'project')}"
            f"**\n\n"

            f"🛩️ Platform: "
            f"{safe_value(item, 'platform')}\n\n"

            f"🎛️ Controller: "
            f"{safe_value(item, 'controller')}\n\n"

            f"📡 Sensor: "
            f"{safe_value(item, 'sensor')}\n\n"

            f"🧭 Navigation: "
            f"{safe_value(item, 'navigation')}\n\n"

            f"🎯 Mission: "
            f"{safe_value(item, 'mission', '')}\n\n"

            f"📅 Date: "
            f"{safe_date(item)}  |  "

            f"⏰ Time: "
            f"{safe_time(item)}  |  "

            f"🔔 "
            f"{'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Mission",
            key=f"drone_{i}"
        ):

            st.session_state.drones.pop(i)

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 OMNI AI | "
    "Omni-Agentic Intelligent Automation System | "
    "10 AI Agents | "
    "Demo + Grok API Mode | "
    "Streamlit + Python | "
    "No Database Dependency"
)
