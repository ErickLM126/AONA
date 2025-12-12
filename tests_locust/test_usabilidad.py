from locust import HttpUser, task, between
import random
import string
import time

HOST = "http://localhost:5000"

def rand_str(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

class UsabilidadUser(HttpUser):
    host = HOST
    wait_time = between(2, 4)

    @task(1)
    def flujo_basico_usuario(self):
        # registro
        suffix = rand_str()
        usuario = f"user{suffix}"
        email = f"user{suffix}@example.com"
        registro = {
            "nombre": "UsabilTest",
            "usuario": usuario,
            "email": email,
            "contrasena": "Password123!",
            "contacto": "999999999",
            "documento": "11111111",
            "id_rol": 1
        }
        with self.client.post("/registro", json=registro, name="/registro", catch_response=True) as r:
            if r.status_code not in (200, 201):
                r.failure(f"Registro fallido: {r.status_code}")

        # login
        login = {"identificador": usuario, "contrasena": registro["contrasena"]}
        with self.client.post("/login", json=login, name="/login", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"Login fallido: {r.status_code}")
            # si el login devuelve un token, lo podríamos usar; aquí seguimos simple

        # ver publicaciones
        self.client.get("/publicaciones", name="/publicaciones")

        # publicar un texto simple (si endpoint /publicar acepta form-data)
        data = {"texto": f"Post de prueba {rand_str(4)}", "usuario": usuario}
        with self.client.post("/publicar", data=data, name="/publicar", catch_response=True) as r:
            if r.status_code not in (200, 201):
                # no marcamos fatal, solo registramos fallo
                r.failure(f"Publicar falló: {r.status_code}")