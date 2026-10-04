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
        "workflow_running": False,
        "workflow_messages": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# ============================================================
# SAFE HELPERS
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


def delete_item(collection_name, index):
    items = st.session_state.get(collection_name, [])

    if 0 <= index < len(items):
        items.pop(index)
        st.session_state[collection_name] = items

    st.rerun()


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [3, 1],
    vertical_alignment="center"
)

with header_col1:
    st.title("🤖 OMNI AI")
    st.subheader("Omni-Agentic Intelligent Automation System")
    st.caption(
        "Multi-Agent AI • Daily Automation • Productivity • "
        "Robotics • Autonomous Systems"
    )

with header_col2:
    st.metric("AI Agents", "10")

st.divider()


# ============================================================
# AGENTS
# ============================================================

AGENTS = {
    "🧠 AI Orchestrator":
        "Master agent that analyzes requests and communicates with specialist agents.",

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
# AGENT KEYWORDS
# ============================================================

def detect_agent(request):
    text = request.lower()

    rules = [
        (
            ["reminder", "alarm", "remind", "deadline"],
            "⏰ Daily Reminder Agent",
        ),
        (
            ["health", "wellness", "fitness", "exercise", "workout"],
            "❤️ Health & Wellness Agent",
        ),
        (
            [
                "calendar",
                "meeting",
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
                "communication",
            ],
            "🌐 Information & Communication Agent",
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
                "embedded",
                "plc",
            ],
            "🤖 Robotics Agent",
        ),
        (
            [
                "drone",
                "uav",
                "autonomous",
                "navigation",
                "quadcopter",
                "flight",
            ],
            "🚁 Drones & Autonomous Systems Agent",
        ),
    ]

    for keywords, agent in rules:
        if any(word in text for word in keywords):
            return agent

    return "🧠 AI Orchestrator"


# ============================================================
# AI PROVIDERS / API KEYS
# ============================================================

def get_secret(name):
    """Read a Streamlit Secret first, then fall back to environment variables."""
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value).strip()
    except Exception:
        pass

    return os.getenv(name, "").strip()


def get_grok_api_key():
    return get_secret("XAI_API_KEY")


def get_openai_api_key():
    return get_secret("OPENAI_API_KEY")


def get_provider_api_key(provider):
    if provider == "Grok":
        return get_grok_api_key()
    if provider == "OpenAI":
        return get_openai_api_key()
    return ""


# ============================================================
# GROK API
# ============================================================

def call_grok(request, agent, api_key):
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-3-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are OMNI AI, a multi-agent intelligent assistant. "
                    "The selected specialist agent is "
                    f"{agent}. "
                    "Respond as part of a multi-agent system. "
                    "Explain which agent should handle the request "
                    "and provide a practical structured response."
                ),
            },
            {
                "role": "user",
                "content": request,
            },
        ],
        "temperature": 1,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Grok API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response received from Grok API.")


# ============================================================
# OPENAI API
# ============================================================

def call_openai(request, agent, api_key):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-6-luna",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are OMNI AI, a multi-agent intelligent assistant. "
                    "The selected specialist agent is "
                    f"{agent}. "
                    "Respond as part of a multi-agent system. "
                    "Explain which agent should handle the request "
                    "and provide a practical structured response."
                ),
            },
            {
                "role": "user",
                "content": request,
            },
        ],
        "temperature": 1,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenAI API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response received from OpenAI API.")


# ============================================================
# UNIFIED AI CALL
# ============================================================

def call_ai_provider(request, agent, provider, api_key):
    if provider == "Grok":
        return call_grok(request, agent, api_key)

    if provider == "OpenAI":
        return call_openai(request, agent, api_key)

    raise RuntimeError(f"Unsupported AI provider: {provider}")


# ============================================================
# AUTOMATIC API / DEMO FALLBACK
# ============================================================

