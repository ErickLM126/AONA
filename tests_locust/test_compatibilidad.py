from locust import HttpUser, task, between
import random

HOST = "http://localhost:5000"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "curl/7.64.1",
    "PostmanRuntime/7.28.4",
]

class CompatibilidadUser(HttpUser):
    host = HOST
    wait_time = between(1, 3)

    @task
    def publicaciones_varios_ua(self):
        ua = random.choice(USER_AGENTS)
        headers = {"User-Agent": ua}
        self.client.get("/publicaciones", headers=headers, name="/publicaciones (UA)")