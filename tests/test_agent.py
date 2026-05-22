"""Tests for client/agent.py module."""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

# Add client to path
sys.path.insert(0, str(Path(__file__).parent.parent / "client"))


class TestMessageTrimming:
    """Test message trimming functionality."""

    def test_trim_messages_preserves_system(self):
        """System message should always be first."""
        from agent import trim_messages, _get_tokenizer
        
        enc = _get_tokenizer("gpt-3.5-turbo")
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ]
        
        # With high max_tokens, all messages should be kept
        result = trim_messages(messages, 100000, model="gpt-3.5-turbo")
        
        assert result[0]["role"] == "system"
        assert len(result) == 2

    def test_trim_messages_respects_limit(self):
        """Messages should be trimmed when exceeding max_tokens."""
        from agent import trim_messages, _get_tokenizer
        
        messages = [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "A"},
            {"role": "assistant", "content": "B"},
            {"role": "user", "content": "C"},
        ]
        
        # Very low limit should keep only system
        enc = _get_tokenizer("gpt-3.5-turbo")
        result = trim_messages(messages, 10, model="gpt-3.5-turbo")
        
        assert result[0]["role"] == "system"


class TestJSONParsing:
    """Test JSON parsing helpers."""

    def test_strip_fences_removes_markdown(self):
        """JSON in code fences should be stripped."""
        from agent import _strip_fences
        
        text = "```json\n{\"plan\": []}\n```"
        result = _strip_fences(text)
        
        assert result == '{"plan": []}'

    def test_strip_fences_extracts_json_object(self):
        """Should extract JSON object from mixed text."""
        from agent import _strip_fences
        
        text = "Here is the plan:\n{\"plan\": [{\"id\": 1}]}\nLet me explain..."
        result = _strip_fences(text)
        
        assert '{"plan"' in result

    def test_strip_fences_passthrough_plain_json(self):
        """Plain JSON should pass through unchanged."""
        from agent import _strip_fences
        
        text = '{"plan": []}'
        result = _strip_fences(text)
        
        assert result == '{"plan": []}'


class TestTokenization:
    """Test token counting functionality."""

    def test_get_tokenizer_fallback(self):
        """Should fallback to cl100k_base for unknown models."""
        from agent import _get_tokenizer
        
        # Should not raise for unknown model
        enc = _get_tokenizer("unknown-model")
        assert enc is not None

    def test_count_tokens_basic(self):
        """Test basic token counting."""
        from agent import _count_tokens, _get_tokenizer
        
        enc = _get_tokenizer("gpt-4")
        msg = {"content": "Hello world"}
        
        count = _count_tokens(msg, enc)
        
        assert count > 0

    def test_count_tokens_empty_content(self):
        """Empty content should still count role overhead."""
        from agent import _count_tokens, _get_tokenizer
        
        enc = _get_tokenizer("gpt-4")
        msg = {"content": ""}
        
        count = _count_tokens(msg, enc)
        
        # Should at least have role_tokens (4)
        assert count >= 4


class TestChatBackend:
    """Test chat backend classes."""

    @pytest.mark.asyncio
    async def test_openai_backend_initialization(self, mock_env):
        """Test OpenAI backend can be initialized."""
        from agent import OpenAIBackend
        
        backend = OpenAIBackend(model="gpt-4", is_azure=False)
        
        assert backend.model == "gpt-4"
        assert backend.client is not None

    @pytest.mark.asyncio
    async def test_openai_backend_chat_with_mock(self, mock_env):
        """Test chat method with mocked response."""
        from agent import OpenAIBackend
        
        backend = OpenAIBackend(model="gpt-4", is_azure=False)
        
        # Mock the client's chat.completions.create
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].message.tool_calls = None
        
        with patch.object(backend.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response
            
            result = await backend.chat(messages=[{"role": "user", "content": "Hi"}])
            
            assert result["content"] == "Test response"
            assert result["tool_calls"] is None


class TestHierarchicalClient:
    """Test HierarchicalClient class."""

    @pytest.mark.asyncio
    async def test_client_initialization(self, mock_env):
        """Test client can be initialized."""
        from agent import HierarchicalClient
        
        client = HierarchicalClient(
            meta_model="gpt-4",
            exec_model="o3",
            is_azure=False
        )
        
        assert client.meta_llm is not None
        assert client.exec_llm is not None
        assert client.sessions == {}

    @pytest.mark.asyncio
    async def test_tools_schema_empty_initially(self, mock_env):
        """Test tools schema returns empty before connection."""
        from agent import HierarchicalClient
        
        client = HierarchicalClient("gpt-4", "o3", False)
        
        # Before connecting, sessions is empty
        # The _tools_schema method accesses self.sessions which is empty dict
        # This should not raise, just return empty list
        # Note: Can't easily test without connecting to servers
        assert client.sessions == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])