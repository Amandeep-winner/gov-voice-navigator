# Gov Voice Navigator

A voice-enabled government ecosystem designed to simplify document renewals, navigate welfare schemes, and provide instant emergency legal assistance through intelligent voice agents. 

This project unifies a **Vue.js/Tailwind Frontend** equipped with the Vapi.ai Web SDK, tightly coupled with a **Flask API Backend** utilizing Qdrant Vector Databases and background notification systems.

---

## 🚀 Setup & Local Configuration

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Qdrant Vector DB** (Accessible via Qdrant Cloud or running locally via Docker)

### 2. Backend Setup (Flask API)
1. **Navigate to the Backend Directory:**
   ```bash
   cd backend
   ```
2. **Create & Activate your Virtual Environment:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Configuration:**
   Ensure you have a `.env` file in the `/backend` folder with your LLM configuration and Qdrant cluster keys:
   ```env
   GEMINI_API_KEY="your-gemini-key"
   # Add QDRANT_URL and QDRANT_API_KEY if using cloud vector store
   ```
5. **Run the Backend Server:**
   ```bash
   python run.py
   ```
   *(The background APScheduler scanning for expiring documents will start automatically inside the context).*

### 3. Frontend Setup (Vue 3 / Vite)
1. **Navigate to the Frontend Directory:**
   ```bash
   cd frontend
   ```
2. **Install Node Modules:**
   ```bash
   npm install
   ```
3. **Configure the Vapi Environment:**
   Create a `.env` file inside the `frontend` root:
   ```env
   VITE_VAPI_PUBLIC_KEY="your-vapi-public-key"
   VITE_VAPI_ASSISTANT_ID="your-vapi-assistant-id"
   ```
   *You can get these from your [Vapi Dashboard](https://dashboard.vapi.ai).*
4. **Run the Development Server:**
   ```bash
   npm run dev
   ```

---

## 📂 System Architecture & File Structure

Here is a high-level overview of where core logic execution lives:

```text
gov-voice-navigator/
│
├── backend/                  # Python/Flask Backend Powering the API Tools
│   ├── app/                  
│   │   ├── __init__.py       # Initializes Flask, CORS, SQLite DB, and APScheduler background tasks
│   │   ├── routes/           # API endpoints (Controllers)
│   │   │   ├── vapi_routes.py    # Native endpoints called automatically by Vapi for scheme queries
│   │   │   ├── user_routes.py    # Endpoints managing profiles
│   │   │   └── forum_routes.py   # Endpoints for the community forum logic
│   │   │
│   │   ├── services/         # Core business logic processing
│   │   │   ├── agent_service.py  # LLM query embeddings and generation with Google Gemini
│   │   │   └── scanner.py        # APScheduler chronological daemon to identify expiring documents
│   │   │
│   │   ├── models/           # SQLite Database schemas (SQLAlchemy)
│   │   │   ├── user.py           # User architecture
│   │   │   ├── forum.py          # Threads and posts
│   │   │   └── notification.py   # ActiveSchemes and UserAlerts triggered by scanner
│   │
│   ├── data/                 # Raw data storage (Mock databases / SQLite structure)
│   ├── scripts/              # Utility scripts (like seeders for initial vector uploads)
│   ├── requirements.txt      # Python dependencies
│   ├── vapi_tools_config.json# The JSON definition loaded into Vapi outlining backend functions
│   └── run.py                # Waitress/Werkzeug entry point to start the Flask server
│
└── frontend/                 # Vue.js 3 + Vite Frontend Shell
    ├── public/               
    ├── src/
    │   ├── components/       # Discrete Reusable HTML Modules
    │   │   └── VoiceWidget.vue     # The global pulsating Vapi microphone logic
    │   │
    │   ├── views/            # Full-page macro layouts via vue-router
    │   │   ├── Dashboard.vue       # Main user dashboard highlighting notifications
    │   │   ├── CommunityForum.vue  # Quora-style thread visualization
    │   │   ├── GovDashboard.vue    # Admin portal to digitize and vectorize gazettes
    │   │   └── SchemeComparison.vue# Matrix UI (Feature 8) for side-by-side scheme analysis
    │   │
    │   ├── router/           
    │   │   └── index.ts            # Maps Frontend URLs (e.g., '/compare') to Views
    │   │
    │   ├── App.vue           # Root Component (Global Navigation Menu and Glassmorphism Shell)
    │   └── main.ts           # Vue Application Instantiation and Pinia mounting
    │
    ├── .env                  # Frontend Environment logic
    ├── package.json          # Node dependency hierarchy
    └── tailwind.config.js    # Styling engine config tailored for modern design
```