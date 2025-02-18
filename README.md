# agentic-observability-bot
Agentic AI implementation of observability 

# Supported python version
>=python 3.10

# Pre-requisites

1. Have ceph cluster with prometheus and telemetry enabled.
2. PostgreSQL should be up and running.
3. python3.10 is supported version
4. ollama to be installed in your machine.
5. Run
```
ollama pull deepseek-r1
```


# To run the UI Bot (frontend) code
1. source venv/bin/activate
2. git clone git@github.com:HaruChebrolu/agentic-observability-bot.git
3. cd agentic-observability-bot/
4. update username,password and database values in backend/.env
5. pip install -r backend/requirements.txt
6. pip install -r frontend/requirements.txt
7. cd frontend
8. streamlit run frontend.py

# To run the UI Bot backend code
1. python3 -m venv venv
2. source venv/bin/activate
3. git clone git@github.com:HaruChebrolu/agentic-observability-bot.git
4. cd agentic-observability-bot/
5. update username,password and database values in backend/.env
6. pip install -r frontend/requirements.txt
7. cd backend
8. python3 agent.py
