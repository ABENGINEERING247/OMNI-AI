import os
import requests
import streamlit as st


# ==========================================================
# OMNI AI
# Omni-Agentic Intelligent Automation System
# ==========================================================

st.set_page_config(
    page_title="OMNI AI - Omni-Agentic Intelligent Automation System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# PROFESSIONAL HEADER
# ==========================================================

st.markdown(
    """
    <div style="
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.35);
        background: linear-gradient(
            135deg,
            rgba(30,30,40,0.95),
            rgba(45,45,65,0.95)
        );
    ">

        <h1 style="
            font-size: 46px;
            margin-bottom: 5px;
        ">
            🤖 OMNI AI
        </h1>

        <h2 style="
            font-size: 25px;
            margin-top: 0;
        ">
            Omni-Agentic Intelligent Automation System
        </h2>

        <p style="
            font-size: 18px;
            margin-top: 15px;
        ">
            Grok-Powered Multi-Agent AI Solution
        </p>

        <p style="
            font-size: 15px;
            margin-top: 12px;
        ">
            10 Specialized AI Agents
            &nbsp; • &nbsp;
            Demo Mode
            &nbsp; • &nbsp;
            Grok API Mode
            &nbsp; • &nbsp;
            Streamlit
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


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
        "artificial intelligence"
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
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Agentic Analysis\n\n"
            "OMNI AI analyzed your request and selected "
            "the appropriate processing route.\n\n"
            "### Workflow\n\n"
            "1. User request received\n"
            "2. Request analyzed\n"
            "3. Specialized agent identified\n"
            "4. Response generated\n\n"
            "✅ Orchestrator Demo completed."
        )

    if agent == "⏰ Daily Reminder Agent":

        return (
            "## ⏰ Daily Reminder Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Reminder Plan\n\n"
            "- Morning routine\n"
            "- Priority task reminder\n"
            "- Important deadline\n"
            "- Afternoon review\n"
            "- Evening daily review\n\n"
            "### Workflow\n\n"
            "1. Identify reminder\n"
            "2. Determine priority\n"
            "3. Organize time\n"
            "4. Prepare reminder\n\n"
            "✅ Reminder Demo completed."
        )

    if agent == "❤️ Health & Wellness Agent":

        return (
            "## ❤️ Health & Wellness Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Wellness Plan\n\n"
            "- Morning activity\n"
            "- Hydration reminder\n"
            "- Fitness session\n"
            "- Rest period\n"
            "- Evening wellness review\n\n"
            "### Workflow\n\n"
            "1. Identify wellness activity\n"
            "2. Organize routine\n"
            "3. Schedule activity\n"
            "4. Review progress\n\n"
            "✅ Wellness Demo completed.\n\n"
            "> This is a general wellness organization "
            "demonstration and does not replace professional "
            "medical advice."
        )

    if agent == "📅 Calendar & Schedule Agent":

        return (
            "## 📅 Calendar & Schedule Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Schedule\n\n"
            "| Time | Activity |\n"
            "|---|---|\n"
            "| 09:00 AM | Meeting / Class |\n"
            "| 11:00 AM | Project Work |\n"
            "| 01:00 PM | Lunch |\n"
            "| 03:00 PM | Review |\n"
            "| 05:00 PM | Follow-up |\n\n"
            "### Workflow\n\n"
            "1. Identify event\n"
            "2. Select time\n"
            "3. Organize schedule\n"
            "4. Review conflicts\n\n"
            "✅ Calendar Demo completed."
        )

    if agent == "📚 Learning & Education Agent":

        return (
            "## 📚 Learning & Education Agent\n\n"
            "**Your Request:**\n\n"
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
            "- Testing and improvement\n\n"
            "### Workflow\n\n"
            "1. Identify learning objective\n"
            "2. Create roadmap\n"
            "3. Schedule learning\n"
            "4. Practice\n"
            "5. Review progress\n\n"
            "✅ Learning Demo completed."
        )

    if agent == "📝 Productivity & Task Management Agent":

        return (
            "## 📝 Productivity & Task Management Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Priority System\n\n"
            "**High Priority**\n"
            "- Urgent tasks\n"
            "- Important deadlines\n\n"
            "**Medium Priority**\n"
            "- Project activities\n"
            "- Follow-up work\n\n"
            "**Low Priority**\n"
            "- Administrative tasks\n"
            "- Optional activities\n\n"
            "### Workflow\n\n"
            "1. Identify tasks\n"
            "2. Assign priorities\n"
            "3. Complete important work\n"
            "4. Review progress\n\n"
            "✅ Productivity Demo completed."
        )

    if agent == "💰 Finance & Expense Management Agent":

        return (
            "## 💰 Finance & Expense Management Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Expense Categories\n\n"
            "| Category | Example |\n"
            "|---|---|\n"
            "| Food | Daily meals |\n"
            "| Transport | Fuel / travel |\n"
            "| Education | Courses / books |\n"
            "| Utilities | Electricity / Internet |\n"
            "| Other | Miscellaneous |\n\n"
            "### Workflow\n\n"
            "1. Record expense\n"
            "2. Categorize expense\n"
            "3. Calculate totals\n"
            "4. Review spending\n"
            "5. Prepare summary\n\n"
            "✅ Finance Demo completed."
        )

    if agent == "🌐 Information & Communication Agent":

        return (
            "## 🌐 Information & Communication Agent\n\n"
            "**Your Request:**\n\n"
            + request
            + "\n\n"
            "### Demo Communication\n\n"
            "**AI Workshop Announcement**\n\n"
            "Dear Team,\n\n"
            "This is a demonstration communication "
            "generated by OMNI AI.\n\n"
            "The requested information has been "
            "structured for professional communication.\n\n"
            "Regards,\n"
            "OMNI AI\n\n"
            "✅ Communication Demo completed."
        )

    if agent == "🤖 Robotics Agent":

        return (
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
            "### Possible Components\n\n"
            "- Raspberry Pi\n"
            "- Arduino / ESP32\n"
            "- Camera\n"
            "- Ultrasonic sensors\n"
            "- Motor driver\n"
            "- DC motors\n"
            "- Battery\n\n"
            "### Development Steps\n\n"
            "1. Define robot objective\n"
            "2. Select hardware\n"
            "3. Connect sensors\n"
            "4. Develop control logic\n"
            "5. Add AI capability\n"
            "6. Test the system\n\n"
            "✅ Robotics Demo completed."
        )

    if agent == "🚁 Drones & Autonomous Systems Agent":

        return (
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
            "- Computer vision\n"
            "- Autonomous inspection\n\n"
            "### Development Workflow\n\n"
            "1. Define mission\n"
            "2. Select sensors\n"
            "3. Design navigation\n"
            "4. Add computer vision\n"
            "5. Implement safety logic\n"
            "6. Test in simulation\n\n"
            "✅ Autonomous Systems Demo completed."
        )

    return (
        "## 🧠 AI Orchestrator\n\n"
        "Request processed successfully."
    )


# ==========================================================
# GROK API
# ==========================================================

def grok_response(request, agent, api_key):

    url = "https://api.x.ai/v1/chat/completions"

    system_prompt = (
        "You are OMNI AI, an intelligent multi-agent "
        "automation platform.\n\n"
        "The user request has been routed to this agent:\n"
        + agent
        + "\n\n"
        "Act as this specialized agent.\n"
        "Provide practical, structured and useful answers.\n"
        "Use headings, lists and tables where appropriate.\n"
        "Do not claim that a real-world action was completed "
        "unless the application actually has the required "
        "integration or tool."
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
# SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:

    st.title("🤖 OMNI AI")

    st.caption(
        "Omni-Agentic Intelligent Automation System"
    )

    st.divider()

    st.subheader("🧭 Agent Navigation")

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

    st.subheader("📊 System")

    st.write("Agents: **10**")
    st.write("AI Engine: **Grok**")
    st.write("Interface: **Streamlit**")
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
# HOME PAGE
# ==========================================================

if selected_navigation == "🏠 Home / Orchestrator":

    st.title("🧠 AI Orchestrator")

    st.subheader(
        "Central Intelligence & Agent Coordination"
    )

    st.write(
        "The AI Orchestrator analyzes user requests "
        "and routes them to the appropriate specialized "
        "AI agent."
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

        **AI Orchestrator / Master Agent**

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

        with col1 if index % 2 == 0 else col2:

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

    st.title(selected_agent)

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
                "🔑 Grok API Mode — Agent connected "
                "to the Grok reasoning engine."
            )

        else:

            st.warning(
                "⚠️ Add XAI_API_KEY in Streamlit Secrets "
                "to use Grok API Mode."
            )

    st.divider()

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
                    "Add the following to Streamlit Secrets:\n\n"
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

st.markdown(
    """
    <div style="text-align:center; padding:15px;">

    <strong>🤖 OMNI AI</strong><br>

    Omni-Agentic Intelligent Automation System<br>

    <small>
    Grok-Powered Multi-Agent AI Solution
    • 10 Specialized Agents
    • Demo + API Mode
    • Streamlit
    </small>

    </div>
    """,
    unsafe_allow_html=True
)
