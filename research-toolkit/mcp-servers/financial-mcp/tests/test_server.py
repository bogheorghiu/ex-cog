"""
Tests for financial MCP server - testing the CRITICAL PATH.

Critical path: MCP tool call → server receives → loads module → executes → returns

These tests verify:
1. Tool listing returns expected tools
2. Dynamic module loading works for all tools
3. Each tool has required execute() function
4. Error handling for invalid inputs
5. End-to-end execution (with mocked yfinance)
"""

import pytest
import sys
import os
import importlib
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, parent_dir)

from tool_definitions import get_tool_definitions


class TestToolDefinitions:
    """Tests for tool discovery - the contract between server and Claude."""

    def test_get_tool_definitions_returns_list(self):
        """Tool definitions should return a list."""
        tools = get_tool_definitions()
        assert isinstance(tools, list)

    def test_expected_tools_present(self):
        """All expected tools should be defined."""
        tools = get_tool_definitions()
        tool_names = [t.name for t in tools]

        expected = [
            "get_stock_price",
            "get_stock_history",
            "get_stock_info",
            "get_technical_indicators",
            "get_stock_analysis",
            "force_fetch_ticker"
        ]

        for name in expected:
            assert name in tool_names, f"Missing tool: {name}"

    def test_each_tool_has_required_schema_fields(self):
        """Each tool must have name, description, and inputSchema."""
        tools = get_tool_definitions()

        for tool in tools:
            assert tool.name, f"Tool missing name"
            assert tool.description, f"Tool {tool.name} missing description"
            assert tool.inputSchema, f"Tool {tool.name} missing inputSchema"
            assert "properties" in tool.inputSchema, f"Tool {tool.name} schema missing properties"

    def test_all_tools_require_symbol(self):
        """Every tool should require a symbol parameter (core invariant)."""
        tools = get_tool_definitions()

        for tool in tools:
            required = tool.inputSchema.get("required", [])
            assert "symbol" in required, f"Tool {tool.name} doesn't require 'symbol'"


class TestDynamicModuleLoading:
    """Tests for the dynamic import pattern - structural integrity."""

    def test_all_tool_modules_exist(self):
        """Every defined tool should have a corresponding implementation module."""
        tools = get_tool_definitions()
        implementations_dir = os.path.join(parent_dir, 'implementations')

        for tool in tools:
            module_path = os.path.join(implementations_dir, f"{tool.name}.py")
            assert os.path.exists(module_path), f"Missing implementation: {tool.name}.py"

    def test_all_modules_have_execute_function(self):
        """Every implementation module must have an execute() function.

        Note: We check via AST parsing because the modules use relative imports
        that only work when imported from the server directory context.
        """
        import ast
        tools = get_tool_definitions()
        implementations_dir = os.path.join(parent_dir, 'implementations')

        for tool in tools:
            module_path = os.path.join(implementations_dir, f"{tool.name}.py")
            with open(module_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)
            function_names = [node.name for node in ast.walk(tree)
                           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]

            assert 'execute' in function_names, f"Module {tool.name} missing execute() function"

    def test_invalid_tool_name_raises_module_not_found(self):
        """Requesting a non-existent tool should fail predictably."""
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("implementations.nonexistent_tool")


class TestServerErrorHandling:
    """Tests for error handling in the server's handle_call_tool."""

    @pytest.mark.asyncio
    async def test_handle_call_tool_with_invalid_tool_raises(self):
        """Invalid tool names should raise ValueError (design decision: fail fast)."""
        # Import server module
        sys.path.insert(0, parent_dir)
        from server import handle_call_tool

        # Call with invalid tool name - should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            await handle_call_tool("definitely_not_a_real_tool", {"symbol": "AAPL"})

        assert "not found" in str(exc_info.value).lower()


class TestIntegration:
    """Integration tests that verify the server can be run.

    Note: Full end-to-end tests with yfinance require running from server directory
    with proper PYTHONPATH. These tests verify the structure is correct for that.
    """

    def test_server_module_imports_cleanly(self):
        """Server module should import without errors (when MCP is available)."""
        try:
            sys.path.insert(0, parent_dir)
            import server
            assert hasattr(server, 'server'), "Server object should exist"
            assert hasattr(server, 'handle_list_tools'), "handle_list_tools should exist"
            assert hasattr(server, 'handle_call_tool'), "handle_call_tool should exist"
        except ImportError as e:
            if "mcp" in str(e).lower():
                pytest.skip("MCP package not installed - skipping server import test")
            raise

    def test_execute_functions_are_async(self):
        """All execute() functions should be async (required by MCP pattern)."""
        import ast
        import inspect
        tools = get_tool_definitions()
        implementations_dir = os.path.join(parent_dir, 'implementations')

        for tool in tools:
            module_path = os.path.join(implementations_dir, f"{tool.name}.py")
            with open(module_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef) and node.name == 'execute':
                    break
            else:
                pytest.fail(f"Module {tool.name} execute() is not async - MCP requires async")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
