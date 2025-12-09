# auth.py
import os
import hmac
from functools import wraps
from flask import request, jsonify

API_KEY = os.getenv("API_KEY", "dev-123")

def _extract_bearer_token(auth_header: str) -> str | None:
    if not auth_header:
        return None
    # Esperamos "Bearer <token>"
    parts = auth_header.split(" ", 1)
    if len(parts) != 2:
        return None
    scheme, token = parts[0].strip(), parts[1].strip()
    if scheme.lower() != "bearer":
        return None
    return token

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = _extract_bearer_token(request.headers.get("Authorization", ""))
        if token is None:
            return jsonify({"error": "Missing or malformed Authorization header"}), 401
        # Comparación constante (evita filtrado por tiempo)
        if not hmac.compare_digest(token, API_KEY):
            return jsonify({"error": "Invalid API key"}), 403
        return f(*args, **kwargs)
    return wrapper
