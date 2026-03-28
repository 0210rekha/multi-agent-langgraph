# multi-agent-langgraph

# Multi-Agent AI System with LangGraph + Ollama

A fully local multi-agent AI pipeline built with LangGraph and Mistral (via Ollama). No OpenAI API key required — runs entirely on your machine.

---

## What It Does

Three specialized agents collaborate to answer any query:

- **Supervisor** — orchestrates the workflow, decides which agent to call next
- **Researcher** — uses the LLM to gather and summarize relevant information
- **Writer** — takes the research and produces a clean, well-structured final answer

---

## Architecture

```
User Query
    ↓
Supervisor ──→ Researcher ──┐
    ↓                       │ (loop back)
Supervisor ──→ Writer   ────┘
    ↓
   END
```

Built on LangGraph's `StateGraph` — each agent is a node, routing is handled by conditional edges, and all agents share a common `TypedDict` state.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agent orchestration graph |
| [LangChain](https://github.com/langchain-ai/langchain) | LLM abstraction layer |
| [Ollama](https://ollama.com/) | Run Mistral locally |
| [Mistral](https://mistral.ai/) | Local LLM |
| Python 3.10+ | Language |

---

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running

### 1. Clone the repo

```bash
git clone https://github.com/your-username/multi-agent-langgraph.git
cd multi-agent-langgraph
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install langgraph langchain-ollama langchain-core
```

### 4. Pull the Mistral model

```bash
ollama pull mistral
```

### 5. Start Ollama

```bash
ollama serve
```

### 6. Run the agent

```bash
python multi_agent.py
```

---

## Example Output

```
Starting multi-agent pipeline...

[Researcher] Fetching info...
[Researcher] Done.
[Writer] Writing final answer...
[Writer] Done.

=== Research ===
RAG (Retrieval-Augmented Generation) is a technique that combines...

=== Final Answer ===
Retrieval-Augmented Generation (RAG) is an AI approach that enhances...
```

---

## Project Structure

```
multi-agent-langgraph/
│
├── multi_agent.py       # Main agent pipeline
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## Key Concepts Learned

- **StateGraph** — LangGraph's core abstraction for building stateful agent workflows
- **Conditional edges** — route execution to different nodes based on current state
- **Loop-back edges** — agents report back to supervisor after each task
- **Local LLMs** — run powerful models privately with zero API costs

---

## Next Steps

- [ ] Add RAG retriever to the Researcher node
- [ ] Add a document loader for PDF/text files
- [ ] Add memory/checkpointing for multi-turn conversations
- [ ] Build a simple web UI with Streamlit

---

## Requirements

```
langgraph
langchain-ollama
langchain-core
```

---

## License

MIT License — feel free to use and modify.

---

## Author

Built by Rekha while learning agentic AI with LangGraph and Ollama.
