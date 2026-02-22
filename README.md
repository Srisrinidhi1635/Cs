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

## Where to run this code

You can run this project in any environment that has **Python 3.10+** and `pip`:

- Your local machine (Windows / macOS / Linux)
- VS Code integrated terminal
- GitHub Codespaces
- Replit / Render / Railway (for demo deployment)

For easiest setup, run locally in a terminal from the project folder.

## Setup (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open in browser: `http://localhost:5000`

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
