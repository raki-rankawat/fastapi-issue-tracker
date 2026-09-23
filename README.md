# FastAPI Issue Tracker

A small REST API for tracking issues, built with [FastAPI](https://fastapi.tiangolo.com/). Issues are stored as JSON on disk — no database required.

## Features

- Full CRUD for issues (`create`, `list`, `get`, `update`, `delete`)
- Pydantic v2 validation with `status` and `priority` enums
- JSON file storage (`data/issue.json`)
- `X-Process-Time` response header via a custom timing middleware
- Permissive CORS (all origins) for easy local frontend development
- Interactive API docs at `/docs`

## Requirements

- Python 3.12
- Dependencies pinned in [requirements.txt](requirements.txt) (`fastapi[standard]`)

## Getting started

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # activate the virtualenv (Windows)
pip install -r requirements.txt
fastapi dev main.py                 # dev server with auto-reload
```

The API is served at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.

For a production-style server (no auto-reload):

```powershell
fastapi run main.py
```

To run in Docker instead, see [docker-setup.md](docker-setup.md).

## API

Base path: `/api/v1/issues`

| Method | Path                       | Description                | Success        |
| ------ | -------------------------- | -------------------------- | -------------- |
| GET    | `/health`                  | Health check               | `200`          |
| GET    | `/api/v1/issues/`          | List all issues            | `200`          |
| GET    | `/api/v1/issues/{id}`      | Get one issue by id        | `200` / `404`  |
| POST   | `/api/v1/issues/`          | Create an issue            | `201`          |
| PUT    | `/api/v1/issues/{id}`      | Update an issue (partial)  | `200` / `404`  |
| DELETE | `/api/v1/issues/{id}`      | Delete an issue            | `204` / `404`  |

### Issue model

| Field         | Type                                   | Notes                              |
| ------------- | -------------------------------------- | ---------------------------------- |
| `id`          | string (UUID)                          | Generated on create                |
| `title`       | string                                 | 3–100 chars                        |
| `description` | string                                 | 5–1000 chars                       |
| `priority`    | `low` \| `medium` \| `high`            | Defaults to `medium`               |
| `status`      | `open` \| `in_progress` \| `closed`    | Set to `open` on create            |

### Example

Create an issue:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/issues/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Login button broken", "description": "Clicking login does nothing", "priority": "high"}'
```

Response (`201 Created`):

```json
{
  "id": "…",
  "title": "Login button broken",
  "description": "Clicking login does nothing",
  "priority": "high",
  "status": "open"
}
```

## Project structure

```
fastapi-issue-tracker/
├── app/
│   ├── middleware/
│   │   └── timer.py       # adds X-Process-Time response header
│   ├── routes/
│   │   └── issues.py      # issue CRUD endpoints
│   ├── schemas.py         # Pydantic models and enums
│   └── storage.py         # JSON file read/write
├── main.py                # app instance, middleware, CORS, router, /health
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── docker-setup.md
```

Issues are persisted to `data/issue.json`, which is created on the first write.
