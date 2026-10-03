import streamlit as st
from openai import OpenAI

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
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# AGENT DEFINITIONS
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
# AGENT DETECTION
# ==========================================================

def detect_agent(request):

    text = request.lower()

    # Daily Reminder
    if any(word in text for word in [
        "reminder",
        "remind",
        "deadline",
        "routine",
        "alarm"
    ]):
        return "⏰ Daily Reminder Agent"

    # Health & Wellness
    if any(word in text for word in [
        "health",
        "fitness",
        "wellness",
        "exercise",
        "workout",
        "diet"
    ]):
        return "❤️ Health & Wellness Agent"

    # Calendar & Schedule
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

    # Learning & Education
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
        "programming"
    ]):
        return "📚 Learning & Education Agent"

    # Productivity
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

    # Finance
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

    # Communication
    if any(word in text for word in [
        "email",
        "message",
        "announcement",
        "report",
        "letter",
        "communication",
        "write an email",
        "draft"
    ]):
        return "🌐 Information & Communication Agent"

    # Robotics
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

    # Drones
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
# DEMO RESPONSE FUNCTIONS
# ==========================================================

def orchestrator_response(request):

    return (
        "## 🧠 AI Orchestrator\n\n"
        "**Your Request:**\n\n"
        + request
        + "\n\n"
        "### Agentic Analysis\n\n"
        "OMNI AI analyzed the request and could not identify "
        "a specific specialized domain.\n\n"
        "The Master Agent is handling the request.\n\n"
        "### Workflow\n\n"
        "1. User request received\n"
        "2. Request analyzed\n"
        "3. Agent selection performed\n"
        "4. Response generated\n\n"
        "✅ Orchestrator Demo completed."
    )


def reminder_response(request):

    return (
        "## ⏰ Daily Reminder Agent\n\n"
        "**Your Request:**\n\n"
        + request
        + "\n\n"
        "### Demo Reminder Plan\n\n"
        "| Time | Activity |\n"
        "|---|---|\n"
        "| 08:00 AM | Morning routine |\n"
        "| 10:00 AM | Priority task |\n"
        "| 01:00 PM | Break / lunch |\n"
        "| 04:00 PM | Review pending tasks |\n"
        "| 08:00 PM | Daily review |\n\n"
        "### Workflow\n\n"
        "1. Identify reminder\n"
        "2. Determine priority\n"
        "3. Assign time\n"
        "4. Create routine\n\n"
        "✅ Reminder Demo completed."
    )


def wellness_response(request):

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
        "> This demonstration is for organization and general "
        "wellness planning and does not replace professional "
        "medical advice."
    )


def calendar_response(request):

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
        "2. Select date/time\n"
        "3. Organize schedule\n"
        "4. Review conflicts\n\n"
        "✅ Calendar Demo completed."
    )


def learning_response(request):

    return (
        "## 📚 Learning & Education Agent\n\n"
        "**Your Request:**\n\n"
        + request
        + "\n\n"
        "### Demo Learning Roadmap\n\n"
        "**Phase 1 — Fundamentals**\n\n"
        "- Learn basic concepts\n"
        "- Understand terminology\n"
        "- Practice simple examples\n\n"
        "**Phase 2 — Practical Learning**\n\n"
        "- Build small projects\n"
        "- Practice regularly\n"
        "- Review mistakes\n\n"
        "**Phase 3 — Advanced Practice**\n\n"
        "- Build a complete project\n"
        "- Apply concepts\n"
        "- Test and improve\n\n"
        "### Workflow\n\n"
        "1. Identify learning objective\n"
        "2. Create roadmap\n"
        "3. Schedule study sessions\n"
        "4. Practice\n"
        "5. Review progress\n\n"
        "✅ Learning Demo completed."
    )


def productivity_response(request):

    return (
        "## 📝 Productivity & Task Management Agent\n\n"
        "**Your Request:**\n\n"
        + request
        + "\n\n"
        "### Demo Priority System\n\n"
        "**Priority 1 — High**\n"
        "- Urgent tasks\n"
        "- Important deadlines\n\n"
        "**Priority 2 — Medium**\n"
        "- Project activities\n"
        "- Follow-up tasks\n\n"
        "**Priority 3 — Low**\n"
        "- Administrative work\n"
        "- Optional activities\n\n"
        "### Workflow\n\n"
        "1. Identify tasks\n"
        "2. Assign priorities\n"
        "3. Complete important work\n"
        "4. Review progress\n"
        "5. Update remaining tasks\n\n"
        "✅ Productivity Demo completed."
    )


def finance_response(request):

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
        "3. Calculate total\n"
        "4. Review spending\n"
        "5. Prepare summary\n\n"
        "✅ Finance Demo completed.\n\n"
        "> This is an organizational demonstration and not "
        "regulated financial advice."
    )


