# Smart Home Service Assistant

Production-style full-stack app to connect users with nearby home service technicians.

## Stack
- **Frontend:** React + Tailwind CSS + Vite
- **Backend:** Flask REST API + JWT
- **Database:** MongoDB
- **NLP:** keyword NLP classifier (spaCy/OpenAI pluggable via `backend/utils/nlp.py`)

## Project Structure
- `frontend/` React app (landing/chatbot, auth, dashboards, bookings)
- `backend/` Flask API, controllers, routes, models, utils
- `database/` MongoDB indexes/schema setup script
- `models/`, `controllers/`, `routes/`, `utils/` top-level references

## Backend API Endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/technicians` (JWT)
- `GET /api/technicians` (admin)
- `PATCH /api/technicians/<id>/approve` (admin)
- `PATCH /api/technicians/<id>/reject` (admin)
- `POST /api/chatbot/match` (JWT)
- `POST /api/bookings` (JWT)
- `GET /api/bookings/me` (JWT)
- `PATCH /api/bookings/<id>/cancel` (JWT)
- `GET /api/bookings` (admin)
- `GET /api/admin/dashboard` (admin)

## Run Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m backend.app
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

Set API URL with `VITE_API_BASE_URL=http://localhost:5000/api` if needed.
