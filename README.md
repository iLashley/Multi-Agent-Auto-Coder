
# Multi-Agent-Auto-Coder 
  (Click on Gif below to open in a new tab)
![Multi-Agent-Auto-Coder](https://github.com/user-attachments/assets/3d8fc2d2-9e99-477a-b3c2-b0679f0a1ab5)

A modular, agent-based AI framework that can plan, write, run, debug, and improve code automatically — or even tackle non-coding tasks. It was originally built to work with local LLMs using [Ollama](https://ollama.com), but can also use cloud-based models like OpenAI’s.

---

## Features

- **Task-to-code pipeline**: Breaks down tasks, writes code, tests it, and fixes problems in a loop
- **Project scaffolding**: Builds and names project folders using LLMs
- **Execution feedback**: Runs code in a temporary virtual environment and tries to correct errors automatically
- **Modular agents**:
  - `Orchestrator`: Breaks down goals into steps
  - `SubAgent`: Handles task execution
  - `Architect`: Builds the project layout
  - `CodeReviewer`: Suggests improvements or fixes
  - `Consultant`: Gives high-level strategy advice
  - `Overseer`: Logs and approves results
  - `Coder`: Writes the code

CLI options like `--dry-run` and `--no-cleanup` let you preview or persist results.

---

## Requirements

- Python 3.9+
- One of the following:
  - [Ollama](https://ollama.com) with models like `llama3`, `codestral`, etc.
  - OpenAI API access (e.g. GPT-4 or GPT-3.5)

### Running with Ollama

Make sure the models are installed:

```bash
ollama run llama3
ollama run codestral
```

### Using OpenAI

Set your API key:

```bash
export OPENAI_API_KEY=your-key-here
```

---

## Model Configuration

Each agent is configurable through `config.py`, and you can use any local or API-based model that’s compatible. Set these using environment variables:

```python
# config.py

import os

ORCHESTRATOR_MODEL = os.getenv('ORCHESTRATOR_MODEL', 'llama3.1:latest')
SUBAGENT_MODEL     = os.getenv('SUBAGENT_MODEL', 'llama3.1:latest')
REFINER_MODEL      = os.getenv('REFINER_MODEL', 'llama3.1:latest')
CONSULTANT_MODEL   = os.getenv('CONSULTANT_MODEL', 'llama3.1:latest')
BUGFIXER_MODEL     = os.getenv('BUGFIXER_MODEL', 'llama3.1:latest')
CODER_MODEL        = os.getenv('CODER_MODEL', 'llama3.1:latest')

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
```

Example:

```bash
export ORCHESTRATOR_MODEL="gpt-4"
export CODER_MODEL="codestral"
```

---

## Usage

### Interactive mode:

```bash
python main.py
```

### With CLI flags:

```bash
python main.py --objective "Build a CSV parser" --dry-run
```

---

## Project Layout

```
agentic_toolset/
├── core/
│   ├── project_manager.py
│   └── venv_manager.py
├── agents/
│   ├── reviewer.py
│   ├── architect.py
│   └── ...
├── utils/
│   └── display.py
├── config.py
main.py
```

---

## Example Tasks (Simple)

- Create a project that calculates and logs Fibonacci numbers up to 100.
- Create a webscraper
- Make an audio file converter that converts mp3 to wav

---

## Roadmap

- [ ] Command-line improvements
- [x] Dry-run and cleanup flags
- [ ] Self-updating agent toolchain
- [ ] Integrated memory (local or vector-based)
- [ ] Optional web interface (Gradio, Textual)

---

Open to feedback, contributions, and ideas.
```

