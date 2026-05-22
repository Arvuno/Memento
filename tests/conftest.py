"""Pytest fixtures and shared test utilities."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

import pytest

# Add client directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "client"))
sys.path.insert(0, str(Path(__file__).parent.parent / "memory"))


@pytest.fixture
def mock_env():
    """Set up mock environment variables."""
    old_env = os.environ.copy()
    os.environ.update({
        "OPENAI_API_KEY": "test-key-for-testing",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "USE_AZURE_OPENAI": "False",
    })
    yield
    os.environ.clear()
    os.environ.update(old_env)


@pytest.fixture
def sample_query():
    """Sample query for testing."""
    return "What is the capital of France?"


@pytest.fixture
def sample_plan_json():
    """Sample plan JSON from planner."""
    return '{"plan": [{"id": 1, "description": "Search for capital of France"}]}'


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI chat response."""
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message.content = "Paris"
    mock_resp.choices[0].message.tool_calls = None
    return mock_resp


@pytest.fixture
def mock_mcp_session():
    """Mock MCP client session."""
    session = AsyncMock()
    session.list_tools = AsyncMock(return_value=MagicMock(tools=[]))
    session.call_tool = AsyncMock(return_value=MagicMock(content="tool result"))
    return session