import os
import requests
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
# HEADER / BANNER
# ==========================================================

st.title("🤖 OMNI AI")

st.subheader(
    "Omni-Agentic Intelligent Automation System"
)

st.write(
    "Grok-Powered Multi-Agent AI Solution"
)

st.caption(
    "10 Specialized AI Agents  •  Demo Mode  •  "
    "Grok API Mode  •  Streamlit"
)

st.divider()


# ==========================================================
# AGENT DEFINITIONS
# ==========================================================

AGENTS = {

    "⏰ Daily Reminder Agent":
        "Manages reminders, deadlines, routines and daily activities.",

    "❤️ Health & Wellness Agent":
        "Organizes wellness routines, fitness activities and appointments.",

    "📅 Calendar & Schedule Agent":
        "Manages meetings, classes, events, appointments and schedules.",

    "📚 Learning & Education Agent":
        "Creates learning plans, study schedules, courses and revision plans.",

    "📝 Productivity & Task Management Agent":
        "Manages tasks, priorities, projects, notes and checklists.",

    "💰 Finance & Expense Management Agent":
        "Organizes user-provided expenses, budgets and spending summaries.",

    "🌐 Information & Communication Agent":
        "Creates emails, messages, reports, announcements and summaries.",

    "🤖 Robotics Agent":
        "Provides assistance for robotics, embedded systems, sensors and automation.",

    "🚁 Drones & Autonomous Systems Agent":
        "Supports UAVs, drones, navigation, computer vision and autonomous systems."
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
        "reminder",
        "remind",
        "deadline",
        "routine",
        "alarm"
    ]):
        return "⏰ Daily Reminder Agent"

    if any(word in text for word in [
        "health",
        "fitness",
        "wellness",
        "exercise",
        "workout",
        "diet"
    ]):
        return "❤️ Health & Wellness Agent"

    if any(word in text for word in [
        "calendar",
        "schedule",
        "meeting",
        "appointment",
        "event",
        "timetable",
        "class"
    ]):
        return "📅 Calendar & Schedule Agent"

    if any(word in text for word in [
        "learn",
        "learning",
        "study",
        "education",
        "python",
        "course",
        "exam",
        "revision",
        "training",
        "lesson",
        "programming",
        "artificial intelligence",
        "machine learning",
        "deep learning"
    ]):
        return "📚 Learning & Education Agent"

    if any(word in text for word in [
        "task",
        "tasks",
        "project",
        "productivity",
        "todo",
        "to-do",
        "checklist",
        "priority",
        "priorities"
    ]):
        return "📝 Productivity & Task Management Agent"

    if any(word in text for word in [
        "expense",
        "expenses",
        "budget",
        "money",
        "finance",
        "financial",
        "spending",
        "cost",
        "payment"
    ]):
        return "💰 Finance & Expense Management Agent"

    if any(word in text for word in [
        "email",
        "message",
        "announcement",
        "report",
        "letter",
        "communication",
        "draft"
    ]):
        return "🌐 Information & Communication Agent"

    if any(word in text for word in [
        "robot",
        "robotics",
        "arduino",
        "raspberry pi",
        "sensor",
        "motor",
        "embedded",
        "automation",
        "robotic arm"
    ]):
        return "🤖 Robotics Agent"

    if any(word in text for word in [
        "drone",
        "uav",
        "unmanned",
        "autonomous",
        "navigation",
        "flight",
        "quadcopter"
    ]):
        return "🚁 Drones & Autonomous Systems Agent"

    return "🧠 AI Orchestrator"


# ==========================================================
# DEMO RESPONSE
# ==========================================================

