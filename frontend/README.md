# BhoomiNetra Frontend

Clean, minimalist hospital-style frontend for the BhoomiNetra land records backend.

## Features

- Soft green + white medical theme
- Fully connected to the backend API
- Configurable base URL (easy to point to real backend later)
- Upload land records (PDF / JPG / PNG)
- Dashboard with status counts + review lists
- Record review & verification with field editing

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Make sure the backend is running at http://127.0.0.1:8000

# 3. Start the frontend
npm run dev
```

Open http://localhost:5173

## Configuration

All configurable values live in:

- `.env` → `VITE_API_BASE_URL`
- `src/config/index.js` → timeout, max file size, app name, etc.

When you move to the real/production backend, just change the value in `.env`.

## Project Structure

```
src/
├── api/            → Backend API calls
├── components/     → Reusable UI pieces
├── pages/          → Full screens
├── hooks/          → Data fetching logic
├── config/         → Easy-to-edit settings
└── utils/          → Helpers (labels, colors…)
```

## Backend Endpoints Used

| Method | Endpoint                     | Used In          |
|--------|------------------------------|------------------|
| GET    | /health                      | (optional)       |
| POST   | /documents/upload            | Upload Page      |
| GET    | /dashboard                   | Dashboard Page   |
| GET    | /records/{id}                | Review Page      |
| POST   | /records/{id}/verify         | Review Page      |
