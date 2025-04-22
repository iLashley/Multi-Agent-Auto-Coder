# config.py

import os

# Environment variables or default configurations for models
ORCHESTRATOR_MODEL = os.getenv('ORCHESTRATOR_MODEL', 'llama3.1:latest')
SUBAGENT_MODEL = os.getenv('SUBAGENT_MODEL', 'llama3.1:latest')
REFINER_MODEL = os.getenv('REFINER_MODEL', 'llama3.1:latest')
CONSULTANT_MODEL = os.getenv('CONSULTANT_MODEL', 'llama3.1:latest')
BUGFIXER_MODEL = os.getenv('BUGFIXER_MODEL', 'llama3.1:latest')
CODER_MODEL = os.getenv('CODER_MODEL', 'llama3.1:latest')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://192.168.1.4:11434')