def communication_response(request):

    return (
        "## 🌐 Information & Communication Agent\n\n"
        "**Your Request:**\n\n"
        + request
        + "\n\n"
        "### Demo Communication\n\n"
        "**Subject: OMNI AI Activity Update**\n\n"
        "Dear Team,\n\n"
        "This is a demonstration message generated by the "
        "OMNI AI Information & Communication Agent.\n\n"
        "The requested communication has been analyzed and "
        "structured for professional use.\n\n"
        "Regards,\n"
        "OMNI AI\n\n"
        "✅ Communication Demo completed."
    )


def robotics_response(request):

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
        "- Battery\n"
        "- AI / Computer Vision\n\n"
        "### Development Steps\n\n"
        "1. Define robot objective\n"
        "2. Select hardware\n"
        "3. Connect sensors\n"
        "4. Develop control logic\n"
        "5. Add AI capability\n"
        "6. Test the system\n\n"
        "✅ Robotics Demo completed."
    )


def drone_response(request):

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
        "### Possible Capabilities\n\n"
        "- Object detection\n"
        "- Navigation\n"
        "- Obstacle detection\n"
        "- Path planning\n"
        "- Computer vision\n"
        "- Autonomous inspection\n\n"
        "### Development Workflow\n\n"
        "1. Define mission\n"
        "2. Select sensors\n"
        "3. Design navigation system\n"
        "4. Add computer vision\n"
        "5. Implement safety logic\n"
        "6. Test in simulation\n\n"
        "✅ Autonomous Systems Demo completed."
    )


# ==========================================================
# DEMO ROUTER
# ==========================================================

def generate_demo_response(request, agent):

    if agent == "🧠 AI Orchestrator":
        return orchestrator_response(request)

    if agent == "⏰ Daily Reminder Agent":
        return reminder_response(request)

    if agent == "❤️ Health & Wellness Agent":
        return wellness_response(request)

    if agent == "📅 Calendar & Schedule Agent":
        return calendar_response(request)

    if agent == "📚 Learning & Education Agent":
        return learning_response(request)

    if agent == "📝 Productivity & Task Management Agent":
        return productivity_response(request)

    if agent == "💰 Finance & Expense Management Agent":
        return finance_response(request)

    if agent == "🌐 Information & Communication Agent":
        return communication_response(request)

    if agent == "🤖 Robotics Agent":
        return robotics_response(request)

    if agent == "🚁 Drones & Autonomous Systems Agent":
        return drone_response(request)

    return orchestrator_response(request)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🤖 OMNI AI")

    st.subheader("Operating Mode")

    mode = st.radio(
        "Select Mode",
        [
            "🎮 Demo Mode",
            "🔑 Grok API Mode"
        ]
    )

    st.divider()

    st.subheader("10 AI Agents")

    for agent_name in AGENTS:
        st.write(agent_name)

    st.divider()

    st.caption(
        "Omni-Agentic Intelligent Automation System"
    )


# ==========================================================
# MAIN INTERFACE
# ==========================================================

st.title("🤖 OMNI AI")

st.subheader(
    "Omni-Agentic Intelligent Automation System"
)

st.write(
    "Centralized multi-agent AI assistant powered by "
    "Python, Streamlit and Grok AI."
)


# ==========================================================
# MODE STATUS
# ==========================================================

if mode == "🎮 Demo Mode":

    st.success(
        "🎮 Demo Mode Active — All 10 agents are working."
    )

else:

    st.info(
        "🔑 Grok API Mode selected."
    )


# ==========================================================
# AGENT DASHBOARD
# ==========================================================

st.divider()

st.subheader("🚀 Available AI Agents")

col1, col2 = st.columns(2)

agent_items = list(AGENTS.items())

for index, item in enumerate(agent_items):

    agent_name = item[0]
    description = item[1]

    with col1 if index % 2 == 0 else col2:

        st.info(
            "**"
            + agent_name
            + "**\n\n"
            + description
        )


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================================
# USER CHAT
# ==========================================================

request = st.chat_input(
    "Ask OMNI AI anything..."
)


if request:

    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": request
        }
    )

    # Display user message

    with st.chat_message("user"):

        st.markdown(request)

    # ======================================================
    # ORCHESTRATOR
    # ======================================================

    selected_agent = detect_agent(request)

    st.success(
        "🧠 AI Orchestrator selected: "
        + selected_agent
    )

    # ======================================================
    # RESPONSE
    # ======================================================

    with st.chat_message("assistant"):

        if mode == "🎮 Demo Mode":

            response = generate_demo_response(
                request,
                selected_agent
            )

            st.markdown(response)

        else:

            st.warning(
                "🔑 Grok API integration will be activated "
                "in the next step."
            )

            response = (
                "Grok API Mode is selected, but the API "
                "connection has not been activated yet."
            )

    # Save assistant response

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