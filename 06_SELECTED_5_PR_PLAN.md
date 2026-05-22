# 06_SELECTED_5_PR_PLAN.md - Implementation Plan

## Selected Priority: Add Test Infrastructure

### Rationale
- Zero test coverage currently exists
- Tests are fundamental for code quality and regression prevention
- No API keys or external dependencies required to implement
- Provides foundation for validating future PRs

---

## Implementation Plan

### Phase 1: Project Configuration

#### 1.1 Add pytest configuration to pyproject.toml
```python
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
asyncio_mode = "auto"
addopts = "-v --tb=short"
```

#### 1.2 Create .github/workflows/test.yml
- Trigger on push and pull_request
- Python 3.11+ matrix
- Run: pip install, pytest
- Cache dependencies

### Phase 2: Test Files

#### 2.1 tests/__init__.py
- Empty, marks tests as package

#### 2.2 tests/conftest.py
- Shared fixtures
- Mock environment variables
- Sample data fixtures

#### 2.3 tests/test_agent.py
- Test message trimming logic
- Test JSON parsing helpers
- Test token counting
- Mock LLM responses for unit testing

#### 2.4 tests/test_memory.py
- Test case retrieval logic (non-parametric)
- Test memory format validation
- Test training data parsing

#### 2.5 tests/test_tools.py
- Test code_agent.py tool schemas
- Test import whitelist validation
- Mock MCP tool responses

### Phase 3: Quality Improvements

#### 3.1 Fix pyproject.toml description
Change: `description = "Add your description here"`
To: `description = "Memento: Fine-tuning LLM Agents without Fine-tuning LLMs - A memory-based continual learning framework for LLM agents"`

#### 3.2 Add basic logging to agent.py
- Add logger.info() for connection events
- Add logger.warning() for fallback behaviors

---

## Files to Create

```
.github/
└── workflows/
    └── test.yml           # ~30 lines

tests/
├── __init__.py            # 0 lines
├── conftest.py            # ~40 lines
├── test_agent.py          # ~100 lines
├── test_memory.py         # ~80 lines
└── test_tools.py         # ~80 lines
```

## Files to Modify

```
pyproject.toml             # Add pytest config + fix description
client/agent.py            # Add logging calls
```

---

## Success Criteria

1. `pytest` runs successfully with 0 collected tests (no errors)
2. CI workflow passes on GitHub Actions
3. pyproject.toml has correct description
4. All new files pass syntax checks

---

## Secondary Improvements (If Time Permits)

### Add Error Logging
Replace bare `except Exception:` handlers with:
```python
except Exception as e:
    logger.error(f"Failed to process: {e}", exc_info=True)
```

Focus files (highest impact):
1. `server/code_agent.py` - most critical
2. `server/search_tool.py` - network errors common
3. `server/documents_tool.py` - file processing errors

### Add CONTRIBUTING.md
Basic guidelines:
- Development setup with uv
- How to run tests
- How to add new MCP tools
- Code style expectations

---

## Notes
- Tests use mocking to avoid needing actual API keys
- Token counting tests use tiktoken for validation
- Memory tests use sample JSONL data
- All tests should be fast (< 5s total runtime)