# QuantumFlow Engine  
**Tredence AI Engineering Assignment**

**QuantumFlow Engine** is a modular, extensible, graph-driven workflow execution system built using **FastAPI** and **Python**.  
It is inspired by LangGraph and implements a complete **Code Review Mini-Agent** pipeline featuring branching, looping, tool orchestration, and shared-state propagation.

This backend demonstrates a clean, scalable, and production-ready architecture while satisfying all requirements of the Tredence AI Engineering assignment.

---

## Key Features

### 1. Quantum Graph Engine
* **Directed Graph Workflows:** Each workflow is represented as a graph of nodes and edges controlling execution order.  
* **Shared State Model:** A Pydantic-validated state object flows across all nodes, ensuring safety and transparency.  
* **Branching & Looping:** Supports conditional routing and repeated execution cycles (e.g., quality improvement loops).  
* **Execution Logging:** Generates timestamped logs for every step of every run.

### 2. Nexus Tool Registry
* **Centralized Registry:** All functional tools used by nodes are registered globally in the Nexus registry.  
* **Extensible:** Developers can add new tools without modifying core engine logic.  
* **Decoupled Workflows:** Nodes reference tools by name, enabling declarative graph definitions.

### 3. In-Memory Runtime
* Stores workflow graph definitions.  
* Maintains active workflow runs and their execution logs.  
* Preserves state snapshots for inspection via APIs.  

### 4. REST API Suite
QuantumFlow exposes a clean set of HTTP endpoints:

* **GET /health** – Health check  
* **POST /graph/create** – Register a new workflow graph  
* **POST /graph/run** – Execute a graph with initial state  
* **GET /graph/state/{run_id}** – Retrieve complete run logs + final state  
* **GET /graph/{graph_id}/definition** – View graph structure  
* **GET /graph/list** – List all graphs  
* **POST /tools/register** – Register a new tool dynamically  
* **GET /tools/list** – View all registered tools  

---

## Example Workflow – Code Review Agent (Quantum Prism)

QuantumFlow includes a full implementation of the **Code Review Agent**, nicknamed **Quantum Prism**.  
It autonomously parses Python code, analyzes complexity, detects issues, generates suggestions, and iterates until quality reaches a target threshold.

### Workflow Logic
1. **Extract Functions** – Parses Python code to detect function definitions.  
2. **Check Complexity** – Evaluates parameter count and basic complexity heuristics.  
3. **Detect Issues** – Checks for long lines, TODO comments, missing docstrings, and code smells.  
4. **Suggest Improvements** – Generates actionable refactoring tips.  
5. **Compute Quality Score** – Produces a numeric score from 0 to 100.  
6. **Loop Node** – If score < threshold, rerun improvements (max 3 cycles).

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/quantumflow-engine.git
cd quantumflow-engine
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8000
```

Access:

* **API Docs:** http://localhost:8000/docs  
* **ReDoc:** http://localhost:8000/redoc  
* **Health:** http://localhost:8000/health  

---

## Usage Examples

### Running the Quantum Prism Code Review Workflow

```bash
curl -X POST "http://localhost:8000/graph/run" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "code_review_default",
    "initial_state": {
      "code": "def calculate(a, b, c, d, e):\n    return a + b + c + d + e"
    }
  }'
```

The response returns:

* `run_id` — Unique identifier for this execution  
* `final_state` — End state after all nodes complete  
* `execution_log` — Timestamped node-by-node trace  

### Creating a Custom QuantumFlow Graph

```bash
curl -X POST "http://localhost:8000/graph/create" \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": [
      {
        "name": "extract",
        "tool_name": "extract_functions",
        "inputs": {"code": "$code"}
      },
      {
        "name": "check_complexity",
        "tool_name": "check_complexity",
        "inputs": {"functions": "$extracted_functions"}
      }
    ],
    "edges": {
      "extract": "check_complexity"
    },
    "graph_id": "my_custom_graph"
  }'
```

### Fetching Run State

```bash
curl -X GET "http://localhost:8000/graph/state/{run_id}"
```

---

## Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=app --cov-report=html
```

---

## Project Structure

```
quantumflow-engine/
├── app/
│   ├── main.py                    # FastAPI entry point
│   ├── api/
│   │   ├── router_workflow.py     # Graph endpoints
│   │   └── router_tools.py        # Tool registry endpoints
│   ├── engine/
│   │   ├── workflow_engine.py     # Core graph executor
│   │   ├── node.py                # Node + loop node definitions
│   │   └── state.py               # Shared Pydantic state model
│   ├── tools/
│   │   ├── builtins.py            # Built-in code-review tools
│   │   └── registry.py            # Nexus tool registry
│   └── workflows/
│       └── code_review_workflow.py # Quantum Prism workflow
├── tests/
│   └── test_workflow.py
├── requirements.txt
└── README.md
```

---

## What the Engine Supports

* **Nodes:** Functions that read/modify state  
* **Edges:** Explicit transitions linking nodes  
* **State:** Pydantic model ensuring safe state propagation  
* **Branching:** Route execution based on conditions  
* **Looping:** Re-run segments until constraints are met  
* **Run Tracking:** Each run captures logs + final state  
* **Tool Registry:** Register and execute tools dynamically  
* **Async-Ready:** Engine supports async functions  

---

## Future Improvements

With additional time, QuantumFlow could support:

1. **Persistent Storage**  
   * Move from in-memory to PostgreSQL/SQLite  
   * Persist workflow history and states  

2. **WebSocket Streaming**  
   * Real-time logs as nodes execute  

3. **Advanced Branching**  
   * Multi-branch routing  
   * Conditional edge selection  

4. **Background Execution**  
   * Run long workflows asynchronously  
   * Celery/RQ-backed workers  

5. **Better Error Handling**  
   * Retry logic  
   * Node fallback policy  

6. **Flexible State Merge Strategies**  
   * Pluggable merge behavior instead of fixed updates  

7. **Graph Visualization**  
   * Mermaid/Graphviz DAG rendering  
   * Execution trace visualization  

8. **Additional Built-in Tools**  
   * Deeper AST code analysis  
   * Support for multiple languages  
   * External LLM or lint integrations  

---

## Design Decisions

* **Modularity:** Engine is workflow-agnostic; tools define behavior.  
* **Explicit Edges:** Ensures transparent debugging.  
* **Pydantic State:** Guarantees type-safe state flow.  
* **In-Memory Simplicity:** Ideal for demo and extension.  
* **Structured Logging:** Debug-friendly execution insights.  

---

## License

MIT License — Feel free to extend, reuse, or customize this engine for your own projects.
