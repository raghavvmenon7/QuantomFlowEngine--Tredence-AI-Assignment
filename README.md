\# QuantumFlow Engine

\*\*Tredence AI Engineering Assignment\*\*

QuantumFlow Engine is a modular, graph-based workflow execution engine built using FastAPI and Python. It is designed to demonstrate architectural clarity, state management, and extensible tool orchestration.

The system features a custom graph executor, a central tool registry (Nexus), and a complete implementation of \*\*Option A: Code Review Agent\*\*.

\## Key Capabilities

1\. \*\*Graph-Based Execution\*\*

&nbsp; Workflows are defined as directed graphs where nodes represent functional steps and edges define transitions.

2\. \*\*State-Driven Architecture\*\*

&nbsp; A shared state dictionary persists across the workflow, allowing data to flow seamlessly between independent tools.

3\. \*\*Conditional Routing \& Looping\*\*

&nbsp; The engine supports dynamic branching and iterative loops based on state conditions (e.g., repeating a step until a quality threshold is met).

4\. \*\*Decoupled Tool Registry\*\*

&nbsp; Logic is separated from execution. The Nexus Registry manages tools, making the system easily extensible without modifying the core engine.

\## Architecture Overview

The project follows a clean separation of concerns:

nexus_project/

│

├── nexus_api/

│ ├── main.py # FastAPI application entry point

│ │

│ ├── pulse_engine/ # Core Workflow Logic

│ │ ├── executor.py # Graph execution and routing

│ │ ├── tool_hub.py # Tool registration system

│ │ └── memory_core.py # In-memory state management

│ │

│ └── agents/ # Specific Agent Implementations

│ └── code_prism.py # Option A: Code Review workflow tools

│

├── requirements.txt

└── README.md

\## Installation \& Usage

\### 1. Install Dependencies

Ensure Python 3.9+ is installed.

&nbsp; pip install -r requirements.txt

\### 2. Start the Server

Launch the FastAPI application using Uvicorn.

&nbsp; python -m uvicorn nexus_api.main:app --reload

\### 3. API Documentation

Once running, the interactive API documentation is available at:

\* Docs: http://127.0.0.1:8000/docs

\* Health Check: http://127.0.0.1:8000/health

\## Code Review Agent (Option A)

This project implements the Code Review workflow ("Code Prism"). The agent autonomously analyzes Python code, checks for complexity, and iteratively suggests improvements until the quality score meets a defined threshold.

\### Workflow Logic

1\. \*\*Extract:\*\* Parses the input code to identify functions.

2\. \*\*Analyze:\*\* Calculates complexity and identifies stylistic or logical issues.

3\. \*\*Suggest:\*\* Generates specific refactoring suggestions.

4\. \*\*Checkpoint:\*\* Evaluates the quality score. If it is below the threshold, the workflow loops back to refinement.

\### How to Run

\*\*Endpoint:\*\* POST /prism/run

\*\*Sample Payload:\*\*

```json

{

&nbsp; "code": "def bad\_function():\\n    print('this is messy')",

&nbsp; "threshold": 90,

&nbsp; "max\_iterations": 3

}



Response: The API returns the final state, including the quality score, a list of suggestions, and the full execution log showing the iterative process.



Design Decisions

Modularity: The engine (Pulse) is completely agnostic of the specific agent logic (Prism). This allows new agents to be added simply by registering new tools.



Synchronous Execution: For this assignment, execution is handled synchronously to ensure strict ordering of steps and simplified debugging.



In-Memory State: Run history and state are stored in memory for performance and simplicity, appropriate for the scope of this assignment.



Future Improvements

Persistence: Integration with PostgreSQL to persist workflow states and support long-running jobs.



Async Processing: Converting tool execution to async/await patterns to handle high-latency operations (e.g., real LLM calls).



Dynamic Loading: Loading graph definitions from JSON configuration files at runtime.

```
