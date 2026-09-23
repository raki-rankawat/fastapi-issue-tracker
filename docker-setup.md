# Run with Docker

## Prerequisites

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and make sure it is running.

## Project files

```
fastapi-issue-tracker/
├── app/
│   └── routes/
│       └── issues.py
├── main.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── .dockerignore
```

**requirements.txt**

```
fastapi[standard]==0.141.1
```

**Dockerfile** tells Docker how to build the image. `compose.yaml` uses it through `build: .`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY app/ ./app/
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

The Dockerfile has to copy every file and folder the app imports. If you add a new top-level folder, add a `COPY` line for it too. Otherwise the container fails on startup with `ModuleNotFoundError: No module named '...'`.

**compose.yaml** builds the image, starts the container, and keeps it in sync with your code:

```yaml
services:
  api:
    build: .
    image: issue-tracker
    container_name: issue-tracker
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    develop:
      watch:
        - action: sync
          path: .
          target: /app
          ignore:
            - .venv/
            - __pycache__/
        - action: rebuild
          path: requirements.txt
```

**.dockerignore** keeps your local virtual environment and cache files out of the image:

```
.venv/
__pycache__/
*.pyc
```

## Steps

1. Open a terminal in the project folder.

2. Build and start the app:

   ```
   docker compose up --build --watch
   ```

3. Open http://localhost:8000/health in your browser. You should see:

   ```json
   {"status": "ok"}
   ```

   The interactive API docs are at http://localhost:8000/docs.

4. Leave it running while you work. Save a file, refresh the page, and your change is there about a second later.

5. Press `Ctrl+C` to stop the app. To also remove the stopped container, run:

   ```
   docker compose down
   ```

## How live reload works

- Every time you save a file, Docker copies it into the running container (`action: sync`).
- Uvicorn's `--reload` sees the new file inside the container and restarts the server.
- If you change `requirements.txt`, Docker rebuilds the image for you (`action: rebuild`).
- If you change the `Dockerfile` or `compose.yaml`, stop with `Ctrl+C` and run `docker compose up --build --watch` again.

Live reload only works while `docker compose up --watch` is running. If you start the app some other way, your edits won't show up.

## Deploy: Docker Hub → Render (free)

This pushes your image to Docker Hub, then runs it on Render's free tier.

### 1. Push the image to Docker Hub

1. Create a free account at [hub.docker.com](https://hub.docker.com/) and note your username.

2. Log in from your terminal (opens a browser, or asks for your password / access token):

   ```
   docker login
   ```

3. Build the image, tagged as `<your-username>/issue-tracker`:

   ```
   docker build -t <your-username>/issue-tracker:latest .
   ```

4. Push it:

   ```
   docker push <your-username>/issue-tracker:latest
   ```

   Your image is now public at `docker.io/<your-username>/issue-tracker`.

### 2. Run it on Render

1. Create a free account at [render.com](https://render.com/).

2. In the dashboard: **New → Web Service → Deploy an existing image from a registry**.

3. **Image URL:** `docker.io/<your-username>/issue-tracker:latest`

4. Pick the **Free** instance type, give it a name, and click **Create Web Service**.

5. Render builds and starts the container, then gives you a public URL like
   `https://issue-tracker-xxxx.onrender.com`. Check `/health` and `/docs` on it.

You don't set a port on Render — it assigns one through the `$PORT` environment
variable, and the Dockerfile's `CMD` already binds to it (falling back to 8000
locally).

### Redeploying after a change

```
docker build -t <your-username>/issue-tracker:latest .
docker push <your-username>/issue-tracker:latest
```

Then in Render click **Manual Deploy → Deploy latest reference** (or enable
auto-deploy on the service).

### Things to know about the free tier

- **The service sleeps after ~15 minutes of no traffic.** The next request wakes
  it and takes ~30–60 seconds to respond. This is normal for the free plan.
- **Storage is ephemeral.** `data/issue.json` lives inside the container, so every
  redeploy or restart wipes all issues. That's fine for a demo; for real
  persistence you'd add a Render Disk (paid) or switch storage to a database.

## Cleaning up old images

Each rebuild creates a new image and moves the `issue-tracker` tag to it. The old one loses its tag and shows up in `docker images` as `<none>`. It isn't used, but it takes up disk space. Remove these leftover images with:

```
docker image prune -f
```

## Notes

- `--host 0.0.0.0` lets your browser reach the app inside the container.
- `"8000:8000"` connects port 8000 on your computer to port 8000 in the container.
- If the port is already in use, or you see `The container name "/issue-tracker" is already in use`, an old container is still around. Remove it with `docker compose down` (or `docker rm -f issue-tracker`) and run again.
- Run Docker commands in PowerShell. Git Bash can silently rewrite paths that start with `/`.
