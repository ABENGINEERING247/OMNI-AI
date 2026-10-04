# 🤖 OMNI AI

## Omni-Agentic Intelligent Automation System

OMNI AI is a Streamlit-based multi-agent intelligent automation platform designed to demonstrate how a central **AI Orchestrator** can communicate with and route requests to specialized AI agents.

The system supports both **Demo Mode** and **Open AI or Grok API Mode**, allowing users to test the complete agentic workflow without an API key and then connect the application to Grok AI when an `XAI_API_KEY` is available.

---

## 🚀 Key Features

### 🧠 AI Orchestrator

The central master agent analyzes the user's request and selects the appropriate specialist agent.

### 🤖 10 AI Agents

1. 🧠 **AI Orchestrator**
2. ⏰ **Daily Reminder Agent**
3. ❤️ **Health & Wellness Agent**
4. 📅 **Calendar & Schedule Agent**
5. 📚 **Learning & Education Agent**
6. 📝 **Productivity & Task Agent**
7. 💰 **Finance & Expense Agent**
8. 🌐 **Information & Communication Agent**
9. 🤖 **Robotics Agent**
10. 🚁 **Drones & Autonomous Systems Agent**

---

## 🔄 Agentic Workflow

OMNI AI demonstrates the following workflow:

```text
                    USER
                     │
                     ▼
             ┌─────────────────┐
             │  Streamlit UI   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ AI ORCHESTRATOR │
             │   Master Agent  │
             └────────┬────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
     Reminder     Calendar     Learning
       Agent        Agent        Agent
          │           │           │
          └───────────┼───────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Tasks       Finance     Wellness
       Agent        Agent        Agent
          │           │           │
          └───────────┼───────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼
      Robotics      Drones
       Agent         Agent
                      │
                      ▼
             ┌─────────────────┐
             │ Demo Engine /   │
             │ OpenAI/Grok API │
             └────────┬────────┘
                      │
                      ▼
              Structured Result
```

---

# 🎮 Demo Mode

Demo Mode does not require an API key.

It allows users to demonstrate the agentic architecture locally.

Example:

```text
User:
Create a robotics project using ESP32 and a camera.

        ↓

AI Orchestrator

        ↓

🤖 Robotics Agent

        ↓

Demo Robotics Workflow

        ↓

Structured Response
```

Another example:

```text
User:
Remind me about my AI class tomorrow at 9 AM.

        ↓

🧠 AI Orchestrator

        ↓

⏰ Daily Reminder Agent

        ↓

Reminder Workflow

        ↓

Notification
```

---

# 🔑 Open AI or Grok API Mode

Grok API Mode connects OMNI AI to the xAI API.

The application sends the user's request together with the selected specialist agent to Grok.

Example:

```text
User Request
     ↓
Agent Detection
     ↓
Selected Specialist Agent
     ↓
Open AI or Grok API
     ↓
AI Response
     ↓
Streamlit
```

The application uses the xAI Chat Completions endpoint and the configured Grok model.

---

# 💬 OMNI AI Chatbot

The chatbot provides a natural-language interface for communicating with the agents.

Example requests:

```text
Create a task for learning Python tomorrow at 6 PM.
```

```text
Schedule a meeting tomorrow at 10 AM.
```

```text
Help me design an ESP32 robotics project.
```

```text
Create a study plan for Artificial Intelligence.
```

```text
Help me organize my monthly expenses.
```

```text
Design a drone navigation system using GPS and IMU.
```

The orchestrator identifies keywords and routes the request to the corresponding specialist.

---

# 🔀 Agent Detection

OMNI AI currently uses lightweight keyword-based routing.

Examples:

| User Request Contains         | Selected Agent             |
| ----------------------------- | -------------------------- |
| reminder, alarm, deadline     | ⏰ Daily Reminder Agent     |
| health, wellness, exercise    | ❤️ Health & Wellness Agent |
| meeting, calendar, schedule   | 📅 Calendar Agent          |
| learning, study, Python, exam | 📚 Learning Agent          |
| task, todo, productivity      | 📝 Task Agent              |
| expense, finance, budget      | 💰 Finance Agent           |
| email, message, report        | 🌐 Communication Agent     |
| robot, Arduino, ESP32, sensor | 🤖 Robotics Agent          |
| drone, UAV, navigation        | 🚁 Drones Agent            |

If no specialist keyword is detected:

```text
🧠 AI Orchestrator
```

is selected.

---

# ⏰ Reminder & Notification System

OMNI AI includes a basic notification engine for scheduled items.

Supported notification categories include:

* Reminders
* Meetings
* Tasks
* Learning activities
* Wellness activities
* Expenses/payment reminders
* Communications
* Robotics projects
* Drone missions

