from __future__ import annotations

import math
import random
import string
from datetime import datetime

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "smart-home-assistant-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_home.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

SERVICE_KEYWORDS = {
    "electrical": ["fan", "electric", "wiring", "switch", "light", "power", "voltage"],
    "plumbing": ["water", "leak", "pipe", "tap", "drain", "toilet", "seepage"],
    "carpentry": ["wood", "furniture", "door", "table", "cabinet", "repair shelf"],
    "painting": ["paint", "wall color", "coating", "primer"],
    "masonry": ["brick", "cement", "plaster", "crack", "tile", "floor"],
    "cleaning": ["clean", "dust", "deep clean", "sanitize", "mop"],
    "appliance repair": [
        "washing machine",
        "refrigerator",
        "fridge",
        "ac",
        "microwave",
        "appliance",
    ],
}

CITY_COORDS = {
    "new york": (40.7128, -74.0060),
    "san francisco": (37.7749, -122.4194),
    "chicago": (41.8781, -87.6298),
    "seattle": (47.6062, -122.3321),
    "austin": (30.2672, -97.7431),
}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80), nullable=True)
    role = db.Column(db.String(20), default="user")  # user / worker / admin

    # worker profile fields
    service_category = db.Column(db.String(80), nullable=True)
    area = db.Column(db.String(120), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    available = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=4.5)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(12), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    issue_text = db.Column(db.String(300), nullable=False)
    detected_category = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    distance_km = db.Column(db.Float, nullable=True)
    payment_mode = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(30), default="Assigned")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id], backref="bookings_as_user")
    worker = db.relationship("User", foreign_keys=[worker_id], backref="bookings_as_worker")


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    worker = db.relationship("User", backref="worker_notifications")
    booking = db.relationship("Booking", backref="notifications")


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


def detect_service(text: str) -> str:
    lower = text.lower()
    scored = []
    for category, keywords in SERVICE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in lower)
        scored.append((score, category))
    top = max(scored, key=lambda item: item[0])
    return top[1] if top[0] > 0 else "cleaning"


def parse_location(city: str, latitude: str | None, longitude: str | None):
    city_norm = (city or "").strip().lower()
    lat = None
    lon = None

    if latitude and longitude:
        try:
            lat = float(latitude)
            lon = float(longitude)
        except ValueError:
            pass

    if lat is None or lon is None:
        if city_norm in CITY_COORDS:
            lat, lon = CITY_COORDS[city_norm]
        else:
            lat, lon = 20.5937, 78.9629
    return city_norm.title(), lat, lon


def haversine_distance(lat1, lon1, lat2, lon2):
    radius = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def find_nearest_worker(category: str, user_lat: float, user_lon: float):
    workers = User.query.filter_by(role="worker", service_category=category, available=True).all()
    workers = [w for w in workers if w.latitude is not None and w.longitude is not None]
    if not workers:
        return None, None

    nearest = min(
        workers,
        key=lambda w: haversine_distance(user_lat, user_lon, w.latitude, w.longitude),
    )
    distance = haversine_distance(user_lat, user_lon, nearest.latitude, nearest.longitude)
    return nearest, round(distance, 2)


def generate_booking_code() -> str:
    return "BK" + "".join(random.choices(string.digits + string.ascii_uppercase, k=8))


