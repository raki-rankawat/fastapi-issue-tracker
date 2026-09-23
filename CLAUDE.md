# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

FastAPI issue tracker with a full CRUD API over JSON file storage. There is no test suite and no linter config yet. See [README.md](README.md) for the user-facing overview and [docker-setup.md](docker-setup.md) for the Docker workflow.

## Architecture

- [main.py](main.py) — creates the `app` instance, registers the timing middleware, adds permissive CORS (all origins), includes the issues router, and defines `GET /health`.
- [app/routes/issues.py](app/routes/issues.py) — `APIRouter` at prefix `/api/v1/issues` with list/get/create/update/delete endpoints (`GET /`, `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}`). `PUT` is a partial update (only non-`None` fields are applied).
- [app/schemas.py](app/schemas.py) — Pydantic v2 models (`IssueCreate`, `IssueUpdate`, `IssueOut`) and the `IssueStatus` (`open`/`in_progress`/`closed`) and `IssuePriority` (`low`/`medium`/`high`) enums. New issues are created with `status=open`.
- [app/storage.py](app/storage.py) — reads/writes the whole issue list as JSON to `data/issue.json`, created on first write. This is a load-modify-save file store with no locking, so it is not safe for concurrent writes.
- [app/middleware/timer.py](app/middleware/timer.py) — adds an `X-Process-Time` response header.

The Dockerfile copies `main.py` and `app/` explicitly; a new top-level module or folder the app imports needs its own `COPY` line, or the container fails at startup with `ModuleNotFoundError`.

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