The application can periodically refresh using:

```python
streamlit_autorefresh
```

When an item becomes due, OMNI AI can display:

* Streamlit toast notification
* In-app warning
* Browser notification when browser permissions allow it

---

# 📅 Calendar & Meetings

The Calendar Agent allows users to create:

* Meetings
* Classes
* Appointments
* Events
* Project Reviews

Each event can contain:

* Title
* Date
* Time
* Duration
* Location/platform
* Participants
* Event type
* Notification setting

---

# 📚 Learning Agent

The Learning Agent allows users to create learning activities.

Information includes:

* Subject/course
* Learning goal
* Study date
* Study time
* Notification

Example:

```text
Subject:
Generative AI

Goal:
Learn prompt engineering and LLM application development.

Date:
2026-10-05

Time:
18:00
```

---

# 📝 Productivity & Task Agent

The Task Agent supports:

* Task creation
* Due dates
* Due times
* Priority
* Completion tracking
* Notifications
* Task deletion

Priority levels:

```text
High
Medium
Low
```

---

# ❤️ Wellness Agent

The Wellness Agent can manage activities such as:

* Exercise
* Walking
* Hydration
* Meditation
* Appointments
* Other wellness activities

---

# 💰 Finance Agent

The Finance Agent provides basic expense organization.

Supported information:

* Expense/payment description
* Amount
* Category
* Payment date
* Payment time
* Notification

Categories include:

```text
Food
Transport
Education
Utilities
Shopping
Bills
Other
```

The dashboard calculates the total expenses stored during the current application session.

---

# 🌐 Communication Agent

The Communication Agent can create:

* Emails
* Announcements
* Reports
* Messages
* Notices

Users can provide:

```text
Recipient
Subject
Content
Schedule Date
Schedule Time
```

OMNI AI generates a basic structured communication and stores it in the current session.

---

# 🤖 Robotics Agent

The Robotics Agent supports project planning for robotics and embedded systems.

### Controllers

Examples include:

* Arduino Uno
* Arduino Mega
* Arduino Nano
* ESP32
* ESP8266
* Raspberry Pi
* Raspberry Pi Pico
* STM32
* PLC
* Jetson Nano
* NVIDIA Jetson Orin
* BeagleBone

### Sensors

Examples:

* Ultrasonic
* IR
* PIR
* Camera
* IMU
* GPS
* LiDAR
* Temperature
* Humidity
* Gas Sensor
* RFID
* Load Cell

### Actuators

Examples:

* DC Motor
* Servo Motor
* Stepper Motor
* Relay
* Solenoid
* Pneumatic Actuator
* Hydraulic Actuator
* Linear Actuator

### Communication

Examples:

* Wi-Fi
* Bluetooth
* BLE
* LoRa
* CAN
* UART
* I2C
* SPI
* Ethernet
* MQTT
* Modbus

---

# 🚁 Drones & Autonomous Systems Agent

The Drone Agent supports planning for autonomous platforms.

### Platforms

* Quadcopter
* Hexacopter
* Octocopter
* Fixed Wing UAV
* VTOL UAV
* UGV
* Autonomous Vehicle

### Controllers

* Pixhawk
* ArduPilot
* PX4
* Raspberry Pi
* Jetson
* ESP32
* Custom Flight Controller

### Sensors

* RGB Camera
* Depth Camera
* Thermal Camera
* LiDAR
* GPS
* IMU
* Ultrasonic
* Radar
* Computer Vision Camera

### Navigation

* GPS
* GPS + IMU
* Visual Navigation
* LiDAR Navigation
* SLAM
* Manual
* Custom

---

# 💾 Data Architecture

The current version intentionally has:

```text
No Database Dependency
```

Application data is stored in:

```python
st.session_state
```

Therefore, data is primarily session-based.

The application does not require:

* MySQL
* PostgreSQL
* SQLite
* MongoDB
* Firebase

This makes the project simple to deploy and demonstrate.

---

# 📁 Suggested Project Structure

```text
OMNI-AI/
│
├── Omniapp1.py
├── README.md
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

---

# 📦 requirements.txt

Create a file named:

```text
requirements.txt
```

with:

```text
streamlit
requests
streamlit-autorefresh
```

---

# 🔐 Streamlit Secrets

For Grok API Mode, configure the API key using Streamlit Secrets.

Create:

```text
.streamlit/secrets.toml
```

and add:

```toml
XAI_API_KEY = "YOUR_XAI_API_KEY"
```

Do **not** publish a real API key inside GitHub source code.

For Streamlit Cloud, add the key through:

```text
App
→ Settings
→ Secrets
```

---

# ▶️ Run Locally

Install Python and open a terminal in the project directory.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run Omniapp1.py
```

