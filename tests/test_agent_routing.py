# tests/test_agent_routing.py
"""Test that the agent routing logic selects the expected tool."""
import pytest
from unittest.mock import MagicMock

# Assume routing function is in src/agent_router.py
from src.agent_router import route_query

def test_agent_routing_selects_correct_tool():
    # Mock tools dictionary
    mock_tool_a = MagicMock(name="ToolA")
    mock_tool_b = MagicMock(name="ToolB")
    tools = {"search": mock_tool_a, "calculate": mock_tool_b}

    # Query that should route to 'search'
    selected = route_query("Find disease prevalence in corn", tools)
    assert selected is mock_tool_a