def demo_response(request, agent):

    if agent == "🧠 AI Orchestrator":

        return (
            "## 🧠 AI Orchestrator\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Agentic Workflow\n\n"
            "1. User request received\n"
            "2. Request analyzed\n"
            "3. Appropriate agent identified\n"
            "4. Agent processing initiated\n"
            "5. Response generated\n\n"
            "✅ Demo Orchestration completed."
        )

    if agent == "⏰ Daily Reminder Agent":

        return (
            "## ⏰ Daily Reminder Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Reminder Plan\n\n"
            "- Morning routine\n"
            "- Important task reminder\n"
            "- Deadline reminder\n"
            "- Afternoon activity\n"
            "- Evening review\n\n"
            "### Workflow\n\n"
            "Identify → Prioritize → Schedule → Remind\n\n"
            "✅ Reminder Demo completed."
        )

    if agent == "❤️ Health & Wellness Agent":

        return (
            "## ❤️ Health & Wellness Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Wellness Plan\n\n"
            "- Morning activity\n"
            "- Hydration\n"
            "- Fitness session\n"
            "- Rest period\n"
            "- Evening wellness review\n\n"
            "### Workflow\n\n"
            "Identify → Organize → Schedule → Review\n\n"
            "✅ Wellness Demo completed.\n\n"
            "> General wellness organization only; "
            "not a substitute for professional medical advice."
        )

    if agent == "📅 Calendar & Schedule Agent":

        return (
            "## 📅 Calendar & Schedule Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Schedule\n\n"
            "| Time | Activity |\n"
            "|---|---|\n"
            "| 09:00 AM | Meeting / Class |\n"
            "| 11:00 AM | Project Work |\n"
            "| 01:00 PM | Break |\n"
            "| 03:00 PM | Review |\n"
            "| 05:00 PM | Follow-up |\n\n"
            "### Workflow\n\n"
            "Identify → Schedule → Organize → Review\n\n"
            "✅ Calendar Demo completed."
        )

    if agent == "📚 Learning & Education Agent":

        return (
            "## 📚 Learning & Education Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Learning Roadmap\n\n"
            "#### Phase 1 — Fundamentals\n"
            "- Basic concepts\n"
            "- Terminology\n"
            "- Simple exercises\n\n"
            "#### Phase 2 — Practical Learning\n"
            "- Practical exercises\n"
            "- Mini projects\n"
            "- Regular practice\n\n"
            "#### Phase 3 — Advanced Practice\n"
            "- Advanced concepts\n"
            "- Complete project\n"
            "- Testing\n\n"
            "### Workflow\n\n"
            "Objective → Roadmap → Practice → Project → Review\n\n"
            "✅ Learning Demo completed."
        )

    if agent == "📝 Productivity & Task Management Agent":

        return (
            "## 📝 Productivity & Task Management Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Priority System\n\n"
            "**High Priority**\n"
            "- Urgent work\n"
            "- Important deadlines\n\n"
            "**Medium Priority**\n"
            "- Project activities\n"
            "- Follow-up tasks\n\n"
            "**Low Priority**\n"
            "- Administrative work\n"
            "- Optional activities\n\n"
            "### Workflow\n\n"
            "Identify → Prioritize → Execute → Review\n\n"
            "✅ Productivity Demo completed."
        )

    if agent == "💰 Finance & Expense Management Agent":

        return (
            "## 💰 Finance & Expense Management Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Expense Categories\n\n"
            "| Category | Example |\n"
            "|---|---|\n"
            "| Food | Meals |\n"
            "| Transport | Fuel / Travel |\n"
            "| Education | Courses / Books |\n"
            "| Utilities | Electricity / Internet |\n"
            "| Other | Miscellaneous |\n\n"
            "### Workflow\n\n"
            "Record → Categorize → Calculate → Summarize\n\n"
            "✅ Finance Demo completed."
        )

    if agent == "🌐 Information & Communication Agent":

        return (
            "## 🌐 Information & Communication Agent\n\n"
            "**Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Communication Workflow\n\n"
            "1. Understand purpose\n"
            "2. Identify audience\n"
            "3. Structure information\n"
            "4. Generate professional content\n"
            "5. Review output\n\n"
            "### Demo Output\n\n"
            "Dear Team,\n\n"
            "This is a professional communication "
            "generated through OMNI AI Demo Mode.\n\n"
            "Regards,\n"
            "OMNI AI\n\n"
            "✅ Communication Demo completed."
        )

    if agent == "🤖 Robotics Agent":

        return (
            "## 🤖 Robotics Agent\n\n"
            "**Request:**\n\n"
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
            "### Possible Components\n\n"
            "- Raspberry Pi\n"
            "- Arduino / ESP32\n"
            "- Camera\n"
            "- Sensors\n"
            "- Motor Driver\n"
            "- DC Motors\n"
            "- Battery\n\n"
            "### Development Steps\n\n"
            "1. Define objective\n"
            "2. Select hardware\n"
            "3. Connect sensors\n"
            "4. Develop control logic\n"
            "5. Add AI capability\n"
            "6. Test system\n\n"
            "✅ Robotics Demo completed."
        )

    if agent == "🚁 Drones & Autonomous Systems Agent":

        return (
            "## 🚁 Drones & Autonomous Systems Agent\n\n"
            "**Request:**\n\n"
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
            "- Computer vision\n"
            "- Autonomous inspection\n\n"
            "### Development Workflow\n\n"
            "Mission → Sensors → Perception → AI → Navigation → Control\n\n"
            "✅ Autonomous Systems Demo completed."
        )

    return (
        "## 🧠 AI Orchestrator\n\n"
        "Request processed successfully."
    )