def process_with_ai(request, agent, provider, allow_fallback=True):
    """
    Use the selected API provider.

    If the key is missing or the API fails and allow_fallback=True,
    automatically switch to Demo Mode instead of crashing the app.
    """
    api_key = get_provider_api_key(provider)

    if not api_key:
        if allow_fallback:
            return (
                demo_response(request, agent),
                "Demo Mode",
                f"{provider} API key not configured. Automatically switched to Demo Mode."
            )

        raise RuntimeError(
            f"{provider} API key is not configured in Streamlit Secrets."
        )

    try:
        result = call_ai_provider(
            request,
            agent,
            provider,
            api_key,
        )

        return result, provider, None

    except Exception as exc:
        if allow_fallback:
            return (
                demo_response(request, agent),
                "Demo Mode",
                f"{provider} API failed. Automatically switched to Demo Mode. Error: {exc}"
            )

        raise


# ============================================================
# DEMO RESPONSE
# ============================================================

def demo_response(request, agent):
    description = AGENTS.get(
        agent,
        "Specialist agent selected."
    )

    return (
        f"## {agent}\n\n"
        f"**Request:** {request}\n\n"
        "### Demo Processing\n\n"
        "1. Request received\n"
        "2. Intent analyzed\n"
        f"3. **{agent}** selected\n"
        "4. Specialist workflow executed\n"
        "5. Structured response generated\n\n"
        "### Agent Role\n\n"
        f"{description}\n\n"
        "🟢 **Agent Status: Active**"
    )


# ============================================================
# NOTIFICATIONS
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
                    new Notification("OMNI AI Reminder", {{
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
                category,
            )
        )

        if item_date is None or item_time is None:
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
                    not in st.session_state.fired_notifications
                ):
                    st.session_state.fired_notifications.add(
                        nid
                    )

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
            icon="🔔"
        )

        browser_notification(message)

    if notifications:
        st.warning(
            "🔔 **OMNI AI NOTIFICATION**\n\n"
            + "\n\n".join(
                f"- {message}"
                for message in notifications
            )
        )


if AUTO_REFRESH_AVAILABLE:
    st_autorefresh(
        interval=15000,
        key="omni_refresh",
    )

run_notification_engine()


# ============================================================
# DEMO AGENT WORKFLOW
# ============================================================

def create_demo_workflow(request):
    primary_agent = detect_agent(request)

    workflow = [
        {
            "from": "👤 User",
            "to": "🧠 AI Orchestrator",
            "message": (
                f"Request received: {request}"
            ),
        },
        {
            "from": "🧠 AI Orchestrator",
            "to": primary_agent,
            "message": (
                f"Orchestrator routes the request "
                f"to {primary_agent}."
            ),
        },
    ]

    if primary_agent != "⏰ Daily Reminder Agent":
        workflow.append(
            {
                "from": primary_agent,
                "to": "⏰ Daily Reminder Agent",
                "message": (
                    "Please create a reminder/notification "
                    "if the request contains a deadline."
                ),
            }
        )

    if primary_agent != "📅 Calendar & Schedule Agent":
        workflow.append(
            {
                "from": primary_agent,
                "to": "📅 Calendar & Schedule Agent",
                "message": (
                    "Please coordinate schedule information "
                    "when dates or meetings are involved."
                ),
            }
        )

    workflow.append(
        {
            "from": "🧠 AI Orchestrator",
            "to": "👤 User",
            "message": (
                "All required agents have communicated. "
                "Final response is ready."
            ),
        }
    )

    return workflow


