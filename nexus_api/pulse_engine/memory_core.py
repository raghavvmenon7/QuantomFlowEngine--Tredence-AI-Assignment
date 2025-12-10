"""
Memory Core - In-memory storage for graphs and execution runs.
"""
from typing import Dict, Any, Optional

class StateManager:
    """Manages in-memory storage of graphs and workflow runs."""
    
    def __init__(self):
        self.graphs: Dict[str, Any] = {}
        self.runs: Dict[str, Any] = {}
    
    def save_graph(self, graph_id: str, graph_data: Any) -> None:
        """Store a graph definition."""
        self.graphs[graph_id] = graph_data
    
    def get_graph(self, graph_id: str) -> Optional[Any]:
        """Retrieve a graph definition."""
        return self.graphs.get(graph_id)
    
    def save_run(self, run_id: str, run_data: Any) -> None:
        """Store a workflow run."""
        self.runs[run_id] = run_data
    
    def get_run(self, run_id: str) -> Optional[Any]:
        """Retrieve a workflow run."""
        return self.runs.get(run_id)
    
    def list_graphs(self) -> list:
        """List all graph IDs."""
        return list(self.graphs.keys())
    
    def list_runs(self) -> list:
        """List all run IDs."""
        return list(self.runs.keys())

# Global state manager instance
state_manager = StateManager()