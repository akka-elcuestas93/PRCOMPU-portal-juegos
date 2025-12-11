# servidor.py
import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


# CARGA .env ANTES DE IMPORTAR database/models
load_dotenv()

from database import Base, engine, SessionLocal
from models import Game, User

# ---------------------------------------------------------------------

app = Flask(__name__)

# CORS con credenciales (cookies)
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)

# Config sesión/cookies
app.secret_key = os.getenv("SECRET_KEY", "change-me")
app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"

# Crear tablas
with engine.begin() as conn:
    Base.metadata.create_all(bind=conn)

# Seed/actualiza admin por defecto (username=1234, password=1234)
with SessionLocal() as db:
    existing = db.execute(select(User).where(User.username == "1234")).scalar_one_or_none()
    if existing:
        existing.role = "admin"
        existing.set_password("1234")
        db.commit()
    else:
        admin = User(username="1234", role="admin")
        admin.set_password("1234")
        db.add(admin)
        db.commit()

# ---------------------------------------------------------------------
# Helpers

def current_user():
    uid = session.get("uid")
    if not uid:
        return None
    with SessionLocal() as db:
        return db.get(User, uid)

def login_required(fn):
    def wrapper(*args, **kwargs):
        if not session.get("uid"):
            return jsonify({"error": "Not authenticated"}), 401
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def admin_required(fn):
    def wrapper(*args, **kwargs):
        uid = session.get("uid")
        role = session.get("role")
        if not uid or role != "admin":
            return jsonify({"error": "Admin required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def get_json():
    if not request.is_json:
        return None, (jsonify({"error": "Body must be JSON"}), 415)
    return request.get_json(), None

# ---------------------------------------------------------------------
# RUTAS CRUD DE JUEGOS

@app.get("/api/games")
def list_games():
    """Listar juegos (visible para todos)."""
    q = request.args.get("q")
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))
    with SessionLocal() as db:
        stmt = select(Game)
        if q:
            stmt = stmt.where(Game.title.ilike(f"%{q}%"))
        items = db.execute(stmt).scalars().all()
        total = len(items)
        data = [g.to_dict() for g in items[offset: offset + limit]]
        return jsonify({"items": data, "total": total, "limit": limit, "offset": offset})

@app.get("/api/games/<int:game_id>")
def get_game(game_id: int):
    """Obtener un juego concreto (visible para todos)."""
    with SessionLocal() as db:
        obj = db.get(Game, game_id)
        if not obj:
            return jsonify({"error": "Game not found"}), 404
        return jsonify(obj.to_dict())

@app.post("/api/games")
@admin_required
def create_game():
    """Crear juego (solo admin)."""
    data = request.get_json(force=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "'title' is required"}), 400
    obj = Game(
        title=title,
        genre=data.get("genre"),
        url=data.get("url"),
        image_url=data.get("image_url"),
        description=data.get("description"),
        rating=data.get("rating"),
    )
    with SessionLocal() as db:
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return jsonify({"error": "title already exists"}), 409
        db.refresh(obj)
        return jsonify(obj.to_dict()), 201

@app.put("/api/games/<int:game_id>")
@app.patch("/api/games/<int:game_id>")
@admin_required
def update_game(game_id: int):
    """Actualizar juego (solo admin)."""
    data = request.get_json(force=True) or {}
    with SessionLocal() as db:
        obj = db.get(Game, game_id)
        if not obj:
            return jsonify({"error": "not found"}), 404
        for field in ("title", "genre", "url", "image_url", "description", "rating"):
            if field in data:
                setattr(obj, field, data[field])
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return jsonify({"error": "title already exists"}), 409
        db.refresh(obj)
        return jsonify(obj.to_dict())

@app.delete("/api/games/<int:game_id>")
@admin_required
def delete_game(game_id: int):
    """Eliminar juego (solo admin)."""
    with SessionLocal() as db:
        obj = db.get(Game, game_id)
        if not obj:
            return jsonify({"error": "not found"}), 404
        db.delete(obj)
        db.commit()
        return jsonify({"status": "deleted", "id": game_id})

# ---------------------------------------------------------------------
# AUTH (registro, login, logout, sesión)

@app.post("/api/auth/register")
def register():
    data = request.get_json(force=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    with SessionLocal() as db:
        exists = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if exists:
            return jsonify({"error": "username already taken"}), 409
        u = User(username=username, role="user")
        u.set_password(password)
        db.add(u)
        db.commit()
        return jsonify({"ok": True})

@app.post("/api/auth/login")
def login():
    data = request.get_json(force=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    with SessionLocal() as db:
        u = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if not u or not u.check_password(password):
            return jsonify({"error": "invalid credentials"}), 401
        # sesión
        session["uid"] = u.id
        session["role"] = u.role
        session.permanent = True  # cookie persistente
        return jsonify({"ok": True, "user": u.to_safe()})

@app.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})

@app.get("/api/me")
def me():
    u = current_user()
    if not u:
        return jsonify({"user": None})
    return jsonify({"user": u.to_safe()})

# ---------------------------------------------------------------------

@app.teardown_appcontext
def remove_session(exc=None):
    SessionLocal.remove()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render te da PORT
    app.run(host="0.0.0.0", port=port)