def run_demo_workflow(request):
    if not request.strip():
        st.warning(
            "Please enter a workflow request."
        )
        return

    workflow = create_demo_workflow(request)

    st.subheader(
        "🔄 Live Multi-Agent Communication"
    )

    progress = st.progress(0)

    for index, step in enumerate(workflow):
        with st.container(border=True):
            st.markdown(
                f"### {step['from']} → {step['to']}"
            )

            st.write(
                step["message"]
            )

        progress.progress(
            int(
                ((index + 1) / len(workflow))
                * 100
            )
        )

    st.success(
        "✅ Demo workflow completed successfully."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("🤖 OMNI AI")
    st.caption("Agent Navigation")

    page = st.radio(
        "Select Module",
        [
            "🏠 Dashboard",
            "🧠 AI Orchestrator",
            "🔄 Agent Workflow Demo",
            "💬 OMNI AI Chatbot",
            "⏰ Reminders & Alarms",
            "📅 Calendar & Meetings",
            "📚 Learning",
            "📝 Tasks & Productivity",
            "❤️ Wellness",
            "💰 Finance",
            "🌐 Communication",
            "🤖 Robotics",
            "🚁 Drones & Autonomous",
        ],
    )

    st.divider()

    mode = st.radio(
        "Operating Mode",
        [
            "🎮 Demo Mode",
            "🔑 API Mode",
        ],
    )

    if mode == "🔑 API Mode":
        provider = st.selectbox(
            "AI Provider",
            [
                "Grok",
                "OpenAI",
            ],
            index=0,
        )

        selected_api_key = get_provider_api_key(provider)

        if selected_api_key:
            st.success(
                f"🔑 {provider} API key detected."
            )
        else:
            st.warning(
                f"{provider} API key not configured. "
                "Automatic Demo fallback is enabled."
            )

        st.caption(
            "Secrets: XAI_API_KEY for Grok • "
            "OPENAI_API_KEY for OpenAI"
        )
    else:
        provider = "Demo"

    # Compatibility variables used by the rest of the application.
    api_key = get_provider_api_key(provider) if provider != "Demo" else ""

    st.divider()

    st.subheader("📊 Data")

    counts = [
        ("Meetings", "meetings"),
        ("Reminders", "reminders"),
        ("Tasks", "tasks"),
        ("Learning", "learning"),
        ("Wellness", "wellness"),
        ("Expenses", "expenses"),
        ("Communications", "communications"),
        ("Robotics", "robotics"),
        ("Drones", "drones"),
    ]

    for label, key in counts:
        st.write(
            f"{label}: "
            f"**{len(st.session_state[key])}**"
        )

    st.divider()

    if st.button(
        "🗑️ Clear All Demo Data",
        use_container_width=True,
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

    st.header("📊 OMNI AI Dashboard")

    st.write(
        "Centralized multi-agent AI assistant with "
        "Demo Mode, Grok API Mode and OpenAI API Mode."
    )

    cols = st.columns(5)

    cols[0].metric(
        "📅 Meetings",
        len(st.session_state.meetings),
    )

    cols[1].metric(
        "⏰ Reminders",
        len(st.session_state.reminders),
    )

    cols[2].metric(
        "📝 Tasks",
        len(st.session_state.tasks),
    )

    cols[3].metric(
        "❤️ Wellness",
        len(st.session_state.wellness),
    )

    cols[4].metric(
        "🤖 Robotics",
        len(st.session_state.robotics),
    )

    st.divider()

    st.subheader("🔄 Architecture")

    st.code(
        """User Request
      ↓
Streamlit UI
      ↓
AI Orchestrator
      ↓
Specialized Agent
      ↓
Other Required Agents
      ↓
Demo Engine / Grok API
      ↓
Task / Schedule Data
      ↓
Notification
      ↓
User""",
        language="text",
    )

    st.subheader("🤖 AI Agents")

    for name, description in AGENTS.items():
        st.info(
            f"**{name}** — {description}"
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
            "Example: Create a meeting tomorrow at "
            "10 AM and remind me."
        ),
        height=150,
    )

    c1, c2 = st.columns(2)

    with c1:
        process_button = st.button(
            "🚀 Process Request",
            use_container_width=True,
        )

    with c2:
        workflow_button = st.button(
            "🔄 Play Agent Workflow",
            use_container_width=True,
        )

    if process_button:

        if not request.strip():

            st.warning(
                "Please enter a request."
            )

        else:

            agent = detect_agent(request)

            st.success(
                f"Selected Agent: {agent}"
            )

            if mode == "🎮 Demo Mode":

                st.markdown(
                    demo_response(
                        request,
                        agent,
                    )
                )

            else:

                with st.spinner(
                    f"🤖 {provider} is processing..."
                ):
                    result, actual_mode, fallback_message = process_with_ai(
                        request,
                        agent,
                        provider,
                        allow_fallback=True,
                    )

                if fallback_message:
                    st.warning(f"⚠️ {fallback_message}")

                if actual_mode == "Demo Mode":
                    st.info("🎮 Response generated in Demo Mode.")
                else:
                    st.success(f"🔑 Response generated using {actual_mode} API.")

                st.markdown(result)

    if workflow_button:

        run_demo_workflow(
            request
        )


# ============================================================
# AGENT WORKFLOW DEMO
# ============================================================

elif page == "🔄 Agent Workflow Demo":

    st.header(
        "🔄 OMNI AI Multi-Agent Workflow Demo"
    )

    st.write(
        "This demonstration shows how the "
        "AI Orchestrator communicates with "
        "specialist agents."
    )

    request = st.text_area(
        "Enter Demo Request",
        value=(
            "Create a robotics project meeting "
            "tomorrow at 10 AM and remind me."
        ),
        height=120,
    )

    if st.button(
        "▶️ PLAY DEMO WORKFLOW",
        use_container_width=True,
    ):

        run_demo_workflow(
            request
        )


# ============================================================
# OMNI AI CHATBOT
# ============================================================

elif page == "💬 OMNI AI Chatbot":

    st.header(
        "💬 OMNI AI Multi-Agent Chatbot"
    )

    st.caption(
        "Chat with the OMNI AI Orchestrator "
        "and route requests to specialist agents."
    )

    if st.session_state.chat_history:

        for message in st.session_state.chat_history:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

    user_prompt = st.chat_input(
        "Ask OMNI AI anything..."
    )

    if user_prompt:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        agent = detect_agent(
            user_prompt
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):

            st.info(
                f"🤖 Routed to: **{agent}**"
            )

            if mode == "🎮 Demo Mode":

                answer = demo_response(
                    user_prompt,
                    agent,
                )

            else:

                with st.spinner(
                    f"🤖 OMNI AI is thinking with {provider}..."
                ):
                    answer, actual_mode, fallback_message = process_with_ai(
                        user_prompt,
                        agent,
                        provider,
                        allow_fallback=True,
                    )

                if fallback_message:
                    st.warning(f"⚠️ {fallback_message}")

                if actual_mode == "Demo Mode":
                    st.info("🎮 Response generated in Demo Mode.")
                else:
                    st.success(f"🔑 Response generated using {actual_mode} API.")

            st.markdown(answer)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# REMINDERS
# ============================================================

elif page == "⏰ Reminders & Alarms":

    st.header(
        "⏰ Daily Reminder Agent"
    )

    with st.form("reminder_form"):

        title = st.text_input(
            "Reminder / Alarm Title"
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Due Date",
            value=date.today(),
        )

        due_time = c2.time_input(
            "⏰ Alarm Time",
            value=time(9, 0),
        )

        notification = st.checkbox(
            "🔔 Enable Alarm / Notification",
            value=True,
        )

        repeat = st.selectbox(
            "🔁 Repeat",
            [
                "Once",
                "Daily",
                "Weekly",
                "Weekdays",
                "Monthly",
            ],
        )

        priority = st.selectbox(
            "⚡ Priority",
            [
                "High",
                "Medium",
                "Low",
            ],
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
                        "title": title.strip(),
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
                        "repeat": repeat,
                        "priority": priority,
                        "notes": notes,
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
            f"📅 {safe_date(item)} | "
            f"🕐 {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}\n\n"
            f"🔁 {safe_value(item, 'repeat')} | "
            f"⚡ {safe_value(item, 'priority')}\n\n"
            f"📝 {safe_value(item, 'notes', '')}"
        )

        if st.button(
            "🗑️ Delete Reminder",
            key=f"rem_delete_{i}",
        ):

            delete_item(
                "reminders",
                i,
            )


# ============================================================
# CALENDAR
# ============================================================

elif page == "📅 Calendar & Meetings":

    st.header(
        "📅 Calendar & Schedule Agent"
    )

    with st.form("meeting_form"):

        title = st.text_input(
            "Meeting / Event Title"
        )

        c1, c2 = st.columns(2)

        meeting_date = c1.date_input(
            "📅 Date",
            value=date.today(),
        )

        meeting_time = c2.time_input(
            "⏰ Time",
            value=time(10, 0),
        )

        duration = st.number_input(
            "Duration (minutes)",
            min_value=15,
            max_value=480,
            value=60,
            step=15,
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
                "Project Review",
            ],
        )

        notification = st.checkbox(
            "🔔 Meeting Notification",
            value=True,
        )

        submit = st.form_submit_button(
            "➕ Add to Calendar"
        )

        if submit:

            if title.strip():

                st.session_state.meetings.append(
                    {
                        "title": title.strip(),
                        "date": meeting_date,
                        "time": meeting_time,
                        "duration": duration,
                        "location": location,
                        "participants": participants,
                        "type": event_type,
                        "notification": notification,
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
            f"📅 {safe_value(item, 'date')} | "
            f"⏰ {safe_value(item, 'time')}\n\n"
            f"⏱️ {safe_value(item, 'duration')} minutes | "
            f"📍 {safe_value(item, 'location', '')}\n\n"
            f"👥 {safe_value(item, 'participants', '')} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Meeting",
            key=f"meeting_delete_{i}",
        ):

            delete_item(
                "meetings",
                i,
            )


# ============================================================
# LEARNING
# ============================================================

elif page == "📚 Learning":

    st.header(
        "📚 Learning & Education Agent"
    )

    with st.form("learning_form"):

        subject = st.text_input(
            "📚 Subject / Course"
        )

        goal = st.text_area(
            "🎯 Learning Goal"
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Study Date",
            value=date.today(),
        )

        due_time = c2.time_input(
            "⏰ Study Time",
            value=time(18, 0),
        )

        notification = st.checkbox(
            "🔔 Study Notification",
            value=True,
        )

        submit = st.form_submit_button(
            "➕ Add Learning Activity"
        )

        if submit:

            if subject.strip():

                st.session_state.learning.append(
                    {
                        "subject": subject.strip(),
                        "goal": goal,
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
                    }
                )

                st.success(
                    "✅ Learning activity added."
                )

            else:

                st.warning(
                    "Enter a subject."
                )

    st.divider()

    if not st.session_state.learning:

        st.info(
            "No learning activities added."
        )

    for i, item in enumerate(
        st.session_state.learning
    ):

        st.info(
            f"📚 **{safe_value(item, 'subject')}**\n\n"
            f"🎯 {safe_value(item, 'goal', '')}\n\n"
            f"📅 {safe_date(item)} | "
            f"⏰ {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Learning Activity",
            key=f"learning_delete_{i}",
        ):

            delete_item(
                "learning",
                i,
            )


# ============================================================
# TASKS
# ============================================================

elif page == "📝 Tasks & Productivity":

    st.header(
        "📝 Productivity & Task Management Agent"
    )

    with st.form("task_form"):

        task = st.text_input(
            "📝 Task"
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Due Date",
            value=date.today(),
        )

        due_time = c2.time_input(
            "⏰ Due Time",
            value=time(17, 0),
        )

        priority = st.selectbox(
            "⚡ Priority",
            [
                "High",
                "Medium",
                "Low",
            ],
        )

        notification = st.checkbox(
            "🔔 Enable Task Notification",
            value=True,
        )

        submit = st.form_submit_button(
            "➕ Add Task"
        )

        if submit:

            if task.strip():

                st.session_state.tasks.append(
                    {
                        "task": task.strip(),
                        "due_date": due_date,
                        "due_time": due_time,
                        "priority": priority,
                        "notification": notification,
                        "completed": False,
                    }
                )

                st.success(
                    "✅ Task added."
                )

            else:

                st.warning(
                    "Enter a task."
                )

    st.divider()

    if not st.session_state.tasks:

        st.info(
            "No tasks added."
        )

    for i, item in enumerate(
        st.session_state.tasks
    ):

        completed = st.checkbox(
            f"✅ {safe_value(item, 'task')}",
            value=bool(
                item.get(
                    "completed",
                    False
                )
            ),
            key=f"task_{i}",
        )

        item["completed"] = completed

        st.caption(
            f"📅 {safe_date(item)} | "
            f"⏰ {safe_time(item)} | "
            f"⚡ {safe_value(item, 'priority')} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Task",
            key=f"task_delete_{i}",
        ):

            delete_item(
                "tasks",
                i,
            )


# ============================================================
# WELLNESS
# ============================================================

elif page == "❤️ Wellness":

    st.header(
        "❤️ Health & Wellness Agent"
    )

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
                "Other",
            ],
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Date",
            value=date.today(),
        )

        due_time = c2.time_input(
            "⏰ Time",
            value=time(7, 0),
        )

        notification = st.checkbox(
            "🔔 Wellness Notification",
            value=True,
        )

        submit = st.form_submit_button(
            "➕ Schedule Wellness Activity"
        )

        if submit:

            if activity.strip():

                st.session_state.wellness.append(
                    {
                        "activity": activity.strip(),
                        "type": activity_type,
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
                    }
                )

                st.success(
                    "✅ Wellness activity scheduled."
                )

            else:

                st.warning(
                    "Enter an activity."
                )

    st.divider()

    if not st.session_state.wellness:

        st.info(
            "No wellness activities added."
        )

    for i, item in enumerate(
        st.session_state.wellness
    ):

        st.info(
            f"❤️ **{safe_value(item, 'activity')}**\n\n"
            f"Type: {safe_value(item, 'type')}\n\n"
            f"📅 {safe_date(item)} | "
            f"⏰ {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Wellness Activity",
            key=f"wellness_delete_{i}",
        ):

            delete_item(
                "wellness",
                i,
            )


