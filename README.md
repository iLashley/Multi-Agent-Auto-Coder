```markdown
# 🧠 Multi-Agent-Auto-Coder

A modular, agent-based AI framework for autonomously planning, writing, executing, debugging, and improving code — or adapting to other tasks — using local LLMs like [Ollama](https://ollama.com) or cloud-based APIs like OpenAI.

Originally designed to run and complete coding projects on your local ollama instance.
---

## 🚀 Features

- 🔄 **Task-to-code pipeline**: Agents orchestrate task breakdowns, generate scripts, review output, and self-correct errors.
- 📁 **Dynamic project structure**: Automatically names and organizes project folders using LLMs.
- 🧪 **Execution feedback loop**: Runs code in a sandboxed venv and auto-fixes issues.
- 🧰 **Multi-agent architecture**:
  - `Orchestrator`: Breaks down goals into sub-tasks
  - `SubAgent`: Executes individual task steps
  - `Architect`: Constructs project structure
  - `CodeReviewer`: Inspects and improves code
  - `Consultant`: Suggests coding strategies
  - `Overseer`: Logs and approves outputs
  - `Coder`: Generates new code blocks
  - Supports `--dry-run` and `--no-cleanup` flags

---

## 🔧 Requirements

- Python 3.9+
- Either:
  - [Ollama](https://ollama.com) with compatible models (`llama3`, `codestral`, etc.)
  - Or OpenAI API access (e.g. GPT-4)

### Running with Ollama:

```bash
ollama run llama3
ollama run codestral
```

### Using OpenAI (optional) (need to add full compatibility still):

Set your API key in an environment variable:

```bash
export OPENAI_API_KEY=your-key-here
```
or add it to the config file.
---

## ⚙️ Model Configuration

Each agent is model-configurable via `config.py`. You can set environment variables to specify which LLM each agent uses, either local (e.g. Ollama) or remote (e.g. OpenAI) you can :
In our example config.py we use llama3.latest for each model, however you may want to specify specific models for your use case and ensure each model will individually run on your system. 
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

### Customization Example

Use different models per role by setting environment variables:

```bash
export ORCHESTRATOR_MODEL="gpt-4"
export CODER_MODEL="codestral:latest"
```

This allows fine-tuned optimization per task, leveraging any model you have installed locally or accessible via an API.

---

## 🧪 Usage

### Run interactively:

```bash
python main.py
```

### Or with CLI flags:

```bash
python main.py --objective "Build a CSV parser" --dry-run
```

---

## 📦 Folder Structure

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

## 📌 Examples

### Generate a Code Project:

> "Create a project that logs Fibonacci numbers to a file."

### Future Ideas:

- Write a market research summary on AI regulations in Europe
- Draft an academic paper in LaTeX

---

## ✅ Roadmap

- [ ] CLI Tooling with agents
- [x] Dry-run / cleanup flags
- [ ] Self-updating toolchain
- [ ] Integrated memory (local or vector-based)
- [ ] Web UI (Gradio / Textual)

---
```

