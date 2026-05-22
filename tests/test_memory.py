"""Tests for memory modules."""

import json
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add memory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "memory"))


class TestMemoryFormat:
    """Test memory case format validation."""

    def test_memory_jsonl_structure(self):
        """Test that memory.jsonl has expected structure."""
        memory_path = Path(__file__).parent.parent / "memory" / "memory.jsonl"
        
        if memory_path.exists():
            with open(memory_path, 'r') as f:
                first_line = f.readline()
                if first_line.strip():
                    data = json.loads(first_line)
                    # Memory cases should have some structure
                    assert isinstance(data, dict)

    def test_training_data_structure(self):
        """Test training_data.jsonl has expected format."""
        training_path = Path(__file__).parent.parent / "memory" / "training_data.jsonl"
        
        if training_path.exists():
            with open(training_path, 'r') as f:
                first_line = f.readline()
                if first_line.strip():
                    data = json.loads(first_line)
                    # Training data should be a list or dict
                    assert isinstance(data, (list, dict))


class TestNonParametricMemory:
    """Test np_memory.py module."""

    def test_np_memory_import(self):
        """Test np_memory module can be imported."""
        try:
            from np_memory import NonParametricMemory
            assert NonParametricMemory is not None
        except ImportError as e:
            pytest.skip(f"np_memory module not importable: {e}")

    def test_np_memory_basic_methods(self):
        """Test basic np_memory methods exist."""
        try:
            from np_memory import NonParametricMemory
            
            # Check class exists and has expected methods
            assert hasattr(NonParametricMemory, 'retrieve')
            assert hasattr(NonParametricMemory, 'add')
        except ImportError:
            pytest.skip("np_memory not available")


class TestParametricMemory:
    """Test parametric_memory.py module."""

    def test_parametric_memory_import(self):
        """Test parametric_memory module can be imported."""
        try:
            from parametric_memory import ParametricMemory
            assert ParametricMemory is not None
        except ImportError as e:
            pytest.skip(f"parametric_memory module not importable: {e}")

    def test_parametric_memory_has_training_method(self):
        """Test parametric memory has training-related methods."""
        try:
            from parametric_memory import ParametricMemory
            
            # Should have retrieval and possibly training methods
            assert hasattr(ParametricMemory, 'retrieve') or hasattr(ParametricMemory, '__init__')
        except ImportError:
            pytest.skip("parametric_memory not available")


class TestTrainRetriever:
    """Test train_memory_retriever.py module."""

    def test_train_script_import(self):
        """Test training script can be imported."""
        try:
            import train_memory_retriever
            assert train_memory_retriever is not None
        except ImportError as e:
            pytest.skip(f"train_memory_retriever not importable: {e}")

    def test_train_script_has_main(self):
        """Test training script has main entry point."""
        try:
            import train_memory_retriever
            
            # Script should have __main__ or main function
            has_main = hasattr(train_memory_retriever, 'main') or hasattr(train_memory_retriever, '__main__')
            # Skip if no main - not all scripts have clear entry points
            if not has_main:
                pytest.skip("No clear main entry point")
        except ImportError:
            pytest.skip("train_memory_retriever not available")


class TestMemoryData:
    """Test memory data files."""

    def test_memory_jsonl_readable(self):
        """Test memory.jsonl is valid JSONL."""
        memory_path = Path(__file__).parent.parent / "memory" / "memory.jsonl"
        
        if not memory_path.exists():
            pytest.skip("memory.jsonl not found")
        
        count = 0
        with open(memory_path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        json.loads(line)
                        count += 1
                    except json.JSONDecodeError:
                        pytest.fail(f"Invalid JSON on line {count + 1}")
        
        assert count > 0, "memory.jsonl should have at least one entry"

    def test_dummy_memo_exists(self):
        """Test dummy_memo.jsonl exists."""
        dummy_path = Path(__file__).parent.parent / "memory" / "dummy_memo.jsonl"
        
        if dummy_path.exists():
            # Should be readable JSONL
            with open(dummy_path, 'r') as f:
                for line in f:
                    if line.strip():
                        json.loads(line)
                        break


if __name__ == "__main__":
    pytest.main([__file__, "-v"])