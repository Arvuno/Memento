# 05_PR_CANDIDATES.md - Memento PR Candidates

## Analysis Summary

### Repository Status
- **Upstream**: Memento-Teams/Memento (MIT, 2.4k stars, 286 forks, 14 open issues)
- **Fork**: okwn/Memento (fresh fork, synced with upstream)
- **Open PRs in upstream**: 1 (LiteLLM gateway feature)

### Quality Issues Identified

#### 1. No Test Coverage
- Zero test files found in repository
- No pytest/unittest configuration
- No CI/CD workflows for validation

#### 2. Code Quality Observations
- Bare `except Exception:` patterns in multiple files (subprocess_interpreter.py, ipython_interpreter.py, excel_tool.py, documents_tool.py, code_agent.py, craw_page.py, search_tool.py)
- No logging calls found (despite colorlog/loguru being imported)
- Some error paths silently fail without user feedback

#### 3. Documentation Gaps
- pyproject.toml has placeholder description: "Add your description here"
- No contributing.md or development guidelines
- README mentions .env configuration but no .env file committed

### Potential PR Candidates

#### High Priority

1. **Add Test Infrastructure**
   - Add `tests/` directory with pytest configuration
   - Create basic tests for core modules (agent.py, memory modules)
   - Add GitHub Actions workflow for CI
   - Files: `pytest.ini` or `pyproject.toml` test config, `.github/workflows/test.yml`

2. **Add Proper Error Logging**
   - Replace bare `except Exception:` with proper logging
   - Add error context to exception handlers
   - Use `logger.error()` / `logger.warning()` consistently
   - Files: multiple server/*.py files

3. **Fix pyproject.toml Description**
   - Change placeholder "Add your description here" to meaningful description
   - File: `pyproject.toml`

#### Medium Priority

4. **Add LiteLLM Gateway Support** (Addresses Issue #39)
   - Open PR already exists for this feature
   - Would enable using any LLM provider supported by LiteLLM
   - Files: `client/agent.py`, possibly new backend class

5. **Improve Gemini API Compatibility** (Addresses Issue #24)
   - Issue: "Gemini model reference in OpenAI client doesn't seem to work"
   - Likely needs proper API base URL configuration for Gemini
   - Files: `client/agent.py`, backend configuration

6. **Add Contributing Guidelines**
   - Create `CONTRIBUTING.md` with development setup instructions
   - Document how to add new MCP tools
   - Explain the planner-executor architecture
   - File: `CONTRIBUTING.md`

#### Lower Priority

7. **Memory Scalability Improvements** (Addresses Issue #25)
   - "Scalability Concerns with Memory Retrieval"
   - Could involve caching, indexing, or batched retrieval
   - Files: `memory/parametric_memory.py`, `memory/np_memory.py`

8. **Add User Memory UI** (Addresses Issue #22)
   - "how to manually control/edit the memories? feature request idea: adding a UI"
   - Could be CLI-based or web-based memory editor
   - Files: new UI component + memory interface

9. **Parametric CBR Training Code Documentation** (Addresses Issue #30)
   - "Parametric Case-Based Reasoning Training Code"
   - Ensure training pipeline is well-documented
   - Files: `memory/train_memory_retriever.py`

### PR Selection for Implementation

**Selected: "Add Test Infrastructure"**
- Clear scope and measurable outcomes
- No dependency on external API access
- Can be verified with syntax checks alone
- Would improve code quality confidence for future PRs

**Secondary: "Add Proper Error Logging"**
- Complements test infrastructure
- Improves debuggability
- Can be done incrementally by file

### Files to Modify/Create

```
.github/
└── workflows/
    └── test.yml           # CI workflow for running tests
tests/
├── __init__.py
├── test_agent.py          # Tests for client/agent.py
├── test_memory.py         # Tests for memory modules
└── conftest.py            # Pytest fixtures
pyproject.toml             # Fix description
CONTRIBUTING.md            # Add contribution guidelines
```

### Risk Assessment
- **Test infrastructure**: Low risk - additive changes only
- **Error logging**: Low risk - adds diagnostics, doesn't change behavior
- **LiteLLM integration**: Medium risk - requires API testing
- **Gemini fix**: Medium risk - requires API key and testing