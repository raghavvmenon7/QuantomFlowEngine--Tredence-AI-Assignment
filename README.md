# QuantumFlow Engine – Tredence AI Engineering Assignment

QuantumFlow Engine is a modular and extensible workflow/graph execution engine built using FastAPI and Python.
It is designed to satisfy the requirements of the Tredence AI Engineering Assignment and demonstrates the following capabilities:

* A minimal workflow execution engine
* State-driven node transitions
* Tool/function registry
* Conditional routing and loop logic
* Clean REST API interface
* Complete implementation of **Option A: Code Review Agent**

This backend uses a structured and scalable architecture designed for clarity, modularity, and maintainability.

## Key Features

### 1. Quantum Graph Engine

* Workflows represented as directed graphs
* Nodes mapped to Python functions (tools)
* Edges define node-to-node transitions
* A shared state dictionary flows through all nodes
* Supports looping and branching using conditional logic

### 2. Tool Registry (Nexus)

* All node functions are registered globally in the Nexus Registry
* Tools operate on the same state object
* Allows flexible extension of new tools without modifying the core engine

### 3. In-Memory Runtime

* Stores graph definitions (graph_id)
* Run details (run_id)
* Current node and State snapshots
* Execution logs

### 4. FastAPI REST Endpoints

* **GET /health** – Service health check
* **POST /prism/run** – Run the prebuilt Option A workflow
* **GET /docs** – Interactive API documentation

## Example Workflow – Option A: Code Review Agent

Implements the steps specified in the assignment for the "Code Prism" workflow:

1. **Extract:** Parses input code to identify functions.
2. **Analyze:** Calculates complexity and identifies stylistic or logical issues.
3. **Suggest:** Generates specific refactoring suggestions.
4. **Checkpoint:** Evaluates the quality score. If below threshold, loops back to refinement.

## Architecture Overview

```text
QuantumFlowEngine/
│
├── nexus_api/
│   ├── main.py                  # FastAPI application and routes
│   │
│   ├── pulse_engine/
│   │   ├── executor.py          # Core workflow executor
│   │   ├── tool_hub.py          # Tool registry for node functions
│   │   └── memory_core.py       # In-memory graphs and execution runs
│   │
│   ├── data_models/
│   │   └── flow_models.py       # Pydantic request/response schemas
│   │
│   └── agents/
│       └── code_prism.py        # Option A workflow tools and graph
│
└── README.md
How to Run the Project
1. Install Dependencies
Bash

pip install -r requirements.txt
2. Start the Server
Bash

python -m uvicorn nexus_api.main:app --reload
3. Verify Service Availability
http://127.0.0.1:8000/docs

Running Option A Workflow
Endpoint POST /prism/run

Example Request
{
  "code": "def bad_function():\n    print('this is messy')",
  "threshold": 90,
  "max_iterations": 3
}
