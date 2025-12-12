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
git clone [https://github.com/](https://github.com/)<your-username>/quantum-flow-engine.git
cd QuantumFlowEngine
pip install -r requirements.txt