# ============================================================
# FINANCE
# ============================================================

elif page == "💰 Finance":

    st.header(
        "💰 Finance & Expense Management Agent"
    )

    with st.form("finance_form"):

        description = st.text_input(
            "Expense / Payment"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0,
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
                "Other",
            ],
        )

        c1, c2 = st.columns(2)

        due_date = c1.date_input(
            "📅 Payment Date",
            value=date.today(),
        )

        due_time = c2.time_input(
            "⏰ Payment Time",
            value=time(12, 0),
        )

        notification = st.checkbox(
            "🔔 Payment Notification",
            value=False,
        )

        submit = st.form_submit_button(
            "➕ Add Expense"
        )

        if submit:

            if description.strip():

                st.session_state.expenses.append(
                    {
                        "description": description.strip(),
                        "amount": amount,
                        "category": category,
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
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
        for item in st.session_state.expenses
        if isinstance(item, dict)
    )

    st.metric(
        "💰 Total Expenses",
        f"{total:,.2f}",
    )

    st.divider()

    if not st.session_state.expenses:

        st.info(
            "No expenses added."
        )

    for i, item in enumerate(
        st.session_state.expenses
    ):

        amount_value = float(
            item.get(
                "amount",
                0
            ) or 0
        )

        st.info(
            f"💰 **{safe_value(item, 'description')}**\n\n"
            f"Amount: {amount_value:,.2f}\n\n"
            f"Category: {safe_value(item, 'category')}\n\n"
            f"📅 {safe_date(item)} | "
            f"⏰ {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Expense",
            key=f"expense_delete_{i}",
        ):

            delete_item(
                "expenses",
                i,
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
            "Notice",
        ],
    )

    recipient = st.text_input(
        "Recipient / Audience"
    )

    subject = st.text_input(
        "Subject"
    )

    content = st.text_area(
        "Message Content",
        height=150,
    )

    c1, c2 = st.columns(2)

    due_date = c1.date_input(
        "📅 Schedule Date",
        value=date.today(),
    )

    due_time = c2.time_input(
        "⏰ Schedule Time",
        value=time(10, 0),
    )

    notification = st.checkbox(
        "🔔 Communication Notification",
        value=False,
    )

    if st.button(
        "✍️ Generate & Save",
        use_container_width=True,
    ):

        if not content.strip():

            st.warning(
                "Please enter message content."
            )

        else:

            generated = (
                f"Dear Team,\n\n"
                f"{content}\n\n"
                f"Regards,\n"
                f"OMNI AI"
            )

            st.session_state.communications.append(
                {
                    "type": content_type,
                    "recipient": recipient,
                    "subject": (
                        subject
                        or content_type
                    ),
                    "content": generated,
                    "due_date": due_date,
                    "due_time": due_time,
                    "notification": notification,
                }
            )

            st.success(
                "✅ Communication saved."
            )

            st.text_area(
                "Generated Content",
                generated,
                height=180,
            )

    st.divider()

    if not st.session_state.communications:

        st.info(
            "No communications saved."
        )

    for i, item in enumerate(
        st.session_state.communications
    ):

        st.info(
            f"🌐 **{safe_value(item, 'subject')}**\n\n"
            f"Type: {safe_value(item, 'type')}\n\n"
            f"Recipient: "
            f"{safe_value(item, 'recipient', '')}\n\n"
            f"📅 {safe_date(item)} | "
            f"⏰ {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        with st.expander(
            "View Content"
        ):

            st.write(
                safe_value(
                    item,
                    "content",
                    ""
                )
            )

        if st.button(
            "🗑️ Delete Communication",
            key=f"communication_delete_{i}",
        ):

            delete_item(
                "communications",
                i,
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

    with st.form("robotics_form"):

        project = st.text_input(
            "🤖 Project Name"
        )

        c1, c2 = st.columns(2)

        controller = c1.selectbox(
            "🎛️ Controller",
            controllers,
        )

        component = c2.selectbox(
            "🧩 Main Component",
            components,
        )

        c3, c4 = st.columns(2)

        sensor = c3.selectbox(
            "📡 Sensor",
            sensors,
        )

        actuator = c4.selectbox(
            "⚙️ Actuator",
            actuators,
        )

        c5, c6 = st.columns(2)

        communication_type = c5.selectbox(
            "📶 Communication",
            communication,
        )

        application = c6.selectbox(
            "🎯 Application",
            applications,
        )

        objective = st.text_area(
            "🎯 Project Objective"
        )

        c7, c8 = st.columns(2)

        due_date = c7.date_input(
            "📅 Project / Review Date",
            value=date.today(),
        )

        due_time = c8.time_input(
            "⏰ Project / Review Time",
            value=time(15, 0),
        )

        notification = st.checkbox(
            "🔔 Enable Robotics Notification",
            value=True,
        )

        submit = st.form_submit_button(
            "➕ Add Robotics Project"
        )

        if submit:

            if project.strip():

                st.session_state.robotics.append(
                    {
                        "project": project.strip(),
                        "controller": controller,
                        "component": component,
                        "sensor": sensor,
                        "actuator": actuator,
                        "communication": communication_type,
                        "application": application,
                        "objective": objective,
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
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
            f"🤖 **{safe_value(item, 'project')}**\n\n"
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
            f"📅 Date: {safe_date(item)} | "
            f"⏰ Time: {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Robotics Project",
            key=f"robotics_delete_{i}",
        ):

            delete_item(
                "robotics",
                i,
            )


# ============================================================
# DRONES
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

    with st.form("drone_form"):

        project = st.text_input(
            "🚁 Mission / Project"
        )

        c1, c2 = st.columns(2)

        platform = c1.selectbox(
            "🛩️ Platform",
            platforms,
        )

        controller = c2.selectbox(
            "🎛️ Controller",
            controllers,
        )

        c3, c4 = st.columns(2)

        sensor = c3.selectbox(
            "📡 Primary Sensor",
            sensors,
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
            ],
        )

        mission = st.text_area(
            "🎯 Mission Objective"
        )

        c5, c6 = st.columns(2)

        due_date = c5.date_input(
            "📅 Mission Date",
            value=date.today(),
        )

        due_time = c6.time_input(
            "⏰ Mission Time",
            value=time(16, 0),
        )

        notification = st.checkbox(
            "🔔 Mission Notification",
            value=True,
        )

        submit = st.form_submit_button(
            "➕ Add Mission"
        )

        if submit:

            if project.strip():

                st.session_state.drones.append(
                    {
                        "project": project.strip(),
                        "platform": platform,
                        "controller": controller,
                        "sensor": sensor,
                        "navigation": navigation,
                        "mission": mission,
                        "due_date": due_date,
                        "due_time": due_time,
                        "notification": notification,
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
            f"🚁 **{safe_value(item, 'project')}**\n\n"
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
            f"📅 Date: {safe_date(item)} | "
            f"⏰ Time: {safe_time(item)} | "
            f"🔔 {'ON' if safe_bool(item) else 'OFF'}"
        )

        if st.button(
            "🗑️ Delete Mission",
            key=f"drone_delete_{i}",
        ):

            delete_item(
                "drones",
                i,
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 OMNI AI | "
    "Omni-Agentic Intelligent Automation System | "
    "10 AI Agents | "
    "Demo + Grok + OpenAI API Modes | "
    "Streamlit + Python | "
    "No Database Dependency"
)
