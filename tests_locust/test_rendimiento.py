from locust import HttpUser, task, between
HOST = "http://localhost:5000"

class RendimientoUser(HttpUser):
    host = HOST
    wait_time = between(0.1, 0.5)  # flujo rápido para carga

    @task(6)
    def publicaciones(self):
        self.client.get("/publicaciones", name="/publicaciones")

    @task(3)
    def productos(self):
        self.client.get("/api/productos", name="/api/productos")

    @task(1)
    def ver_imagenes_uploads(self):
        # intenta obtener una imagen con nombre ejemplo (si existe)
        self.client.get("/uploads/sample.jpg", name="/uploads/sample.jpg", catch_response=False)