"""
Flow Models - Pydantic schemas for requests and responses.
"""
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class NodeConfig(BaseModel):
    """Node configuration in a graph."""
    type: str = Field(..., description="Node type: 'function', 'condition'")
    function: Optional[str] = Field(None, description="Tool function name")
    config: Optional[Dict[str, Any]] = Field(None, description="Additional config")

class Graph(BaseModel):
    """Workflow graph definition."""
    name: str
    nodes: Dict[str, NodeConfig]
    edges: Dict[str, Any]
    start_node: str
    description: Optional[str] = None

class LogLevel(str, Enum):
    """Log severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class ExecutionLog(BaseModel):
    """Single log entry during execution."""
    timestamp: datetime
    level: LogLevel
    message: str

class WorkflowRun(BaseModel):
    """Represents a workflow execution."""
    run_id: str
    graph_id: str
    state: Dict[str, Any]
    status: str
    logs: List[ExecutionLog]
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

class CreateGraphRequest(BaseModel):
    """Request to create a new graph."""
    name: str
    nodes: Dict[str, Dict[str, Any]]
    edges: Dict[str, Any]
    start_node: str
    description: Optional[str] = None

class RunGraphRequest(BaseModel):
    """Request to run a graph."""
    graph_id: str
    initial_state: Dict[str, Any]

class PrismRunRequest(BaseModel):
    """Request for Code Review workflow."""
    code: str = Field(..., description="Source code to review")
    threshold: int = Field(70, description="Quality score threshold")
    max_iterations: int = Field(3, description="Maximum refinement loops")