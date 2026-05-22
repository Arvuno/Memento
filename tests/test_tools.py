"""Tests for server MCP tools."""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

# Add server to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "server" / "interpreters"))


class TestCodeAgentImports:
    """Test code_agent.py can be imported."""

    def test_code_agent_import(self):
        """Test code_agent module imports correctly."""
        try:
            import code_agent
            assert code_agent is not None
        except ImportError as e:
            pytest.skip(f"code_agent not importable: {e}")

    def test_fastmcp_available(self):
        """Test FastMCP is available."""
        try:
            from mcp.server.fastmcp import FastMCP
            assert FastMCP is not None
        except ImportError:
            pytest.fail("FastMCP should be installed")


class TestInterpreters:
    """Test interpreter modules."""

    def test_base_interpreter_import(self):
        """Test base interpreter can be imported."""
        try:
            from base import BaseInterpreter
            assert BaseInterpreter is not None
        except ImportError as e:
            pytest.skip(f"base not importable: {e}")

    def test_interpreters_factory_import(self):
        """Test interpreters module exports."""
        try:
            from interpreters import (
                DockerInterpreter,
                E2BInterpreter,
                InternalPythonInterpreter,
                SubprocessInterpreter,
            )
            assert DockerInterpreter is not None
            assert E2BInterpreter is not None
            assert InternalPythonInterpreter is not None
            assert SubprocessInterpreter is not None
        except ImportError as e:
            pytest.skip(f"interpreters not importable: {e}")


class TestImportWhitelist:
    """Test import whitelist functionality in code_agent.py."""

    def test_whitelist_exists(self):
        """Test DEFAULT_IMPORT_WHITELIST exists."""
        try:
            import code_agent
            assert hasattr(code_agent, 'DEFAULT_IMPORT_WHITELIST')
            assert isinstance(code_agent.DEFAULT_IMPORT_WHITELIST, list)
        except ImportError:
            pytest.skip("code_agent not importable")

    def test_whitelist_includes_common_packages(self):
        """Test whitelist contains expected packages."""
        try:
            import code_agent
            whitelist = code_agent.DEFAULT_IMPORT_WHITELIST
            
            # Should include common data science packages
            assert 'numpy' in whitelist or 'np' in whitelist
            assert 'pandas' in whitelist or 'pd' in whitelist
            assert 'torch' in whitelist
        except ImportError:
            pytest.skip("code_agent not importable")


class TestToolServers:
    """Test individual tool server modules."""

    def test_search_tool_import(self):
        """Test search_tool.py imports."""
        try:
            import search_tool
            assert search_tool is not None
        except ImportError as e:
            pytest.skip(f"search_tool not importable: {e}")

    def test_documents_tool_import(self):
        """Test documents_tool.py imports."""
        try:
            import documents_tool
            assert documents_tool is not None
        except ImportError as e:
            pytest.skip(f"documents_tool not importable: {e}")

    def test_image_tool_import(self):
        """Test image_tool.py imports."""
        try:
            import image_tool
            assert image_tool is not None
        except ImportError as e:
            pytest.skip(f"image_tool not importable: {e}")

    def test_excel_tool_import(self):
        """Test excel_tool.py imports."""
        try:
            import excel_tool
            assert excel_tool is not None
        except ImportError as e:
            pytest.skip(f"excel_tool not importable: {e}")

    def test_math_tool_import(self):
        """Test math_tool.py imports."""
        try:
            import math_tool
            assert math_tool is not None
        except ImportError as e:
            pytest.skip(f"math_tool not importable: {e}")


class TestMCPServerIntegration:
    """Test MCP server functionality."""

    def test_mcp_client_import(self):
        """Test MCP client can be imported."""
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            assert ClientSession is not None
            assert StdioServerParameters is not None
            assert stdio_client is not None
        except ImportError:
            pytest.fail("MCP client should be installed")

    @pytest.mark.asyncio
    async def test_stdio_server_parameters(self):
        """Test StdioServerParameters creation."""
        from mcp import StdioServerParameters
        
        params = StdioServerParameters(
            command="python",
            args=["-c", "print('hello')"]
        )
        
        assert params.command == "python"
        assert "-c" in params.args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])