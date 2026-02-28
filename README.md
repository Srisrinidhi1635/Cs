# Smart Home Service Assistant

Production-ready full-stack web application that connects users with nearby home service technicians.

## Tech Stack
- **Frontend:** React + Vite + Tailwind CSS + Framer Motion
- **Backend:** Flask REST API + JWT Auth
- **Database:** MongoDB
- **NLP:** Rule-based service classification utility (`spaCy/OpenAI-ready extension point`)

## Project Structure
```
/backend
  /controllers
  /database
  /models
  /routes
  /utils
/frontend
  /src/components
  /src/pages
  /src/contexts
/database
/models
/controllers
/routes
/utils
```

## Environment Variables
Create `backend/.env`:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=smart_home_service_assistant
JWT_SECRET_KEY=replace-with-strong-secret
JWT_EXPIRES_HOURS=24
OPENAI_API_KEY=
```

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:5000/api
```

## Installation
### 1) Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API starts at `http://localhost:5000`.

### 2) Frontend setup
```bash
cd frontend
npm install
npm run dev
```

Frontend starts at `http://localhost:5173`.

## API Endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/technicians` (technician registration)
- `GET /api/technicians?service_type=plumber&lat=..&lng=..`
- `PATCH /api/technicians/<id>/approve` (admin only)
- `POST /api/bookings` (JWT)
- `GET /api/bookings` (JWT)
- `DELETE /api/bookings/<id>` (JWT)
- `POST /api/chatbot/analyze` (JWT)
- `GET /api/admin/dashboard` (admin JWT)

## NLP Chatbot Classification
Implemented in `backend/utils/nlp.py`.
Example mappings:
- "My sink is leaking" → `plumber`
- "Lights not working in my room" → `electrician`
- "Need someone to paint my walls" → `painter`

## MongoDB Collections
- `users`
- `technicians`
- `bookings`
- `chat_history`

Detailed schema + sample queries: `database/mongodb_schema.js`.

## Notes
- Password hashing via Werkzeug.
- JWT-protected private routes.
- Distance matching via Haversine formula.
- Responsive UI with dashboard sidebar and animated chatbot messages.
