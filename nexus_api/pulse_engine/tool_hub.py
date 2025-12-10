"""
Tool Hub - Registry for managing executable functions.
"""
from typing import Dict, Callable, Optional
import asyncio
from functools import wraps

class ToolRegistry:
    """
    Global registry for workflow tools.
    Handles both sync and async functions automatically.
    """
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable) -> None:
        """Register a tool function."""
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered")
        self._tools[name] = func
        print(f"✓ Registered tool: {name}")
    
    def decorator(self, name: str):
        """Decorator for tool registration."""
        def wrapper(func: Callable):
            self.register(name, func)
            return func
        return wrapper
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get a tool and wrap it to be async if needed.
        """
        tool = self._tools.get(name)
        if not tool:
            return None
        
        # Wrap sync functions to be async
        if not asyncio.iscoroutinefunction(tool):
            @wraps(tool)
            async def async_wrapper(*args, **kwargs):
                return tool(*args, **kwargs)
            return async_wrapper
        
        return tool
    
    def list_tools(self) -> list:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def count(self) -> int:
        """Count registered tools."""
        return len(self._tools)

# Global tool registry instance
tool_hub = ToolRegistry()