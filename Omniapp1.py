import os
import requests
from datetime import datetime, date, time

import streamlit as st


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
# HEADER
# ==========================================================

st.title("🤖 OMNI AI")
st.subheader("Omni-Agentic Intelligent Automation System")
st.write("Grok-Powered Multi-Agent AI Solution")
st.caption(
    "10 Specialized AI Agents • Demo Mode • Grok API Mode • Streamlit"
)
st.divider()


# ==========================================================
# AGENTS
# ==========================================================

AGENTS = {
    "⏰ Daily Reminder Agent":
        "Manages reminders, alarms, deadlines and routines.",

    "❤️ Health & Wellness Agent":
        "Manages wellness activities, fitness and appointments.",

    "📅 Calendar & Schedule Agent":
        "Manages meetings, events, classes and appointments.",

    "📚 Learning & Education Agent":
        "Creates study plans, learning activities and revision schedules.",

    "📝 Productivity & Task Management Agent":
        "Manages tasks, priorities, projects and checklists.",

    "💰 Finance & Expense Management Agent":
        "Manages demo expenses, budgets and spending summaries.",

    "🌐 Information & Communication Agent":
        "Creates emails, messages, announcements and reports.",

    "🤖 Robotics Agent":
        "Supports robotics, embedded systems, sensors and automation.",

    "🚁 Drones & Autonomous Systems Agent":
        "Supports drones, UAVs, navigation and autonomous systems."
}


# ==========================================================
# SESSION STATE
# ==========================================================

if "meetings" not in st.session_state:
    st.session_state.meetings = []

if "reminders" not in st.session_state:
    st.session_state.reminders = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "learning" not in st.session_state:
    st.session_state.learning = []

if "wellness" not in st.session_state:
    st.session_state.wellness = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "robotics_projects" not in st.session_state:
    st.session_state.robotics_projects = []

if "drone_projects" not in st.session_state:
    st.session_state.drone_projects = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================================
# AGENT DETECTION
# ==========================================================

def detect_agent(request):

    text = request.lower()

    if any(x in text for x in [
        "reminder", "remind", "alarm", "deadline"
    ]):
        return "⏰ Daily Reminder Agent"

    if any(x in text for x in [
        "health", "fitness", "wellness",
        "exercise", "workout"
    ]):
        return "❤️ Health & Wellness Agent"

    if any(x in text for x in [
        "calendar", "meeting", "schedule",
        "appointment", "event", "class"
    ]):
        return "📅 Calendar & Schedule Agent"

    if any(x in text for x in [
        "learn", "learning", "study",
        "education", "python", "course",
        "exam", "revision", "training"
    ]):
        return "📚 Learning & Education Agent"

    if any(x in text for x in [
        "task", "todo", "to-do",
        "project", "productivity",
        "checklist", "priority"
    ]):
        return "📝 Productivity & Task Management Agent"

    if any(x in text for x in [
        "expense", "expenses", "budget",
        "finance", "money", "spending",
        "payment", "cost"
    ]):
        return "💰 Finance & Expense Management Agent"

    if any(x in text for x in [
        "email", "message", "announcement",
        "report", "letter", "communication"
    ]):
        return "🌐 Information & Communication Agent"

    if any(x in text for x in [
        "robot", "robotics", "arduino",
        "raspberry pi", "sensor", "motor",
        "embedded", "robotic arm"
    ]):
        return "🤖 Robotics Agent"

    if any(x in text for x in [
        "drone", "uav", "autonomous",
        "navigation", "quadcopter",
        "flight"
    ]):
        return "🚁 Drones & Autonomous Systems Agent"

    return "🧠 AI Orchestrator"


# ==========================================================
# DEMO RESPONSE
# ==========================================================

