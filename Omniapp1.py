import os
import requests
import streamlit as st

# ==========================================================
# OMNI AI
# Omni-Agentic Intelligent Automation System
# Demo Mode + Grok API Mode
# ==========================================================

st.set_page_config(
    page_title="OMNI AI",
    page_icon="🤖",
    layout="wide"
)

# ==========================================================
# AGENTS
# ==========================================================

AGENTS = {
    "🧠 AI Orchestrator": "Central request analysis and agent coordination.",
    "⏰ Daily Reminder Agent": "Reminders, deadlines and daily routines.",
    "❤️ Health & Wellness Agent": "Wellness, fitness and appointment organization.",
    "📅 Calendar & Schedule Agent": "Meetings, events and schedule planning.",
    "📚 Learning & Education Agent": "Learning plans, courses and study schedules.",
    "📝 Productivity & Task Management Agent": "Tasks, priorities, projects and checklists.",
    "💰 Finance & Expense Management Agent": "Expenses, budgets and spending organization.",
    "🌐 Information & Communication Agent": "Emails, messages, reports and announcements.",
    "🤖 Robotics Agent": "Robotics, embedded systems, sensors and automation.",
    "🚁 Drones & Autonomous Systems Agent": "Drones, UAVs, navigation and autonomous systems."
}

# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# AGENT DETECTION
# ==========================================================

def detect_agent(request):

    text = request.lower()

    if any(word in text for word in [
        "reminder", "remind", "deadline", "routine", "alarm"
    ]):
        return "⏰ Daily Reminder Agent"

    if any(word in text for word in [
        "health", "fitness", "wellness", "exercise",
        "workout", "diet"
    ]):
        return "❤️ Health & Wellness Agent"

    if any(word in text for word in [
        "calendar", "schedule", "meeting", "appointment",
        "event", "timetable", "class"
    ]):
        return "📅 Calendar & Schedule Agent"

    if any(word in text for word in [
        "learn", "learning", "study", "education",
        "python", "course", "exam", "revision",
        "training", "lesson", "programming"
    ]):
        return "📚 Learning & Education Agent"

    if any(word in text for word in [
        "task", "tasks", "project", "productivity",
        "todo", "to-do", "checklist", "priority",
        "priorities"
    ]):
        return "📝 Productivity & Task Management Agent"

    if any(word in text for word in [
        "expense", "expenses", "budget", "money",
        "finance", "financial", "spending", "cost",
        "payment"
    ]):
        return "💰 Finance & Expense Management Agent"

    if any(word in text for word in [
        "email", "message", "announcement", "report",
        "letter", "communication", "draft"
    ]):
        return "🌐 Information & Communication Agent"

    if any(word in text for word in [
        "robot", "robotics", "arduino", "raspberry pi",
        "sensor", "motor", "embedded", "automation",
        "robotic arm"
    ]):
        return "🤖 Robotics Agent"

    if any(word in text for word in [
        "drone", "uav", "unmanned", "autonomous",
        "navigation", "flight", "quadcopter"
    ]):
        return "🚁 Drones & Autonomous Systems Agent"

    return "🧠 AI Orchestrator"


# ==========================================================
# DEMO RESPONSE
# ==========================================================

def demo_response(request, agent):

    responses = {

        "🧠 AI Orchestrator": (
            "## 🧠 AI Orchestrator\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "OMNI AI analyzed the request and routed it "
            "through the Master Agent.\n\n"
            "### Workflow\n\n"
            "1. Request received\n"
            "2. Request analyzed\n"
            "3. Agent selected\n"
            "4. Response generated\n\n"
            "✅ Orchestrator Demo completed."
        ),

        "⏰ Daily Reminder Agent": (
            "## ⏰ Daily Reminder Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Reminder Plan\n\n"
            "- Morning routine\n"
            "- Priority task reminder\n"
            "- Afternoon review\n"
            "- Evening daily review\n\n"
            "✅ Reminder Demo completed."
        ),

        "❤️ Health & Wellness Agent": (
            "## ❤️ Health & Wellness Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Wellness Plan\n\n"
            "- Morning activity\n"
            "- Hydration reminder\n"
            "- Exercise session\n"
            "- Rest period\n"
            "- Evening wellness review\n\n"
            "✅ Wellness Demo completed."
        ),

        "📅 Calendar & Schedule Agent": (
            "## 📅 Calendar & Schedule Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Schedule\n\n"
            "| Time | Activity |\n"
            "|---|---|\n"
            "| 09:00 | Meeting / Class |\n"
            "| 11:00 | Project Work |\n"
            "| 01:00 | Lunch |\n"
            "| 03:00 | Review |\n"
            "| 05:00 | Follow-up |\n\n"
            "✅ Calendar Demo completed."
        ),

        "📚 Learning & Education Agent": (
            "## 📚 Learning & Education Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Learning Roadmap\n\n"
            "1. Fundamentals\n"
            "2. Practical exercises\n"
            "3. Mini projects\n"
            "4. Advanced practice\n"
            "5. Final project\n\n"
            "✅ Learning Demo completed."
        ),

        "📝 Productivity & Task Management Agent": (
            "## 📝 Productivity & Task Management Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Workflow\n\n"
            "1. Identify tasks\n"
            "2. Set priorities\n"
            "3. Complete high-priority work\n"
            "4. Review progress\n"
            "5. Update remaining tasks\n\n"
            "✅ Productivity Demo completed."
        ),

        "💰 Finance & Expense Management Agent": (
            "## 💰 Finance & Expense Management Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Categories\n\n"
            "- Food\n"
            "- Transport\n"
            "- Education\n"
            "- Utilities\n"
            "- Other\n\n"
            "✅ Finance Demo completed."
        ),

        "🌐 Information & Communication Agent": (
            "## 🌐 Information & Communication Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Communication\n\n"
            "Dear Team,\n\n"
            "This is a demonstration communication generated "
            "by OMNI AI.\n\n"
            "Regards,\n"
            "OMNI AI\n\n"
            "✅ Communication Demo completed."
        ),

        "🤖 Robotics Agent": (
            "## 🤖 Robotics Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Robotics Architecture\n\n"
            "Sensors\n"
            "↓\n"
            "Microcontroller / Raspberry Pi\n"
            "↓\n"
            "AI Processing\n"
            "↓\n"
            "Decision Making\n"
            "↓\n"
            "Motor Controller\n"
            "↓\n"
            "Robot Actuators\n\n"
            "### Components\n\n"
            "- Raspberry Pi\n"
            "- Arduino / ESP32\n"
            "- Camera\n"
            "- Sensors\n"
            "- Motor Driver\n"
            "- Motors\n\n"
            "✅ Robotics Demo completed."
        ),

        "🚁 Drones & Autonomous Systems Agent": (
            "## 🚁 Drones & Autonomous Systems Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Autonomous Architecture\n\n"
            "Camera / Sensors\n"
            "↓\n"
            "Perception\n"
            "↓\n"
            "AI Decision System\n"
            "↓\n"
            "Navigation\n"
            "↓\n"
            "Flight Controller\n"
            "↓\n"
            "Actuators\n\n"
            "### Capabilities\n\n"
            "- Object detection\n"
            "- Navigation\n"
            "- Obstacle detection\n"
            "- Path planning\n"
            "- Computer vision\n\n"
            "✅ Autonomous Systems Demo completed."
        )
    }

    return responses.get(
        agent,
        responses["🧠 AI Orchestrator"]
    )


