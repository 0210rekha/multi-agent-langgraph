from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# ── 1. State ──────────────────────────────────────────────
class AgentState(TypedDict):
    query: str
    research: str
    final_answer: str
    next: str

# ── 2. LLM - Mistral via Ollama (no API key needed) ───────
llm = ChatOllama(model="mistral", temperature=0)

# ── 3. Nodes ──────────────────────────────────────────────
def supervisor(state: AgentState) -> dict:
    if not state.get("research"):
        return {"next": "researcher"}
    if not state.get("final_answer"):
        return {"next": "writer"}
    return {"next": "END"}

def researcher(state: AgentState) -> dict:
    print("[Researcher] Fetching info...")
    messages = [
        SystemMessage(content="You are a researcher. Find key facts about the topic. Be concise."),
        HumanMessage(content=state["query"])
    ]
    response = llm.invoke(messages)
    print("[Researcher] Done.")
    return {"research": response.content}

def writer(state: AgentState) -> dict:
    print("[Writer] Writing final answer...")
    messages = [
        SystemMessage(content="You are a writer. Use the research to write a clear, helpful answer."),
        HumanMessage(content=f"Query: {state['query']}\n\nResearch: {state['research']}")
    ]
    response = llm.invoke(messages)
    print("[Writer] Done.")
    return {"final_answer": response.content}

# ── 4. Routing ────────────────────────────────────────────
def route(state: AgentState) -> Literal["researcher", "writer", "__end__"]:
    n = state.get("next", "")
    if n == "researcher":
        return "researcher"
    if n == "writer":
        return "writer"
    return "__end__"

# ── 5. Build graph ────────────────────────────────────────
graph = StateGraph(AgentState)

graph.add_node("supervisor",  supervisor)
graph.add_node("researcher",  researcher)
graph.add_node("writer",      writer)

graph.set_entry_point("supervisor")

graph.add_conditional_edges("supervisor", route)
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer",     "supervisor")

app = graph.compile()

# ── 6. Run ────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting multi-agent pipeline...\n")

    result = app.invoke({
        "query": "What is retrieval-augmented generation?",
        "research": "",
        "final_answer": "",
        "next": ""
    })

    print("\n=== Research ===")
    print(result["research"])
    print("\n=== Final Answer ===")
    print(result["final_answer"])