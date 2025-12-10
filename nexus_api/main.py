"""
QuantumFlow Engine - FastAPI Application.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from nexus_api.pulse_engine.executor import GraphExecutor
from nexus_api.pulse_engine.tool_hub import tool_hub
from nexus_api.pulse_engine.memory_core import state_manager
from nexus_api.schemas.flow_models import (
    CreateGraphRequest, RunGraphRequest, PrismRunRequest,
    Graph, NodeConfig
)
from nexus_api.agents.code_prism import register_prism_tools

# Initialize FastAPI
app = FastAPI(
    title="QuantumFlow Engine",
    description="Modular workflow orchestration system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register workflow tools
register_prism_tools(tool_hub)

# Initialize executor
executor = GraphExecutor(tool_hub, state_manager)

@app.get("/", tags=["system"])
async def root():
    """API root endpoint."""
    return {
        "engine": "QuantumFlow",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "tools_registered": tool_hub.count()
    }

@app.get("/health", tags=["system"])
async def health_check():
    """System health check."""
    return {
        "status": "QuantumFlow operational",
        "tools_registered": tool_hub.count(),
        "version": "1.0.0"
    }

@app.post("/graph/create", tags=["workflow"])
async def create_graph(request: CreateGraphRequest):
    """Register a new workflow graph."""
    try:
        # Convert to NodeConfig objects
        nodes = {
            k: NodeConfig(**v) for k, v in request.nodes.items()
        }
        
        graph = Graph(
            name=request.name,
            nodes=nodes,
            edges=request.edges,
            start_node=request.start_node,
            description=request.description
        )
        
        graph_id = executor.register_graph(graph)
        
        return {
            "graph_id": graph_id,
            "message": "Graph registered successfully",
            "nodes": list(nodes.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/graph/run", tags=["workflow"])
async def run_graph(request: RunGraphRequest):
    """Execute a workflow graph."""
    try:
        run = await executor.execute(
            request.graph_id,
            request.initial_state
        )
        
        exec_time = None
        if run.completed_at:
            exec_time = (run.completed_at - run.started_at).total_seconds()
        
        return {
            "run_id": run.run_id,
            "status": run.status,
            "final_state": run.state,
            "logs": [
                {
                    "timestamp": log.timestamp.isoformat(),
                    "level": log.level.value,
                    "message": log.message
                }
                for log in run.logs
            ],
            "execution_time_seconds": exec_time,
            "error": run.error
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/state/{run_id}", tags=["workflow"])
async def get_run_state(run_id: str):
    """Get workflow run status."""
    run = state_manager.get_run(run_id)
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    exec_time = None
    if run.completed_at:
        exec_time = (run.completed_at - run.started_at).total_seconds()
    
    return {
        "run_id": run.run_id,
        "status": run.status,
        "current_state": run.state,
        "execution_time_seconds": exec_time
    }

@app.post("/prism/run", tags=["agents"])
async def run_prism_agent(request: PrismRunRequest):
    """Execute the Code Review (Prism) workflow."""
    # Build Prism graph
    graph = Graph(
        name="CodePrism",
        nodes={
            "extract": NodeConfig(
                type="function", 
                function="function_extractor"
            ),
            "analyze": NodeConfig(
                type="function",
                function="complexity_analyzer"
            ),
            "suggest": NodeConfig(
                type="function",
                function="improvement_suggester"
            ),
            "checkpoint": NodeConfig(
                type="function",
                function="quality_checkpoint"
            )
        },
        edges={
            "extract": "analyze",
            "analyze": "suggest",
            "suggest": "checkpoint",
            "checkpoint": {
                "type": "conditional",
                "condition": "stop == True",
                "if_true": "end",
                "if_false": "extract"
            }
        },
        start_node="extract"
    )
    
    graph_id = executor.register_graph(graph)
    
    # Execute workflow
    run = await executor.execute(graph_id, {
        "code": request.code,
        "threshold": request.threshold,
        "max_iterations": request.max_iterations,
        "iteration": 0,
        "quality_score": 0
    })
    
    exec_time = None
    if run.completed_at:
        exec_time = (run.completed_at - run.started_at).total_seconds()
    
    return {
        "run_id": run.run_id,
        "status": run.status,
        "final_state": run.state,
        "execution_log": [
            {
                "step": i + 1,
                "timestamp": log.timestamp.isoformat(),
                "message": log.message
            }
            for i, log in enumerate(run.logs)
        ],
        "execution_time_seconds": exec_time
    }