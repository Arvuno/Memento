# 00_STATE.md - Memento Repository Analysis

## Repository Information
- **Fork Source**: Memento-Teams/Memento (upstream)
- **Fork Owner**: okwn
- **Fork URL**: https://github.com/okwn/Memento
- **License**: MIT
- **Archived**: No
- **Default Branch**: main

## Upstream Statistics
- **Stars**: 2,432
- **Forks**: 286
- **Open Issues**: 14
- **Open PRs**: 1

## Project Overview
**Memento** is a memory-based, continual-learning framework that helps LLM agents improve from experience without updating model weights. It implements a Planner-Executor architecture with Case-Based Reasoning (CBR) for task decomposition and execution.

**Paper**: [arXiv:2508.16153](https://arxiv.org/abs/2508.16153)

## Key Technologies
- **Language**: Python 3.11+
- **LLM Integration**: OpenAI API (GPT-4.1 planner, o3 executor), Azure OpenAI
- **Protocol**: MCP (Model Context Protocol) for tool orchestration
- **Memory**: Case-based reasoning with parametric (neural retriever) and non-parametric variants

## Repository Structure
```
Memento/
├── client/           # Agent implementation
│   ├── agent.py              # Main hierarchical planner-executor
│   ├── no_parametric_cbr.py  # Non-parametric CBR
│   ├── parametric_memory.py  # Parametric memory with neural retriever
│   └── agent_local_server.py # Local vLLM support
├── server/           # MCP tool servers
│   ├── code_agent.py         # Code execution workspace
│   ├── search_tool.py        # Web search via SearxNG
│   ├── serp_search.py        # SERP-based search
│   ├── documents_tool.py     # Multi-format document processing
│   ├── image_tool.py         # Image analysis
│   ├── video_tool.py         # Video processing
│   ├── excel_tool.py         # Spreadsheet processing
│   ├── math_tool.py          # Mathematical computations
│   ├── craw_page.py          # Web page crawling
│   └── ai_crawler.py         # Query-aware compression crawler
├── interpreters/     # Code execution backends
│   ├── docker_interpreter.py
│   ├── e2b_interpreter.py
│   ├── internal_python_interpreter.py
│   ├── ipython_interpreter.py
│   └── subprocess_interpreter.py
├── memory/           # Memory components
│   ├── parametric_memory.py     # Case retriever
│   ├── train_memory_retriever.py # Training script
│   ├── np_memory.py              # Non-parametric utilities
│   ├── memory.jsonl             # Case bank
│   └── training_data.jsonl      # Training data
└── searxng-docker/  # SearxNG Docker setup
```

## Current Working Directory
- **Path**: `/root/oss-pr-campaign/repos/memento`
- **Branch**: main (synced with upstream/main)

## Upstream Remote
- **Name**: upstream
- **URL**: https://github.com/Memento-Teams/Memento.git

## Known Issues / Observations
1. No CI/CD workflows found (.github/workflows/ absent)
2. No test files detected in repository
3. Fork has 0 stars/forks (new fork)
4. 14 open issues in upstream, 1 open PR
5. Issues include: LiteLLM gateway request, memory scalability, Gemini API compatibility, parametric CBR training code requests

## Next Steps
- Create 01_REPO_MAP.md with detailed file mapping
- Analyze code quality and potential PR candidates
- Identify good first issues for contributions