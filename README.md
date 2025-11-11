## Overview

AI Blog Generator uses:
- Frontend: React + TypeScript + Vite + Tailwind CSS
- Backend: FastAPI (Python) using the OpenAI Python SDK
- Configuration: .env with API_KEY and BASE_URL shared across services

## Prerequisites

- Node.js 18+
- Python 3.10+

## Configure environment

Copy .env and fill in your values:

```
API_KEY=your_api_key
BASE_URL=https://api.portkey.ai/v1
VITE_API_BASE_URL=http://localhost:8000
```

Notes:
- API_KEY and BASE_URL are read by the FastAPI backend.
- VITE_API_BASE_URL is used by the frontend to call the backend. During dev, the Vite dev server also proxies /api to http://localhost:8000.

## Install dependencies

Frontend:

```
npm install
```

Backend:

```
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r server\requirements.txt
```

## Run locally

Run backend (port 8000):

```powershell
uvicorn server.main:app --reload --port 8000
```

Health check:

```powershell
curl http://localhost:8000/api/health
```

In a separate terminal, run frontend (port 3000):

```powershell
npm run dev
```

Open http://localhost:3000

## Build for production

```powershell
npm run build
```

The static site is emitted to dist/. Serve it with any static server. Deploy your FastAPI backend separately.

## Docker

Using docker-compose:

```powershell
docker-compose up -d --build
```

This starts both backend (port 8000) and frontend (port 3000). Access at http://localhost:3000

Make sure your `.env` file has `API_KEY` and `BASE_URL` set.

To stop:

```powershell
docker-compose down
```

To rebuild after code changes:

```powershell
docker-compose up -d --build
```

Access the app at http://localhost:3000

## Troubleshooting
- Error message on UI: "Sorry, something went wrong while generating content": ensure backend is running and health check returns ok.
- Verify `.env` has correct API_KEY and BASE_URL and you restarted backend after changes.
- If responses contain malformed JSON, backend now attempts fallback parsing; check server logs for tags like `generate-tips:` or `from-topic:` in errors.