# ==========================================================
# GROK API
# ==========================================================

def grok_response(request, agent, api_key):

    url = "https://api.x.ai/v1/chat/completions"

    system_prompt = (
        "You are OMNI AI, an intelligent multi-agent "
        "automation system. You have a central AI "
        "Orchestrator and specialized agents. "
        "The selected agent for this request is: "
        + agent
        + ". Respond as that specialized agent. "
        "Give practical, structured and useful answers. "
        "Do not claim that an action was actually performed "
        "unless the application has a real tool for that action."
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

    mode = st.radio(
        "Operating Mode",
        [
            "🎮 Demo Mode",
            "🔑 Grok API Mode"
        ]
    )

    st.divider()

    st.subheader("AI Agents")

    for agent_name in AGENTS:
        st.write(agent_name)

    st.divider()

    st.caption(
        "Omni-Agentic Intelligent Automation System"
    )


# ==========================================================
# MAIN
# ==========================================================

st.title("🤖 OMNI AI")

st.subheader(
    "Omni-Agentic Intelligent Automation System"
)

st.write(
    "Centralized multi-agent AI assistant powered by "
    "Streamlit, Python and Grok AI."
)


# ==========================================================
# API KEY
# ==========================================================

api_key = ""

if mode == "🔑 Grok API Mode":

    st.info(
        "🔑 Grok API Mode is active."
    )

    # Streamlit Cloud Secrets
    try:

        api_key = st.secrets["XAI_API_KEY"]

    except Exception:

        api_key = ""

    # Local fallback
    if not api_key:

        api_key = os.getenv(
            "XAI_API_KEY",
            ""
        )

    if api_key:

        st.success(
            "✅ Grok API key detected."
        )

    else:

        st.warning(
            "⚠️ XAI_API_KEY not found. "
            "Add it in Streamlit Secrets."
        )

else:

    st.success(
        "🎮 Demo Mode Active — "
        "No API key required."
    )


# ==========================================================
# AGENT DASHBOARD
# ==========================================================

st.divider()

st.subheader("🚀 Available AI Agents")

col1, col2 = st.columns(2)

items = list(AGENTS.items())

for index, item in enumerate(items):

    name = item[0]
    description = item[1]

    with col1 if index % 2 == 0 else col2:

        st.info(
            "**"
            + name
            + "**\n\n"
            + description
        )


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ==========================================================
# USER REQUEST
# ==========================================================

request = st.chat_input(
    "Ask OMNI AI anything..."
)


if request:

    with st.chat_message("user"):

        st.markdown(request)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": request
        }
    )

    # Agent selection

    selected_agent = detect_agent(
        request
    )

    st.success(
        "🧠 AI Orchestrator selected: **"
        + selected_agent
        + "**"
    )

    # Generate response

    with st.chat_message("assistant"):

        if mode == "🎮 Demo Mode":

            response = demo_response(
                request,
                selected_agent
            )

            st.markdown(response)

        else:

            if not api_key:

                response = (
                    "⚠️ Grok API key is not configured.\n\n"
                    "Please add **XAI_API_KEY** to "
                    "Streamlit Secrets."
                )

                st.warning(response)

            else:

                try:

                    with st.spinner(
                        "🤖 OMNI AI is thinking..."
                    ):

                        response = grok_response(
                            request,
                            selected_agent,
                            api_key
                        )

                    st.markdown(response)

                except Exception as error:

                    response = (
                        "❌ Grok API request failed.\n\n"
                        + str(error)
                    )

                    st.error(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "OMNI AI | Demo Mode + Grok API Mode | "
    "10 Specialized AI Agents"
)