# ==========================================================
# GROK API RESPONSE
# ==========================================================

def grok_response(request, agent, api_key):

    url = "https://api.x.ai/v1/chat/completions"

    system_prompt = (
        "You are OMNI AI, an intelligent multi-agent "
        "automation platform.\n\n"
        "The user's request has been routed to:\n"
        + agent
        + "\n\n"
        "Act as this specialized agent.\n"
        "Provide useful, structured and practical answers.\n"
        "Use headings, lists and tables when appropriate.\n"
        "Do not claim that you performed a real-world action "
        "unless the application has the required integration."
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

    st.caption(
        "Agent Navigation"
    )

    st.divider()

    navigation = [
        "🏠 Home / Orchestrator",
        "⏰ Daily Reminder Agent",
        "❤️ Health & Wellness Agent",
        "📅 Calendar & Schedule Agent",
        "📚 Learning & Education Agent",
        "📝 Productivity & Task Management Agent",
        "💰 Finance & Expense Management Agent",
        "🌐 Information & Communication Agent",
        "🤖 Robotics Agent",
        "🚁 Drones & Autonomous Systems Agent"
    ]

    selected_navigation = st.radio(
        "Select Agent",
        navigation
    )

    st.divider()

    st.subheader("⚙️ Operating Mode")

    mode = st.radio(
        "Select Mode",
        [
            "🎮 Demo Mode",
            "🔑 Grok API Mode"
        ]
    )

    st.divider()

    st.subheader("📊 System Status")

    st.write("AI Agents: **10**")
    st.write("AI Engine: **Grok**")
    st.write("Framework: **Streamlit**")
    st.write("Database: **Not Required**")


# ==========================================================
# API KEY
# ==========================================================

api_key = ""

if mode == "🔑 Grok API Mode":

    try:

        api_key = st.secrets["XAI_API_KEY"]

    except Exception:

        api_key = ""

    if not api_key:

        api_key = os.getenv(
            "XAI_API_KEY",
            ""
        )


# ==========================================================
# HOME / ORCHESTRATOR
# ==========================================================

if selected_navigation == "🏠 Home / Orchestrator":

    st.header(
        "🧠 AI Orchestrator / Master Agent"
    )

    st.write(
        "The central intelligence layer of OMNI AI. "
        "It analyzes natural-language requests and "
        "routes them to the appropriate specialized agent."
    )

    st.divider()

    if mode == "🎮 Demo Mode":

        st.success(
            "🎮 Demo Mode Active — No API key required."
        )

    else:

        if api_key:

            st.success(
                "🔑 Grok API Mode Active — API key detected."
            )

        else:

            st.warning(
                "⚠️ Grok API Mode selected, but "
                "XAI_API_KEY was not found."
            )

    st.subheader("🔄 OMNI AI Architecture")

    st.markdown(
        """
        **User Request**

        ↓

        **Streamlit Interface**

        ↓

        **AI Orchestrator**

        ↓

        **Agent Analysis & Selection**

        ↓

        **Specialized AI Agent**

        ↓

        **Grok AI Reasoning**

        ↓

        **Intelligent Response**
        """
    )

    st.divider()

    st.subheader("🚀 Specialized AI Agents")

    col1, col2 = st.columns(2)

    agent_items = list(AGENTS.items())

    for index, item in enumerate(agent_items):

        name = item[0]
        description = item[1]

        if index % 2 == 0:

            with col1:

                st.info(
                    "**"
                    + name
                    + "**\n\n"
                    + description
                )

        else:

            with col2:

                st.info(
                    "**"
                    + name
                    + "**\n\n"
                    + description
                )


# ==========================================================
# SPECIALIZED AGENT PAGE
# ==========================================================

else:

    selected_agent = selected_navigation

    st.header(selected_agent)

    st.write(
        AGENTS[selected_agent]
    )

    st.divider()

    if mode == "🎮 Demo Mode":

        st.success(
            "🎮 Demo Mode — Agent ready for testing."
        )

    else:

        if api_key:

            st.success(
                "🔑 Grok API Mode — Agent connected."
            )

        else:

            st.warning(
                "⚠️ Add XAI_API_KEY in Streamlit "
                "Secrets to use Grok API Mode."
            )

    st.subheader("💡 Example Request")

    examples = {

        "⏰ Daily Reminder Agent":
            "Create reminders for my important activities today.",

        "❤️ Health & Wellness Agent":
            "Create a simple daily wellness routine.",

        "📅 Calendar & Schedule Agent":
            "Create a productive schedule for tomorrow.",

        "📚 Learning & Education Agent":
            "Create a 30-day Python and AI learning plan.",

        "📝 Productivity & Task Management Agent":
            "Create a priority task list for today.",

        "💰 Finance & Expense Management Agent":
            "Organize my monthly expenses into categories.",

        "🌐 Information & Communication Agent":
            "Write an announcement for an AI workshop.",

        "🤖 Robotics Agent":
            "Design a Raspberry Pi object detection robot.",

        "🚁 Drones & Autonomous Systems Agent":
            "Design an autonomous drone inspection system."
    }

    st.code(
        examples[selected_agent],
        language="text"
    )


# ==========================================================
# CHAT HISTORY
# ==========================================================

if st.session_state.messages:

    st.divider()

    st.subheader("💬 Conversation")

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


# ==========================================================
# CHAT INPUT
# ==========================================================

request = st.chat_input(
    "Ask OMNI AI anything..."
)


# ==========================================================
# PROCESS REQUEST
# ==========================================================

if request:

    with st.chat_message("user"):

        st.markdown(request)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": request
        }
    )

    detected_agent = detect_agent(
        request
    )

    st.info(
        "🧠 **AI Orchestrator selected:** "
        + detected_agent
    )

    with st.chat_message("assistant"):

        if mode == "🎮 Demo Mode":

            response = demo_response(
                request,
                detected_agent
            )

            st.markdown(response)

        else:

            if not api_key:

                response = (
                    "⚠️ **Grok API key is not configured.**\n\n"
                    "Please add this to Streamlit Secrets:\n\n"
                    "`XAI_API_KEY = \"YOUR_GROK_API_KEY\"`"
                )

                st.warning(response)

            else:

                try:

                    with st.spinner(
                        "🤖 OMNI AI is thinking..."
                    ):

                        response = grok_response(
                            request,
                            detected_agent,
                            api_key
                        )

                    st.markdown(response)

                except Exception as error:

                    response = (
                        "❌ **Grok API request failed.**\n\n"
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
    "🤖 OMNI AI | Omni-Agentic Intelligent Automation System | "
    "10 AI Agents | Demo + Grok API Mode"
)