def require_role(*roles):
    if not current_user.is_authenticated or current_user.role not in roles:
        flash("You do not have permission to access this page.", "danger")
        return False
    return True


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("role", "user")
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        city = request.form.get("city", "")
        phone = request.form.get("phone", "")

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            city=city,
            role=role,
            phone=phone or None,
        )

        if role == "worker":
            category = request.form.get("service_category", "")
            area = request.form.get("area", "")
            phone = request.form.get("phone", "")
            lat = request.form.get("latitude")
            lon = request.form.get("longitude")
            _, lat, lon = parse_location(city, lat, lon)
            user.service_category = category
            user.area = area
            user.phone = phone
            user.latitude = lat
            user.longitude = lon
            user.available = True
            user.rating = 4.5

        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", categories=list(SERVICE_KEYWORDS.keys()))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role", "user").strip().lower()
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")

        if not identifier or not password:
            flash("Please provide login ID and password.", "danger")
            return render_template("login.html")

        normalized = identifier.lower()
        user = User.query.filter(
            (db.func.lower(User.email) == normalized) | (User.phone == identifier)
        ).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid credentials", "danger")
            return render_template("login.html")

        if role == "worker" and user.role != "worker":
            flash("This account is not registered as a worker.", "danger")
            return render_template("login.html")

        if role == "user" and user.role == "worker":
            flash("Please use Worker Login for worker accounts.", "danger")
            return render_template("login.html")

        login_user(user)
        flash("Welcome back!", "success")
        if user.role == "worker":
            return redirect(url_for("worker_dashboard"))
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "worker":
        return redirect(url_for("worker_dashboard"))
    history = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("dashboard.html", history=history)


