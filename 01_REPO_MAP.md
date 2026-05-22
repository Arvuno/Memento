# 01_REPO_MAP.md - Memento Repository Map

## File Structure

### Root Level
| File | Purpose |
|------|---------|
| `README.md` | Project documentation, quickstart, architecture |
| `LICENSE` | MIT License |
| `pyproject.toml` | Python project metadata (uv-based) |
| `requirements.txt` | Pip dependencies |
| `uv.lock` | Locked dependencies (uv) |
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore patterns |
| `.python-version` | Python version spec (3.11+) |

### Client (`client/`)
| File | Lines | Purpose |
|------|-------|---------|
| `agent.py` | 301 | Main hierarchical client with planner-executor loop, MCP tool connections |
| `no_parametric_cbr.py` | - | Non-parametric case-based reasoning implementation |
| `parametric_memory_cbr.py` | - | Parametric CBR with neural retriever |
| `agent_local_server.py` | - | Local vLLM server support for self-hosted LLMs |
| `parametric_memory.py` | - | Parametric memory module |

### Server (`server/`) - MCP Tool Servers
| File | Purpose |
|------|---------|
| `code_agent.py` | FastMCP server for code execution with workspace management, import whitelist |
| `search_tool.py` | Web search via SearxNG |
| `serp_search.py` | SERP-based search using SerpAPI |
| `jina_fetch_tool.py` | Jina AI content fetching |
| `craw_page.py` | Web page crawling |
| `ai_crawl.py` | Query-aware compression crawler for reducing token costs |
| `documents_tool.py` | Multi-format document processing (PDF, Office, images, audio, video) |
| `image_tool.py` | Image analysis and captioning |
| `video_tool.py` | Video processing and narration |
| `excel_tool.py` | Spreadsheet processing |
| `math_tool.py` | Mathematical computations |

### Interpreters (`server/interpreters/`)
| File | Purpose |
|------|---------|
| `base.py` | Base interpreter interface |
| `interpreters.py` | Interpreter factory/exports |
| `docker_interpreter.py` | Docker-based sandboxed execution |
| `e2b_interpreter.py` | E2B cloud sandbox |
| `internal_python_interpreter.py` | In-process Python execution |
| `ipython_interpreter.py` | Jupyter kernel-based execution |
| `subprocess_interpreter.py` | Subprocess-based execution |
| `interpreter_error.py` | Error definitions |
| `logger.py` | Logging utilities |

### Memory (`memory/`)
| File | Purpose |
|------|---------|
| `parametric_memory.py` | Case retriever for inference |
| `train_memory_retriever.py` | Retriever training script |
| `np_memory.py` | Non-parametric memory utilities |
| `memory.jsonl` | Memory pool (cases with outcomes) |
| `training_data.jsonl` | Training data for retriever |
| `dummy_memo.jsonl` | Sample/dummy cases |

### Data (`data/`)
| File | Purpose |
|------|---------|
| `deepresearcher.jsonl` | DeepResearcher benchmark data |

### SearxNG Docker (`searxng-docker/`)
| File | Purpose |
|------|---------|
| `docker-compose.yaml` | Docker Compose for SearxNG |
| `searxng/settings.yml` | SearxNG configuration |
| `Caddyfile` | Caddy reverse proxy config |
| `README.md` | Docker setup instructions |

## Dependencies

### Core Dependencies (pyproject.toml + requirements.txt)
- `openai==1.75.0` - LLM API client
- `fastmcp==2.7.0` - MCP server framework
- `tenacity==9.1.2` - Retry logic
- `tiktoken==0.9.0` - Tokenizer
- `pandas==2.2.3` - Data manipulation
- `torch>=2.0.0` - ML framework
- `transformers>=4.30.0` - NLP models
- `scikit-learn>=1.3.0` - ML utilities
- `crawl4ai>=0.7.4` - Web crawling
- `assemblyai==0.40.2` - Audio transcription
- `yt-dlp>=2025.8.27` - Video downloading
- `opencv-python==4.11.0.86` - Image processing

## Key Patterns

### MCP Tool Architecture
- Server scripts use `FastMCP` from `mcp.server.fastmcp`
- Tools exposed via `@mcp.tool()` decorator
- Client connects via `ClientSession` with `StdioServerParameters`
- Communication via stdio (JSON-RPC over stdin/stdout)

### Planner-Executor Pattern
- Planner (gpt-4.1): Decomposes tasks into JSON plan `{"plan": [{"id": INT, "description": STRING}]}`
- Executor (o3): Executes individual tasks using available MCP tools
- Max 3 cycles per query to prevent infinite loops

### Memory System
- Case bank stores `(s_T, a_T, r_T)` tuples
- Non-parametric: Simple retrieval by similarity
- Parametric: Neural retriever trained with `train_memory_retriever.py`

## Codebase Statistics
- Total Python files: ~50
- Largest files: code_agent.py (1205 lines), agent.py (301 lines)
- No test files detected
- No CI/CD workflows detected