The application will open in the browser.

---

# 🌐 Streamlit Community Cloud Deployment

### Step 1 — Create GitHub Repository

Create a repository, for example:

```text
omni-ai
```

### Step 2 — Upload Files

Upload:

```text
Omniapp1.py
requirements.txt
README.md
```

### Step 3 — Open Streamlit Cloud

Go to:

```text
https://share.streamlit.io/
```

### Step 4 — Deploy

Select:

```text
New app
```

Select your GitHub repository and Python file:

```text
Omniapp1.py
```

Then deploy.

### Step 5 — Configure API Key

After deployment:

```text
App Settings
→ Secrets
```

Add:

```toml
XAI_API_KEY = "YOUR_XAI_API_KEY"
```

Save the secret and restart the application.

---

# 🧪 Recommended Demo Presentation

For a live demonstration, use the following sequence.

### Demo 1 — Orchestration

Enter:

```text
I need to learn Python and create a study schedule.
```

Expected routing:

```text
🧠 AI Orchestrator
        ↓
📚 Learning & Education Agent
```

---

### Demo 2 — Reminder

Enter:

```text
Remind me about my AI workshop tomorrow at 9 AM.
```

Expected routing:

```text
🧠 AI Orchestrator
        ↓
⏰ Daily Reminder Agent
```

---

### Demo 3 — Robotics

Enter:

```text
Design an ESP32 robot using an ultrasonic sensor and DC motor.
```

Expected routing:

```text
🧠 AI Orchestrator
        ↓
🤖 Robotics Agent
```

---

### Demo 4 — Drone

Enter:

```text
Help me design a GPS and IMU based autonomous drone system.
```

Expected routing:

```text
🧠 AI Orchestrator
        ↓
🚁 Drones & Autonomous Systems Agent
```

---

### Demo 5 — Finance

Enter:

```text
Help me organize my monthly expenses and budget.
```

Expected routing:

```text
🧠 AI Orchestrator
        ↓
💰 Finance & Expense Agent
```

---

# 🏗️ Technology Stack

| Technology              | Purpose                    |
| ----------------------- | -------------------------- |
| Python                  | Application logic          |
| Streamlit               | Web interface              |
| xAI Grok API            | AI reasoning               |
| Streamlit Session State | Temporary application data |
| Requests                | API communication          |
| Streamlit Autorefresh   | Notification checking      |
| GitHub                  | Source-code hosting        |
| Streamlit Cloud         | Deployment                 |

---

# 🔮 Future Development

The architecture can be extended with:

* n8n workflow automation
* WhatsApp integration
* Email automation
* Google Calendar integration
* Persistent database
* Vector database/RAG
* Local LLMs
* Ollama
* LM Studio
* GPT4All
* Voice interface
* Document processing
* Computer vision
* IoT device control
* ESP32 integration
* Raspberry Pi integration
* Robotics control
* Drone telemetry
* MQTT
* REST APIs
* Multi-agent tool calling
* Autonomous workflow execution

A future architecture could become:

```text
                    OMNI AI
                       │
                AI ORCHESTRATOR
                       │
        ┌──────────────┼──────────────┐
        │              │              │
      Agents         Tools        Knowledge
        │              │              │
        ▼              ▼              ▼
     Grok API         n8n            RAG
        │              │              │
        └──────────────┼──────────────┘
                       │
               External Services
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     WhatsApp        Email        IoT/Robotics
```

---

# ⚠️ Important Security Note

Never hard-code a production API key directly into:

```python
Omniapp1.py
```

Never commit:

```text
secrets.toml
```

containing a real API key to a public GitHub repository.

Use Streamlit Secrets or environment variables.

If an API key has already been exposed publicly, revoke/rotate it through the API provider before continuing.

---

# 🟢 Project Status

```text
OMNI AI
────────────────────────────────

Streamlit UI          ✅
10-Agent Architecture ✅
AI Orchestrator       ✅
Demo Mode             ✅
Grok API Mode         ✅
Chatbot Architecture  ✅
Reminder System       ✅
Calendar              ✅
Learning              ✅
Tasks                 ✅
Wellness              ✅
Finance               ✅
Communication         ✅
Robotics              ✅
Drone Systems         ✅
Database Dependency   ❌
```

---

## 🤖 OMNI AI

**Omni-Agentic Intelligent Automation System**

> Multi-Agent AI • Intelligent Automation • Productivity • Learning • Wellness • Communication • Finance • Robotics • Autonomous Systems

Built with:

```text
Python + Streamlit + Open AI or Grok API
```