@app.route("/worker-dashboard")
@login_required
def worker_dashboard():
    if not require_role("worker"):
        return redirect(url_for("dashboard"))

    assigned_bookings = (
        Booking.query.filter_by(worker_id=current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    notifications = (
        Notification.query.filter_by(worker_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return render_template("worker_dashboard.html", bookings=assigned_bookings, notifications=notifications)


@app.route("/notification/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_notification_read(notification_id: int):
    notification = db.session.get(Notification, notification_id)
    if not notification or notification.worker_id != current_user.id:
        flash("Notification not found.", "danger")
        return redirect(url_for("worker_dashboard"))

    notification.is_read = True
    db.session.commit()
    return redirect(url_for("worker_dashboard"))


@app.route("/chat")
@login_required
def chat():
    if current_user.role == "worker":
        flash("Workers should use worker dashboard to view assigned issues.", "info")
        return redirect(url_for("worker_dashboard"))
    return render_template("chat.html", categories=list(SERVICE_KEYWORDS.keys()))


@app.route("/api/chatbot", methods=["POST"])
@login_required
def chatbot_api():
    payload = request.get_json()
    message = payload.get("message", "")
    city = payload.get("city", "")
    latitude = payload.get("latitude")
    longitude = payload.get("longitude")

    category = detect_service(message)
    city_label, lat, lon = parse_location(city, latitude, longitude)
    worker, distance = find_nearest_worker(category, lat, lon)

    if not worker:
        return jsonify(
            {
                "service": category,
                "reply": f"I detected '{category}'. No available workers nearby right now.",
            }
        )

    eta = max(20, int(distance * 8))
    return jsonify(
        {
            "service": category,
            "reply": f"Detected {category}. Nearest worker: {worker.name}, {distance} km away.",
            "provider": {
                "id": worker.id,
                "name": worker.name,
                "distance": distance,
                "phone": worker.phone,
                "eta": eta,
                "city": worker.city,
                "rating": worker.rating,
            },
            "location": {"city": city_label, "latitude": lat, "longitude": lon},
        }
    )


@app.route("/book", methods=["POST"])
@login_required
def book_service():
    worker_id = request.form.get("provider_id", type=int)
    issue = request.form.get("issue", "")
    category = request.form.get("category", "")
    city = request.form.get("city", "")
    latitude = request.form.get("latitude", type=float)
    longitude = request.form.get("longitude", type=float)
    payment_mode = request.form.get("payment_mode", "UPI")

    worker = db.session.get(User, worker_id)
    if not worker or worker.role != "worker":
        flash("Worker unavailable.", "danger")
        return redirect(url_for("chat"))

    booking = Booking(
        booking_code=generate_booking_code(),
        user_id=current_user.id,
        worker_id=worker.id,
        issue_text=issue,
        detected_category=category,
        city=city,
        latitude=latitude,
        longitude=longitude,
        distance_km=round(haversine_distance(latitude, longitude, worker.latitude, worker.longitude), 2),
        payment_mode=payment_mode,
        status="Assigned",
    )
    db.session.add(booking)
    db.session.flush()

    notification = Notification(
        worker_id=worker.id,
        booking_id=booking.id,
        message=f"New issue from {current_user.name}: {issue}",
    )
    db.session.add(notification)
    db.session.commit()

    flash(f"Service booked successfully. Booking ID: {booking.booking_code}", "success")
    return redirect(url_for("dashboard"))


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin_panel():
    if not require_role("admin"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        if User.query.filter_by(email=email).first():
            flash("Worker email already exists", "danger")
            return redirect(url_for("admin_panel"))

        city = request.form["city"]
        lat = request.form.get("latitude")
        lon = request.form.get("longitude")
        _, lat, lon = parse_location(city, lat, lon)

        worker = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(request.form.get("password", "worker123")),
            city=city,
            role="worker",
            service_category=request.form["category"],
            area=request.form.get("area"),
            latitude=lat,
            longitude=lon,
            phone=request.form["phone"],
            available=request.form.get("available") == "on",
            rating=request.form.get("rating", type=float) or 4.5,
        )
        db.session.add(worker)
        db.session.commit()
        flash("Worker added", "success")
        return redirect(url_for("admin_panel"))

    workers = User.query.filter_by(role="worker").order_by(User.service_category.asc()).all()
    requests_data = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin.html", providers=workers, requests_data=requests_data)


def seed_data():
    if not User.query.filter_by(email="admin@smarthome.com").first():
        admin = User(
            name="System Admin",
            email="admin@smarthome.com",
            password_hash=generate_password_hash("admin123"),
            city="New York",
            role="admin",
        )
        db.session.add(admin)

    if User.query.filter_by(role="worker").count() == 0:
        workers = [
            User(name="Alex Sparks", email="alex@smarthome.com", password_hash=generate_password_hash("worker123"), city="New York", role="worker", service_category="electrical", area="Queens", latitude=40.7282, longitude=-73.7949, phone="+1-555-1001", available=True, rating=4.7),
            User(name="Mia Pipes", email="mia@smarthome.com", password_hash=generate_password_hash("worker123"), city="New York", role="worker", service_category="plumbing", area="Brooklyn", latitude=40.6782, longitude=-73.9442, phone="+1-555-1002", available=True, rating=4.6),
            User(name="Noah Wood", email="noah@smarthome.com", password_hash=generate_password_hash("worker123"), city="Chicago", role="worker", service_category="carpentry", area="Loop", latitude=41.8837, longitude=-87.6325, phone="+1-555-1003", available=True, rating=4.8),
            User(name="Ella Colors", email="ella@smarthome.com", password_hash=generate_password_hash("worker123"), city="San Francisco", role="worker", service_category="painting", area="Sunset", latitude=37.7599, longitude=-122.4148, phone="+1-555-1004", available=True, rating=4.4),
            User(name="Ava Stone", email="ava@smarthome.com", password_hash=generate_password_hash("worker123"), city="Austin", role="worker", service_category="masonry", area="Downtown", latitude=30.2676, longitude=-97.7429, phone="+1-555-1005", available=True, rating=4.5),
            User(name="Liam Fresh", email="liam@smarthome.com", password_hash=generate_password_hash("worker123"), city="Seattle", role="worker", service_category="cleaning", area="Capitol Hill", latitude=47.6231, longitude=-122.3197, phone="+1-555-1006", available=True, rating=4.9),
            User(name="Olivia Fixit", email="olivia@smarthome.com", password_hash=generate_password_hash("worker123"), city="Chicago", role="worker", service_category="appliance repair", area="Hyde Park", latitude=41.7943, longitude=-87.5907, phone="+1-555-1007", available=True, rating=4.7),
        ]
        db.session.add_all(workers)

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
