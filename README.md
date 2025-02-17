# agentic-observability-bot
Observability Chatbot is an AI-powered assistant designed to help engineers monitor, debug, and analyse cloud infrastructure and application performance in real time. It integrates with logging, 
metrics, and tracing platforms such as Prometheus, Grafana, Open Telemetry, and Azure Monitor. The chatbot provides quick insights into system health, failure diagnostics, and anomaly detection, reducing
the need for manual log searches and dashboard navigation.
With the increasing complexity of distributed systems, the Observability Chatbot acts as a one-stop solution for querying logs, detecting anomalies, and getting actionable recommendations, 
significantly improving Mean Time to Resolution (MTTR).

# Pre-requisites

1. Have ceph cluster with prometheus and telemetry enabled.
2. PostgreSQL should be up and running.

# Architecture diagram
<img width="1010" alt="Screenshot 2025-02-08 at 10 39 47 AM" src="https://github.com/user-attachments/assets/465fb3e5-dcc9-404d-aaa2-abab73b6ab5d" />


# To run the UI Bot (frontend) code
1. source venv/bin/activate
2. git clone git@github.com:HaruChebrolu/agentic-observability-bot.git
3. cd agentic-observability-bot/
4. pip install -r backend/requirements.txt
5. pip install -r frontend/requirements.txt
6. cd frontend
7. streamlit run frontend.py

# To run the backend code
1. python3 -m venv venv
2. source venv/bin/activate
3. git clone git@github.com:HaruChebrolu/agentic-observability-bot.git
4. cd agentic-observability-bot/
5. pip install -r backend/requirements.txt
6. cd backend
7. python3 agent.py
