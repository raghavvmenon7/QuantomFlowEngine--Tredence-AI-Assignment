"""
Graph Executor - Core workflow execution engine.
"""
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from nexus_api.schemas.flow_models import (
    Graph, NodeConfig, WorkflowRun, ExecutionLog, LogLevel
)
from nexus_api.pulse_engine.tool_hub import ToolRegistry
from nexus_api.pulse_engine.memory_core import StateManager

class GraphExecutor:
    """
    Executes workflow graphs with state management and control flow.
    """
    
    def __init__(self, tool_registry: ToolRegistry, state_manager: StateManager):
        self.tool_registry = tool_registry
        self.state_manager = state_manager
    
    def register_graph(self, graph: Graph) -> str:
        """Register a new graph and return its ID."""
        graph_id = f"g-{uuid.uuid4().hex[:12]}"
        self.state_manager.save_graph(graph_id, graph)
        return graph_id
    
    async def execute(
        self, 
        graph_id: str, 
        initial_state: Dict[str, Any]
    ) -> WorkflowRun:
        """
        Execute a workflow graph with the given initial state.
        """
        graph = self.state_manager.get_graph(graph_id)
        if not graph:
            raise ValueError(f"Graph '{graph_id}' not found")
        
        run_id = f"r-{uuid.uuid4().hex[:12]}"
        state = initial_state.copy()
        logs = []
        
        run = WorkflowRun(
            run_id=run_id,
            graph_id=graph_id,
            state=state,
            status="running",
            logs=logs,
            started_at=datetime.utcnow()
        )
        
        self.state_manager.save_run(run_id, run)
        
        try:
            current_node = graph.start_node
            max_steps = 100
            step = 0
            
            while current_node and current_node != "end" and step < max_steps:
                step += 1
                
                # Log step
                self._log(run, LogLevel.INFO, 
                         f"Step {step}: Executing '{current_node}'")
                
                # Execute node
                node_config = graph.nodes.get(current_node)
                if not node_config:
                    raise ValueError(f"Node '{current_node}' not found")
                
                state = await self._execute_node(node_config, state, run)
                run.state = state
                
                # Determine next node
                current_node = self._get_next_node(
                    current_node, 
                    graph.edges, 
                    state
                )
                
                # Log transition
                if current_node and current_node != "end":
                    self._log(run, LogLevel.INFO, 
                             f"→ Transitioning to '{current_node}'")
            
            if step >= max_steps:
                raise RuntimeError("Maximum steps reached - possible infinite loop")
            
            run.status = "completed"
            run.completed_at = datetime.utcnow()
            self._log(run, LogLevel.INFO, 
                     f"✓ Workflow completed in {step} steps")
            
        except Exception as e:
            run.status = "failed"
            run.completed_at = datetime.utcnow()
            run.error = str(e)
            self._log(run, LogLevel.ERROR, f"✗ Workflow failed: {str(e)}")
        
        self.state_manager.save_run(run_id, run)
        return run
    
    async def _execute_node(
        self, 
        node_config: NodeConfig, 
        state: Dict[str, Any],
        run: WorkflowRun
    ) -> Dict[str, Any]:
        """Execute a single node."""
        if node_config.type == "function":
            func_name = node_config.function
            if not func_name:
                raise ValueError("Function name not specified")
            
            tool = self.tool_registry.get_tool(func_name)
            if not tool:
                available = self.tool_registry.list_tools()
                raise ValueError(
                    f"Tool '{func_name}' not found. "
                    f"Available: {available}"
                )
            
            # Execute tool
            result = await tool(state)
            
            # Merge result into state
            return {**state, **result}
        
        raise ValueError(f"Unknown node type: {node_config.type}")
    
    def _get_next_node(
        self, 
        current_node: str, 
        edges: Dict[str, Any], 
        state: Dict[str, Any]
    ) -> Optional[str]:
        """Determine next node based on edges and state."""
        edge = edges.get(current_node)
        
        if not edge:
            return "end"
        
        # Simple edge
        if isinstance(edge, str):
            return edge
        
        # Conditional edge
        if isinstance(edge, dict):
            condition = edge.get("condition", "")
            if_true = edge.get("if_true", "end")
            if_false = edge.get("if_false", "end")
            
            try:
                # Safe eval with state context
                result = eval(condition, {"__builtins__": {}}, state)
                return if_true if result else if_false
            except Exception:
                return if_false
        
        return "end"
    
    def _log(self, run: WorkflowRun, level: LogLevel, message: str):
        """Add a log entry."""
        log = ExecutionLog(
            timestamp=datetime.utcnow(),
            level=level,
            message=message
        )
        run.logs.append(log)

# Global executor instance (will be initialized in main.py)
executor = None