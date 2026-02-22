# Smart Home Service Assistant

A complete Flask web application that connects users with nearby home service providers using an AI-style NLP chatbot and location-based matching.

## Features

- User authentication (register/login/logout)
- AI chatbot with keyword-based NLP intent detection
- Location-based nearest technician assignment (Haversine distance)
- Multi-service categories:
  - Electrical works
  - Plumbing
  - Carpentry
  - Painting
  - Masonry
  - Cleaning
  - Appliance repair
- Service booking with booking ID and payment mode
- User dashboard for tracking and history
- Admin panel for technician and request management
- Responsive light-blue modern UI

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Flask, Flask-Login, Flask-SQLAlchemy
- Database: SQLite

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:5000`

## Demo Accounts

- Admin: `admin@smarthome.com` / `admin123`

## Project Structure

```text
app.py
templates/
static/css/style.css
static/js/chat.js
requirements.txt
```
