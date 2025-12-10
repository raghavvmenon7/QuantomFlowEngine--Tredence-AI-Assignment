"""
Code Prism Agent - Code Review Workflow Implementation.
"""
from typing import Dict, Any
import re
from nexus_api.pulse_engine.tool_hub import ToolRegistry

def function_extractor(state: Dict[str, Any]) -> Dict[str, Any]:
    """Extract functions from source code."""
    code = state.get("code", "")
    
    # Find function definitions
    func_pattern = r'def\s+(\w+)\s*\([^)]*\):'
    functions = re.findall(func_pattern, code)
    
    function_details = []
    for func_name in functions:
        func_start = code.find(f"def {func_name}")
        if func_start != -1:
            remaining = code[func_start:]
            lines = remaining.split('\n')
            
            # Count function lines
            func_lines = [lines[0]]
            for i in range(1, len(lines)):
                if lines[i] and not lines[i].startswith((' ', '\t')):
                    break
                func_lines.append(lines[i])
            
            function_details.append({
                "name": func_name,
                "lines": len(func_lines),
                "body": '\n'.join(func_lines)
            })
    
    return {
        "functions": function_details,
        "function_count": len(functions),
        "extraction_complete": True
    }

def complexity_analyzer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze code complexity and quality."""
    functions = state.get("functions", [])
    code = state.get("code", "")
    
    score = 50  # Base score
    issues = []
    
    # Analyze function count
    func_count = len(functions)
    if func_count == 0:
        score -= 20
        issues.append("No functions detected")
    elif func_count > 5:
        score -= 5
        issues.append(f"Too many functions ({func_count})")
    elif 2 <= func_count <= 5:
        score += 20
    
    # Analyze individual functions
    for func in functions:
        lines = func.get("lines", 0)
        if lines > 20:
            score -= 10
            issues.append(f"Function '{func['name']}' exceeds 20 lines")
        elif lines < 10:
            score += 10
    
    # Check code length
    if len(code) > 500:
        score -= 10
        issues.append("Code is excessively long")
    
    # Clamp score
    score = max(0, min(100, score))
    
    return {
        "quality_score": score,
        "issues": issues,
        "complexity_check_complete": True
    }

def improvement_suggester(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate code improvement suggestions."""
    issues = state.get("issues", [])
    functions = state.get("functions", [])
    quality_score = state.get("quality_score", 0)
    
    suggestions = []
    
    # Issue-based suggestions
    if "No functions detected" in str(issues):
        suggestions.append("Refactor code into modular functions")
    
    for issue in issues:
        if "exceeds" in str(issue).lower():
            suggestions.append("Break down large functions into smaller units")
        if "Too many functions" in str(issue):
            suggestions.append("Consider class-based organization")
    
    # Function-specific suggestions
    for func in functions:
        if "return" not in func.get("body", "").lower():
            suggestions.append(
                f"Add explicit return statement to '{func['name']}'"
            )
    
    # General improvements
    if quality_score < 70:
        suggestions.extend([
            "Add comprehensive docstrings",
            "Implement type hints for parameters",
            "Review variable naming conventions"
        ])
    
    # Simulate improvement
    iteration = state.get("iteration", 0) + 1
    improved_score = min(quality_score + 15, 100)
    
    return {
        "suggestions": suggestions,
        "iteration": iteration,
        "quality_score": improved_score,
        "suggestion_complete": True
    }

def quality_checkpoint(state: Dict[str, Any]) -> Dict[str, Any]:
    """Decide whether to continue or stop the loop."""
    quality_score = state.get("quality_score", 0)
    threshold = state.get("threshold", 70)
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 3)
    
    # Stop conditions
    stop = (
        quality_score >= threshold or 
        iteration >= max_iterations
    )
    
    return {
        "stop": stop,
        "checkpoint_passed": stop
    }

def register_prism_tools(registry: ToolRegistry) -> None:
    """Register all Code Prism tools."""
    registry.register("function_extractor", function_extractor)
    registry.register("complexity_analyzer", complexity_analyzer)
    registry.register("improvement_suggester", improvement_suggester)
    registry.register("quality_checkpoint", quality_checkpoint)