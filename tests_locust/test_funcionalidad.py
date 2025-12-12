from locust import HttpUser, task, between
import random
import string
import json

HOST = "http://localhost:5000"

def rand_str(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

class FuncionalidadUser(HttpUser):
    host = HOST
    wait_time = between(1, 3)

    @task(2)
    def ver_publicaciones_y_productos(self):
        with self.client.get("/publicaciones", name="/publicaciones", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"GET /publicaciones returned {r.status_code}")
        with self.client.get("/api/productos", name="/api/productos", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"GET /api/productos returned {r.status_code}")

    @task(1)
    def registro_y_login_basico(self):
        suffix = rand_str()
        payload = {
            "nombre": f"TestUser{suffix}",
            "usuario": f"user{suffix}",
            "email": f"test{suffix}@example.com",
            "contrasena": "Password123!",
            "contacto": "1234567890",
            "documento": "12345678",
            "id_rol": 1
        }
        with self.client.post("/registro", json=payload, name="/registro", catch_response=True) as r:
            if r.status_code not in (200, 201):
                r.failure(f"POST /registro returned {r.status_code}")
        login_payload = {"identificador": payload["usuario"], "contrasena": payload["contrasena"]}
        with self.client.post("/login", json=login_payload, name="/login", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"POST /login returned {r.status_code}")