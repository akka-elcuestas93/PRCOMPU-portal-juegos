# test_api.py
"""
Prueba automatizada del backend Flask (API /api/games)
Usa la API_KEY dev-123 solo para verificación local, no requiere login por cookies.
"""

import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
API_KEY = os.getenv("API_KEY", "dev-123")

# Header con API key (modo test)
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

TEST_TITLE = "__TEST_GAME__"

def main():
    print(f"Conectando a {BASE_URL}/api ...")

    # 0) Limpieza previa si existe ese título
    r = requests.get(f"{BASE_URL}/api/games?q={TEST_TITLE}", headers=HEADERS)
    r.raise_for_status()
    for item in r.json().get("items", []):
        if item.get("title") == TEST_TITLE:
            print(f"- Eliminando juego previo con título {TEST_TITLE}")
            requests.delete(f"{BASE_URL}/api/games/{item['id']}", headers=HEADERS)

    # 1) Crear
    payload = {
        "title": TEST_TITLE,
        "genre": "Arcade",
        "url": "https://example.com/test",
        "image_url": "https://picsum.photos/200",
        "description": "Juego de prueba",
        "rating": 4.2,
    }
    print("- Creando juego de prueba...")
    r = requests.post(f"{BASE_URL}/api/games", json=payload, headers=HEADERS)
    assert r.status_code == 201, f"Fallo creación: {r.text}"
    game = r.json()
    game_id = game["id"]

    # 2) Listar
    print("- Listando juegos...")
    r = requests.get(f"{BASE_URL}/api/games", headers=HEADERS)
    assert r.status_code == 200, f"Error al listar: {r.text}"
    assert any(g["id"] == game_id for g in r.json().get("items", []))

    # 3) Leer uno
    print("- Obteniendo juego individual...")
    r = requests.get(f"{BASE_URL}/api/games/{game_id}", headers=HEADERS)
    assert r.status_code == 200, f"Error al leer: {r.text}"
    assert r.json()["title"] == TEST_TITLE

    # 4) Update
    print("- Actualizando juego...")
    upd = {"rating": 4.8, "genre": "Arcade/Action"}
    r = requests.patch(f"{BASE_URL}/api/games/{game_id}", json=upd, headers=HEADERS)
    assert r.status_code == 200, f"Error al actualizar: {r.text}"
    assert abs(r.json()["rating"] - 4.8) < 1e-9

    # 5) Delete
    print("- Eliminando juego...")
    r = requests.delete(f"{BASE_URL}/api/games/{game_id}", headers=HEADERS)
    assert r.status_code == 200, f"Error al borrar: {r.text}"

    # 6) Confirmar borrado
    r = requests.get(f"{BASE_URL}/api/games/{game_id}", headers=HEADERS)
    assert r.status_code == 404, f"Juego no borrado correctamente: {r.text}"

    print("✅ CRUD completo verificado con éxito.")


if __name__ == "__main__":
    main()