def demo_response(request, agent):

    if agent == "⏰ Daily Reminder Agent":
        return f"""
## ⏰ Daily Reminder Agent

**Request:** {request}

### Demo Capabilities

- Create reminder
- Create alarm
- Set deadline
- Manage recurring routine
- Organize daily activities
- Review upcoming reminders

✅ Demo Reminder Agent processed your request.
"""

    if agent == "📅 Calendar & Schedule Agent":
        return f"""
## 📅 Calendar & Schedule Agent

**Request:** {request}

### Demo Capabilities

- Create meeting
- Create appointment
- Create class
- Create event
- Organize daily schedule
- Review upcoming calendar
- Detect basic scheduling conflicts

✅ Demo Calendar Agent processed your request.
"""

    if agent == "📚 Learning & Education Agent":
        return f"""
## 📚 Learning & Education Agent

**Request:** {request}

### Demo Learning Workflow

1. Identify learning objective
2. Create roadmap
3. Divide into activities
4. Schedule study
5. Review progress

### Example

**Python + AI Learning**

Week 1 → Python Fundamentals  
Week 2 → Data & Machine Learning  
Week 3 → Generative AI  
Week 4 → Agentic AI Project

✅ Demo Learning Agent processed your request.
"""

    if agent == "📝 Productivity & Task Management Agent":
        return f"""
## 📝 Productivity & Task Management Agent

**Request:** {request}

### Demo Workflow

1. Capture task
2. Assign priority
3. Set deadline
4. Track completion
5. Review productivity

✅ Demo Productivity Agent processed your request.
"""

    if agent == "💰 Finance & Expense Management Agent":
        return f"""
## 💰 Finance & Expense Management Agent

**Request:** {request}

### Demo Capabilities

- Add expense
- Categorize expense
- Calculate totals
- Review spending
- Create budget summary

⚠️ Demo financial data only.

✅ Demo Finance Agent processed your request.
"""

    if agent == "❤️ Health & Wellness Agent":
        return f"""
## ❤️ Health & Wellness Agent

**Request:** {request}

### Demo Wellness Plan

- Morning activity
- Hydration
- Fitness activity
- Rest
- Evening review

⚠️ General wellness organization only.

✅ Demo Wellness Agent processed your request.
"""

    if agent == "🌐 Information & Communication Agent":
        return f"""
## 🌐 Information & Communication Agent

**Request:** {request}

### Demo Communication Workflow

Understand → Draft → Structure → Review → Finalize

### Example

**Subject: AI Workshop**

Dear Team,

This is a demonstration announcement generated
by OMNI AI.

Regards,  
OMNI AI

✅ Demo Communication Agent processed your request.
"""

    if agent == "🤖 Robotics Agent":
        return f"""
## 🤖 Robotics Agent

**Request:** {request}

### Demo Robotics Architecture

Sensors
↓
ESP32 / Arduino / Raspberry Pi
↓
AI Processing
↓
Decision Making
↓
Motor Controller
↓
Robot Actuators

### Demo Components

- ESP32
- Raspberry Pi
- Camera
- Ultrasonic Sensor
- Motor Driver
- Motors
- Battery

✅ Demo Robotics Agent processed your request.
"""

    if agent == "🚁 Drones & Autonomous Systems Agent":
        return f"""
## 🚁 Drones & Autonomous Systems Agent

**Request:** {request}

### Demo Autonomous Architecture

Camera / Sensors
↓
Computer Vision
↓
AI Decision
↓
Navigation
↓
Flight Controller
↓
Actuators

### Demo Capabilities

- Object detection
- Navigation
- Obstacle avoidance
- Path planning
- Autonomous inspection

✅ Demo Autonomous Systems Agent processed your request.
"""

    return f"""
## 🧠 AI Orchestrator

**Request:** {request}

### Agentic Workflow

User Request
↓
Request Analysis
↓
Agent Selection
↓
Specialized Agent
↓
Response Generation

**Selected Agent:** {agent}

✅ Demo Orchestration completed.
"""


# ==========================================================
# GROK API
# ==========================================================

def grok_response(request, agent, api_key):

    url = "https://api.x.ai/v1/chat/completions"

    system_prompt = f"""
You are OMNI AI, an intelligent multi-agent AI platform.

The selected specialized agent is:
{agent}

Provide a structured, practical response.

Do not claim that a real-world action was completed
unless an actual external integration exists.

You are currently operating through the OMNI AI
Streamlit application.
"""

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

    if response.status_code != 200:

        if response.status_code == 403:
            raise Exception(
                "Grok API credits or monthly spending limit "
                "may have been reached. Please check xAI "
                "billing/usage. Demo Mode remains available."
            )

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

    st.subheader("📊 Demo Statistics")

    st.write(
        "Meetings:",
        len(st.session_state.meetings)
    )

    st.write(
        "Reminders:",
        len(st.session_state.reminders)
    )

    st.write(
        "Tasks:",
        len(st.session_state.tasks)
    )

    st.write(
        "Expenses:",
        len(st.session_state.expenses)
    )

    st.divider()

    if st.button("🗑️ Clear All Demo Data"):

        st.session_state.meetings = []
        st.session_state.reminders = []
        st.session_state.tasks = []
        st.session_state.expenses = []
        st.session_state.learning = []
        st.session_state.wellness = []
        st.session_state.messages = []
        st.session_state.robotics_projects = []
        st.session_state.drone_projects = []

        st.success("Demo data cleared.")
        st.rerun()


