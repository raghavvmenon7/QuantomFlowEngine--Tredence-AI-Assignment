# QuantumFlow Engine – Tredence AI Engineering Assignment

**QuantumFlow Engine** is a modular and extensible workflow/graph execution engine built using **FastAPI** and **Python**. Designed to satisfy the requirements of the Tredence AI Engineering Assignment, it provides a clean backend architecture for defining agentic pipelines, managing state, and executing logic loops.

This project implements **Option A: Code Review Agent** (internally named "Code Prism") to demonstrate the engine's capabilities in handling branching, looping, and state retention.

## Features

### Core Engine
* **Quantum Graph Engine:** Workflows are represented as directed graphs where nodes map to Python functions and edges define transitions.
* **State-Driven Architecture:** A shared state dictionary flows through all nodes, allowing for dynamic data modification and persistence.
* **Nexus Tool Registry:** A centralized registry where all node functions are stored, allowing for flexible extension of new tools without modifying the core engine.
* **Control Flow:** Supports conditional routing (branching) and iterative loops (e.g., refining code until a quality threshold is met).
* **In-Memory Runtime:** Efficiently stores graph definitions, active run states, and execution logs in memory for low-latency performance.

### Example Workflow: Code Prism (Option A)
The engine implements a complete code review pipeline that iteratively improves code quality:
1.  **Extract** – Parses input code to identify functions and structure.
2.  **Analyze** – Calculates complexity metrics and identifies stylistic or logical issues.
3.  **Suggest** – Generates specific refactoring suggestions based on analysis.
4.  **Checkpoint (Loop)** – Evaluates the quality score against a threshold. If the score is insufficient, the workflow loops back to refinement (up to a max iteration limit).

## API Endpoints

The system exposes a clean REST interface via FastAPI:

* `GET /health` – Service health check to verify availability.
* `POST /prism/run` – triggers the prebuilt **Code Prism** (Option A) workflow.
* `GET /docs` – Interactive Swagger UI documentation.
* `GET /redoc` – ReDoc API documentation.

## Installation

Clone the repository and install the required dependencies:

```bash
Running the Server
Start the FastAPI server using Uvicorn:

Bash

python -m uvicorn nexus_api.main:app --reload
The API will be available at:

API Docs: http://127.0.0.1:8000/docs

Health Check: https://www.google.com/search?q=http://127.0.0.1:8000/health

Usage Examples
Running the Code Review Agent
You can trigger the "Code Prism" workflow using curl or Postman.

Request:

Bash

curl -X POST "[http://127.0.0.1:8000/prism/run](http://127.0.0.1:8000/prism/run)" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def bad_function():\n    print(\"this is messy\")",
    "threshold": 90,
    "max_iterations": 3
  }'
Response: The API will return a JSON object containing the run_id, the final_state (with quality scores and suggestions), and a detailed execution_log.

Project Structure
Plaintext

QuantumFlowEngine/
│
├── nexus_api/
│   ├── main.py                  # FastAPI application entry point
│   │
│   ├── pulse_engine/
│   │   ├── executor.py          # Core workflow execution logic
│   │   ├── tool_hub.py          # Nexus Registry for tool management
│   │   └── memory_core.py       # In-memory storage for graphs/runs
│   │
│   ├── data_models/
│   │   └── flow_models.py       # Pydantic schemas for requests/responses
│   │
│   └── agents/
│       └── code_prism.py        # Option A workflow definition & tools
│
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
Future Improvements
Given more time, the following features would be added to enhance production readiness:

Persistent Storage: Migrate from memory_core.py to a proper database (SQLite/PostgreSQL) to persist run history across server restarts.

Async Execution: Fully leverage Python's asyncio for non-blocking execution of long-running tools.

Dynamic Graph Creation: Expose an endpoint to define new graphs via JSON payload (rather than hardcoding them in agents/).

WebSocket Streaming: Stream logs to the client in real-time as nodes complete execution.

Design Decisions
Simplicity over Complexity: The engine uses a straightforward graph traversal algorithm to ensure clarity and ease of debugging.

Centralized Tooling (Nexus): Decoupling tools from the graph logic allows them to be tested independently and reused across different workflows.

Pydantic for Data: Strict typing ensures that state transitions are valid and reduces runtime errors.

In-Memory Storage: Chosen for this assignment to keep the setup minimal and focused on logic rather than infrastructure overhead.

License
MIT License - Feel free to use this as a learning resource or a base for your own agentic workflows.
git clone [https://github.com/](https://github.com/)<your-username>/quantum-flow-engine.git
cd QuantumFlowEngine
pip install -r requirements.txt

