# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

Early-stage FastAPI issue tracker. The only code so far is [main.py](main.py), which creates the `app` instance and a `GET /health` endpoint. Direct dependencies are pinned in [requirements.txt](requirements.txt). There is no test suite, no linter config, and no git repo yet.

## Environment

- Python 3.12 virtualenv at `.venv` (Windows layout: `.venv\Scripts\`).
- Installed via `fastapi[standard]`: FastAPI, Uvicorn, Pydantic v2, pydantic-settings, httpx, python-dotenv, email-validator. No database, ORM, or test framework is installed.

## Commands (PowerShell)

```powershell
.venv\Scripts\Activate.ps1          # activate venv
fastapi dev main.py                 # dev server with auto-reload at http://127.0.0.1:8000 (docs at /docs)
fastapi run main.py                 # production-style server
pip install <pkg>                   # add dependencies (then consider recording them in a requirements file)
```

If tests are added, `pip install pytest` and use FastAPI's `TestClient` (httpx is already installed); run a single test with `pytest path/to/test_file.py::test_name`.