# ==========================================================
# API KEY
# ==========================================================

api_key = ""

if mode == "🔑 Grok API Mode":

    try:
        api_key = st.secrets["XAI_API_KEY"]
    except Exception:
        api_key = os.getenv("XAI_API_KEY", "")


# ==========================================================
# DASHBOARD
# ==========================================================

if selected == "🏠 Dashboard":

    st.header("📊 OMNI AI Demo Dashboard")

    st.write(
        "Central control panel for the OMNI AI "
        "multi-agent system."
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
        total = sum(
            x["amount"]
            for x in st.session_state.expenses
        )

        st.metric(
            "💰 Expenses",
            f"{total:,.0f}"
        )

    st.divider()

    st.subheader("🤖 System Architecture")

    st.write(
        "User → Streamlit → AI Orchestrator → "
        "Specialized Agent → Grok / Demo Engine → Response"
    )

    st.divider()

    st.subheader("🚀 Available Demo Modules")

    cols = st.columns(3)

    modules = [
        "📅 Calendar & Meetings",
        "⏰ Reminders & Alarms",
        "📝 Tasks",
        "💰 Expenses",
        "📚 Learning",
        "❤️ Wellness",
        "🌐 Communication",
        "🤖 Robotics",
        "🚁 Autonomous Systems"
    ]

    for i, module in enumerate(modules):

        with cols[i % 3]:
            st.info(module)


# ==========================================================
# ORCHESTRATOR
# ==========================================================

elif selected == "🧠 AI Orchestrator":

    st.header("🧠 AI Orchestrator")

    st.write(
        "Enter a natural-language request and OMNI AI "
        "will select the appropriate agent."
    )

    request = st.text_area(
        "Your Request",
        placeholder=(
            "Example: Schedule a meeting tomorrow at 10 AM "
            "and remind me 30 minutes before."
        )
    )

    if st.button("🚀 Process Request") and request:

        agent = detect_agent(request)

        st.success(
            "Selected Agent: " + agent
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
                    "XAI_API_KEY is not configured."
                )

            else:

                try:

                    with st.spinner(
                        "OMNI AI is thinking..."
                    ):

                        result = grok_response(
                            request,
                            agent,
                            api_key
                        )

                    st.markdown(result)

                except Exception as error:

                    st.error(str(error))


# ==========================================================
# REMINDERS & ALARMS
# ==========================================================

elif selected == "⏰ Reminders & Alarms":

    st.header("⏰ Reminders & Alarms")

    st.write(
        "Create and manage demo reminders and alarms."
    )

    with st.form("reminder_form"):

        title = st.text_input(
            "Reminder / Alarm Title"
        )

        reminder_date = st.date_input(
            "Date",
            value=date.today()
        )

        reminder_time = st.time_input(
            "Time",
            value=time(9, 0)
        )

        repeat = st.selectbox(
            "Repeat",
            [
                "Once",
                "Daily",
                "Weekly",
                "Weekdays"
            ]
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        submitted = st.form_submit_button(
            "➕ Add Reminder"
        )

        if submitted:

            if title:

                st.session_state.reminders.append(
                    {
                        "title": title,
                        "date": reminder_date,
                        "time": reminder_time,
                        "repeat": repeat,
                        "priority": priority
                    }
                )

                st.success(
                    "Reminder added successfully."
                )

            else:

                st.warning(
                    "Please enter a reminder title."
                )

    st.divider()

    st.subheader("📋 Saved Reminders")

    if st.session_state.reminders:

        for i, item in enumerate(
            st.session_state.reminders
        ):

            st.info(
                f"⏰ **{item['title']}**\n\n"
                f"📅 {item['date']}  "
                f"🕐 {item['time']}\n\n"
                f"🔁 {item['repeat']}  |  "
                f"Priority: {item['priority']}"
            )

            if st.button(
                "Delete",
                key=f"delete_reminder_{i}"
            ):

                st.session_state.reminders.pop(i)
                st.rerun()

    else:

        st.info(
            "No reminders yet. Add your first reminder above."
        )


# ==========================================================
# CALENDAR & MEETINGS
# ==========================================================

elif selected == "📅 Calendar & Meetings":

    st.header("📅 Calendar & Meetings")

    st.write(
        "Create demo meetings, appointments, classes and events."
    )

    with st.form("meeting_form"):

        meeting_title = st.text_input(
            "Meeting / Event Title"
        )

        meeting_date = st.date_input(
            "Date",
            value=date.today()
        )

        meeting_time = st.time_input(
            "Start Time",
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
            "Location / Platform",
            placeholder="Conference Room / Zoom / Teams"
        )

        participants = st.text_input(
            "Participants"
        )

        meeting_type = st.selectbox(
            "Type",
            [
                "Meeting",
                "Class",
                "Appointment",
                "Event",
                "Project Review"
            ]
        )

        add_meeting = st.form_submit_button(
            "➕ Add to Calendar"
        )

        if add_meeting:

            if meeting_title:

                st.session_state.meetings.append(
                    {
                        "title": meeting_title,
                        "date": meeting_date,
                        "time": meeting_time,
                        "duration": duration,
                        "location": location,
                        "participants": participants,
                        "type": meeting_type
                    }
                )

                st.success(
                    "Calendar item added."
                )

            else:

                st.warning(
                    "Please enter meeting/event title."
                )

    st.divider()

    st.subheader("📆 Upcoming Calendar")

    if st.session_state.meetings:

        sorted_meetings = sorted(
            st.session_state.meetings,
            key=lambda x: (
                x["date"],
                x["time"]
            )
        )

        for i, meeting in enumerate(
            sorted_meetings
        ):

            st.info(
                f"📌 **{meeting['title']}**\n\n"
                f"📅 {meeting['date']}  "
                f"🕐 {meeting['time']}\n\n"
                f"⏱️ {meeting['duration']} minutes\n\n"
                f"📍 {meeting['location'] or 'Not specified'}\n\n"
                f"👥 {meeting['participants'] or 'Not specified'}\n\n"
                f"🏷️ {meeting['type']}"
            )

    else:

        st.info(
            "Calendar is empty. Add a meeting or event above."
        )


# ==========================================================
# TASKS
# ==========================================================

elif selected == "📝 Tasks & Productivity":

    st.header("📝 Tasks & Productivity")

    with st.form("task_form"):

        task = st.text_input(
            "Task"
        )

        task_priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        task_due = st.date_input(
            "Due Date",
            value=date.today()
        )

        add_task = st.form_submit_button(
            "➕ Add Task"
        )

        if add_task and task:

            st.session_state.tasks.append(
                {
                    "task": task,
                    "priority": task_priority,
                    "due": task_due,
                    "completed": False
                }
            )

            st.success(
                "Task added."
            )

    st.divider()

    for i, item in enumerate(
        st.session_state.tasks
    ):

        completed = st.checkbox(
            item["task"],
            value=item["completed"],
            key=f"task_{i}"
        )

        item["completed"] = completed

        st.caption(
            f"Priority: {item['priority']} | "
            f"Due: {item['due']}"
        )


# ==========================================================
# FINANCE
# ==========================================================

elif selected == "💰 Finance":

    st.header("💰 Finance & Expense Manager")

    with st.form("expense_form"):

        description = st.text_input(
            "Expense Description"
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
                "Other"
            ]
        )

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        add_expense = st.form_submit_button(
            "➕ Add Expense"
        )

        if add_expense and description:

            st.session_state.expenses.append(
                {
                    "description": description,
                    "amount": amount,
                    "category": category,
                    "date": expense_date
                }
            )

            st.success(
                "Expense added."
            )

    st.divider()

    total = sum(
        x["amount"]
        for x in st.session_state.expenses
    )

    st.metric(
        "💰 Total Demo Expenses",
        f"{total:,.2f}"
    )

    if st.session_state.expenses:

        for item in st.session_state.expenses:

            st.write(
                f"**{item['description']}** — "
                f"{item['amount']:,.2f} — "
                f"{item['category']} — "
                f"{item['date']}"
            )


# ==========================================================
# LEARNING
# ==========================================================

elif selected == "📚 Learning":

    st.header("📚 Learning & Education Agent")

    with st.form("learning_form"):

        subject = st.text_input(
            "Subject / Course"
        )

        learning_goal = st.text_input(
            "Learning Goal"
        )

        duration = st.number_input(
            "Duration (days)",
            min_value=1,
            max_value=365,
            value=30
        )

        add_learning = st.form_submit_button(
            "➕ Add Learning Plan"
        )

        if add_learning and subject:

            st.session_state.learning.append(
                {
                    "subject": subject,
                    "goal": learning_goal,
                    "duration": duration
                }
            )

            st.success(
                "Learning plan created."
            )

    for item in st.session_state.learning:

        st.info(
            f"📚 **{item['subject']}**\n\n"
            f"Goal: {item['goal']}\n\n"
            f"Duration: {item['duration']} days"
        )


# ==========================================================
# WELLNESS
# ==========================================================

elif selected == "❤️ Wellness":

    st.header("❤️ Health & Wellness")

    with st.form("wellness_form"):

        activity = st.text_input(
            "Activity"
        )

        wellness_time = st.time_input(
            "Time",
            value=time(7, 0)
        )

        wellness_type = st.selectbox(
            "Type",
            [
                "Exercise",
                "Walking",
                "Hydration",
                "Meditation",
                "Appointment",
                "Other"
            ]
        )

        add_wellness = st.form_submit_button(
            "➕ Add Wellness Activity"
        )

        if add_wellness and activity:

            st.session_state.wellness.append(
                {
                    "activity": activity,
                    "time": wellness_time,
                    "type": wellness_type
                }
            )

            st.success(
                "Wellness activity added."
            )

    for item in st.session_state.wellness:

        st.info(
            f"❤️ **{item['activity']}** — "
            f"{item['time']} — {item['type']}"
        )


# ==========================================================
# COMMUNICATION
# ==========================================================

elif selected == "🌐 Communication":

    st.header("🌐 Information & Communication")

    communication_type = st.selectbox(
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
        "Message / Content"
    )

    if st.button("✍️ Generate Demo Draft"):

        draft = (
            f"## {communication_type}\n\n"
            f"**To:** {recipient}\n\n"
            f"**Subject:** {subject}\n\n"
            f"Dear Team,\n\n"
            f"{content}\n\n"
            f"Regards,\n"
            f"OMNI AI"
        )

        st.markdown(draft)


# ==========================================================
# ROBOTICS
# ==========================================================

elif selected == "🤖 Robotics":

    st.header("🤖 Robotics Agent")

    with st.form("robotics_form"):

        project = st.text_input(
            "Robotics Project"
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
            "Main Sensor"
        )

        objective = st.text_area(
            "Project Objective"
        )

        add_robot = st.form_submit_button(
            "➕ Create Demo Project"
        )

        if add_robot and project:

            st.session_state.robotics_projects.append(
                {
                    "project": project,
                    "controller": controller,
                    "sensor": sensor,
                    "objective": objective
                }
            )

            st.success(
                "Robotics project created."
            )

    for item in st.session_state.robotics_projects:

        st.info(
            f"🤖 **{item['project']}**\n\n"
            f"Controller: {item['controller']}\n\n"
            f"Sensor: {item['sensor']}\n\n"
            f"Objective: {item['objective']}"
        )


# ==========================================================
# DRONES
# ==========================================================

elif selected == "🚁 Drones & Autonomous":

    st.header("🚁 Drones & Autonomous Systems")

    with st.form("drone_form"):

        project = st.text_input(
            "Autonomous Project"
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
            "Sensor / Camera"
        )

        mission = st.text_area(
            "Mission Objective"
        )

        add_drone = st.form_submit_button(
            "➕ Create Demo Mission"
        )

        if add_drone and project:

            st.session_state.drone_projects.append(
                {
                    "project": project,
                    "platform": platform,
                    "sensor": sensor,
                    "mission": mission
                }
            )

            st.success(
                "Autonomous mission created."
            )

    for item in st.session_state.drone_projects:

        st.info(
            f"🚁 **{item['project']}**\n\n"
            f"Platform: {item['platform']}\n\n"
            f"Sensor: {item['sensor']}\n\n"
            f"Mission: {item['mission']}"
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "🤖 OMNI AI | Omni-Agentic Intelligent Automation System | "
    "10 AI Agents | Demo + Grok API Mode | Database-Free Demo"
)
