# AI SQL Database Agent

![AI SQL Database Agent](https://img.shields.io/badge/Status-Active-success.svg)
![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-61DAFB.svg?logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)
![LangChain](https://img.shields.io/badge/Agent-LangChain-black.svg)
![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20LLaMA3-f54e42.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite)

An enterprise-grade, full-stack application that allows users to interact with a complex relational database using **Natural Language**. 

Built with a beautiful Glassmorphism React frontend and a highly resilient LangChain-powered FastAPI backend, this agent acts as your personal Senior Data Analyst. It securely translates human questions into optimized SQL queries, executes them against the database, and returns gorgeous Markdown-formatted tables along with professional business insights.

## Key Features

- **Natural Language to SQL**: Ask questions in plain English (e.g., *"What are the top 5 branches by revenue?"*). The AI handles the complex joins and aggregations.
- **Secure Execution Pipeline**: Queries are rigorously validated to strictly enforce `SELECT`-only read operations. SQL injection or destructive operations (`DROP`, `DELETE`) are blocked at the orchestrator level.
- **Automatic LLM Failover**: Highly resilient backend architecture. If the primary Large Language Model hits API rate limits, the system transparently reroutes the request to fallback models (e.g., LLaMA-3 70B -> LLaMA-3 8B -> Mixtral) ensuring zero downtime.
- **Dynamic Schema Introspection**: The backend dynamically scans the active database and serves the schema to the React UI in real-time.
- **Premium User Interface**: Built with custom React components, smooth CSS micro-animations, Lucide icons, and React-Markdown for stunning table renderings.
- **Conversational Awareness**: The agent is smart enough to know when you are just saying "hi" and seamlessly bypasses the SQL execution pipeline to hold a natural conversation.

## System Architecture & Agent Workflow

The core intelligence is powered by **LangChain (LCEL)** within a FastAPI service layer. When a user submits a prompt, the system executes the following strict sequence:

1. **Intent Detection**: The Agent determines if the query requires a database fetch or if it's purely conversational.
2. **Schema Injection**: If a query is needed, the live database schema (Tables, Columns, Primary Keys, Types) is injected into the prompt.
3. **SQL Generation**: The LLM acts as a Senior SQL Developer, constructing the exact syntax needed.
4. **Validation (Guardrails)**: The backend validates the query strictly for safety and correctness.
5. **Execution**: The query is run against the SQLite database.
6. **Analysis & Interpretation**: The raw JSON output is fed *back* to the LLM, which translates the raw numbers into a Markdown Table and authors a concise Business Insight.
7. **Frontend Delivery**: The payload is streamed back to the React UI for beautiful rendering.

## Project Structure

```text
SqlAgent/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # RESTful Routers (Chat & Database Schema)
│   │   ├── agent/            # LangChain Orchestrator, Prompts, & Output Parsers
│   │   ├── llm/              # LLM Provider Factory (with Automatic Failovers)
│   │   ├── services/         # Business Logic Layer
│   │   ├── tools/            # SQL Execution & Validation Tools
│   │   └── database/         # SQLite DB, DDL Schemas, & Synthetic Data Generators
│   ├── main.py               # FastAPI entry point
│   └── requirements.txt      # Python dependencies
│
└── frontend/                 # React UI
    ├── src/
    │   ├── components/       # Chat UI, Right Panel (Schema Viewer), Typewriter text
    │   ├── context/          # Global State & Theme management
    │   ├── hooks/            # Custom React Hooks (useChat, useDatabaseSchema)
    │   ├── services/         # Axios API clients
    │   └── styles/           # Glassmorphism CSS variables & globals
    ├── index.html            # Vite entry point
    └── package.json          # Node dependencies
```

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- A [Groq API Key](https://console.groq.com/keys)

### 1. Backend Setup

Navigate to the backend directory, create a virtual environment, and install dependencies:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory and add your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Generate the massive synthetic database (Wait ~30 seconds for it to build the 50,000+ relational rows):
```bash
python app/database/seed/generate_data.py
```

Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
*The backend API will now be running on `http://localhost:8000`*

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
```

Start the Vite development server:
```bash
npm run dev
```
*The React application will now be running on `http://localhost:3000`*

## Usage Example

1. Open your browser to `http://localhost:3000`
2. Click the **Databases** icon in the left sidebar to expand the Right Panel. You will see the dynamic Schema Viewer instantly introspect the 16+ active tables.
3. In the chat box, type: *"Show me the top 3 cities by total number of customers."*
4. Watch as the AI generates the SQL, executes it, and formats the result into a beautiful markdown table with an actionable business insight!

---
*Developed with using React, FastAPI, and LangChain.*
**Kaleem Malik | AI Engineer**
