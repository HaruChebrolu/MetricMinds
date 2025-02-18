# agentic-observability-bot
Agentic AI implementation of observability 

# Pre-requisites

1. Have ceph cluster with prometheus and telemetry enabled.
2. PostgreSQL should be up and running with user `postgres`, password `postgres` and table `postgres`.
3. ollama to be installed in your machine.
4. Run 
```
ollama pull llama3
```

# To run the UI Bot (frontend) code
1. source venv/bin/activate
2. git clone git@github.com:HaruChebrolu/agentic-observability-bot.git
3. cd agentic-observability-bot/
4. pip install -r backend/requirements.txt
5. pip install -r frontend/requirements.txt
6. cd frontend
7. streamlit run frontend.py

# To run the UI Bot backend code
1. python3 -m venv venv
2. source venv/bin/activate
3. git clone git@github.com:HaruChebrolu/agentic-observability-bot.git
4. cd agentic-observability-bot/
5. pip install -r backend/requirements.txt
6. cd backend
7. python3 agent.py
