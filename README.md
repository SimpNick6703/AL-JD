## AI Blog Generator
[![Netlify Status](https://api.netlify.com/api/v1/badges/09acfca0-923e-412a-b8fc-6886644836ab/deploy-status?branch=blog-generator)](https://al-jd-blog-gen.netlify.app/)

This project is deployed on Netflify (Frontend) and Azure Web Apps (Backend):
- Web UI: https://al-jd-blog-gen.netlify.app
- Swagger Docs: https://al-jd-blog-gen.azurewebsites.net/docs

AI Blog Generator uses:
- Frontend: React + TypeScript + Vite + Tailwind CSS
- Backend: FastAPI (Python) using the OpenAI Python SDK

## Prerequisites
- Node.js 18+
- Python 3.10+

## Configure environment
Copy .env and fill in your values:
```
API_KEY=your_api_key
BASE_URL=https://api.portkey.ai/v1
VITE_API_BASE_URL=http://localhost:8000 # Backend URL
```

> [!NOTE]
> - API_KEY and BASE_URL are read by the FastAPI backend.
> - VITE_API_BASE_URL is used by the frontend to call the backend. During dev, the Vite dev server also proxies /api to http://localhost:8000.

## Install dependencies
Frontend:
```
npm install
```

Backend:
```
pip install -r server/requirements.txt
```

## Run locally
Run backend (port 8000):
```bash
uvicorn server.main:app --reload --port 8000
```

Health check:
```bash
curl http://localhost:8000/api/health
```

In a separate terminal, run frontend (port 3000):
```bash
npm run dev
```
Open http://localhost:3000

## Build for production
```bash
npm run build
```

## Docker
Using docker-compose:
```bash
docker-compose up -d --build
```

This starts both backend (port 8000) and frontend (port 3000). Access at http://localhost:3000

Make sure your `.env` file has `API_KEY`, `BASE_URL` and `VITE_API_BASE_URL` set.

To stop:
```bash
docker-compose down
```

To rebuild after code changes:
```bash
docker-compose up -d --build
```

Access the app at http://localhost:3000

## Troubleshooting
- Error message on UI: "Sorry, something went wrong while generating content": ensure backend is running and health check returns ok.
- Verify `.env` has correct API_KEY, BASE_URL and VITE_API_BASE_URL and you restarted backend after changes.
- If responses contain malformed JSON, backend now attempts fallback parsing; check server logs for tags like `generate-tips:` or `from-topic:` in errors.
