from locust import HttpUser, task, between
import random
import string

HOST = "http://localhost:5000"

def rand_str(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

class SeguridadUser(HttpUser):
    host = HOST
    wait_time = between(1, 2)

    @task(2)
    def sql_injection_login(self):
        payload = {
            "identificador": "' OR '1'='1",
            "contrasena": "' OR '1'='1"
        }
        with self.client.post("/login", json=payload, name="/login-sqli", catch_response=True) as r:
            # esperamos que el servicio no devuelva 200 con éxito para credenciales injertadas
            if r.status_code == 200 and ("token" in r.text or "success" in r.text.lower()):
                r.failure("Possible SQLi vulnerability: login succeeded with injection payload")

    @task(1)
    def overflow_test_registro(self):
        long_str = "A" * 5000
        payload = {
            "nombre": long_str,
            "usuario": long_str,
            "email": f"{rand_str()}@example.com",
            "contrasena": "p",
            "contacto": "1",
            "documento": "1",
            "id_rol": 1
        }
        with self.client.post("/registro", json=payload, name="/registro-overflow", catch_response=True) as r:
            if r.status_code >= 500:
                r.failure(f"Server error for large payload: {r.status_code}")