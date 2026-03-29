# 🌍 AI Trip Planner Agent (MCP Integration)

An intelligent, data-aware travel planning agent built with the **Google Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**. 

This project demonstrates how to cleanly separate LLM reasoning from tool execution by securely connecting a Gemini model to the live OpenWeatherMap API via a local MCP server.



## ✨ Features

* **Context-Aware Itineraries:** Generate realistic 2-day travel plans customised to the destination's actual, live weather conditions.
* **Standardised Tooling (MCP):** Utilises the modern Model Context Protocol (v1.0+) to safely expose external APIs to the agent without hardcoding API calls into the agent's core logic.
* **Serverless Deployment:** Fully containerised and deployed on Google Cloud Run with a built-in ADK Web UI for easy testing.



## 🏗️ Architecture

1. **The Brain (`agent.py`):** An ADK `Agent` powered by `gemini-2.5-flash`. It is instructed to always check the weather before generating a plan.
2. **The Tool (`weather_mcp.py`):** A standalone MCP `stdio_server` that securely fetches live temperature and condition data from OpenWeatherMap.
3. **The Bridge (`MCPToolset`):** The ADK framework manages the execution of subprocesses and data formatting between the LLM and the MCP server.



## 🚀 Getting Started

### Prerequisites

* Python 3.12+
* Google Cloud CLI (`gcloud`) configured with an active project
* An [OpenWeatherMap API Key](https://openweathermap.org/api)



### Local Setup

1. **Clone the repository and navigate to the project folder:**
   
   ```bash
   git clone https://github.com/anirban94chakraborty/trip-planner.git
   cd trip-planner/trip_planner_agent
   ```

2. **Create and activate a virtual environment (using `uv` or `venv`):**

   ```bash
   uv venv --python 3.12
   source .venv/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your environment variables:** 

   Create a `.env` file in the root directory and add your keys:

   ```txt
   GOOGLE_GENAI_USE_VERTEXAI=1
   GOOGLE_CLOUD_PROJECT=your_project_id_here
   GOOGLE_CLOUD_LOCATION=us-central1
   PROJECT_ID=your_project_id_here
   PROJECT_NUMBER=your_project_number_here
   SA_NAME=project-service
   SERVICE_ACCOUNT=project-service@your_project_id_here.iam.gserviceaccount.com
   MODEL="gemini-2.5-flash"
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

5. **Run the agent locally**:

   ```bash
   adk run .
   ```

   *The ADK CLI will output a local port (e.g., 8080) where you can interact with the agent via a web UI.*



## ☁️ Cloud Run Deployment

This project uses the ADK CLI to automate containerization and serverless deployment to ***Google Cloud Run***.

**Deployment Command:**

```bash
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=trip-planner-agent \
  --with_ui \
  . \
  -- --service-account=$SERVICE_ACCOUNT --set-env-vars="OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY,PROJECT_ID=$PROJECT_ID,LOCATION=us-central1"
```

> **Note on Secret Management:** To maintain security best practices, the `.env` file is excluded from the container build. The OpenWeather API key and GCP configurations are securely injected at runtime using the `--set-env-vars` flag.



## 📂 Project Structure

```
trip-planner/
├── trip_planner_agent/
│   ├── __init__.py
│   ├── agent.py               # Defines the ADK Agent and MCP connection
│   ├── weather_mcp.py         # The local MCP stdio server logic
│   ├── requirements.txt       # ADK and external dependencies
│   └── .env                   # Local secrets (Ignored in deployment)
└── README.md
```