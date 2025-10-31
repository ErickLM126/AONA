# AONA

Resumen
-------
AONA es un proyecto con una API backend en Python y una interfaz frontend en React. Este README explica cómo instalar dependencias, ejecutar la API, correr el frontend y ejecutar pruebas.

Estructura principal
--------------------
- [backend/api_aona.py](backend/api_aona.py) — API backend (Python).  
- [backend/requirements.txt](backend/requirements.txt) — Dependencias Python.  
- [backend/db/harmonics_of_narutal_art.sql](backend/db/harmonics_of_narutal_art.sql) — SQL de ejemplo / esquema de base de datos.  
- [backend/tests/test_api_aona.py](backend/tests/test_api_aona.py) — Tests del backend.  
- [backend/tests/test_registro.py](backend/tests/test_registro.py) — Tests del backend.  
- [frontend/package.json](frontend/package.json) — Configuración y scripts del frontend (npm).  
- [frontend/README.md](frontend/README.md) — Información específica del frontend.  
- [frontend/src/main.jsx](frontend/src/main.jsx) — Punto de entrada React.  
- [frontend/src/index.js](frontend/src/index.js) — Montaje de la app.  
- [frontend/src/pages/home.jsx](frontend/src/pages/home.jsx) — Ejemplo de página.  
- [frontend/src/hooks/useRegistro.js](frontend/src/hooks/useRegistro.js) — Hook de registro.  
- [README.md](README.md) — Este archivo.

Requisitos previos
------------------
- Python 3.8+ y pip
- Node.js 14+ y npm (o yarn)
- git (opcional)
- SQLite o el motor que uses si importas [backend/db/harmonics_of_narutal_art.sql](backend/db/harmonics_of_narutal_art.sql)

Instalación y ejecución — Backend
--------------------------------
1. Crear y activar un entorno virtual (recomendado):
   ```sh
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```
2. Instalar dependencias:
   ```sh
   pip install -r backend/requirements.txt
   ```
3. (Opcional) Inicializar base de datos importando:
   ```sh
   sqlite3 mydb.sqlite < backend/db/harmonics_of_narutal_art.sql
   ```
4. Ejecutar la API:
   - Si [backend/api_aona.py](backend/api_aona.py):
     ```sh
     python backend/api_aona.py
     ```

Instalación y ejecución — Frontend
---------------------------------
1. Entrar al directorio frontend:
   ```sh
   cd frontend
   ```
2. Instalar dependencias:
   ```sh
   npm install
   ```
3. Ejecutar en modo desarrollo:
   ```sh
   npm start
   ```
4. Crear build de producción:
   ```sh
   npm run build
   ```

Pruebas
-------
- Backend (pytest):
  ```sh
  pytest -q
  ```
  Los tests están en [backend/tests](backend/tests).
- Frontend:
  - Si hay tests en [frontend/src](frontend/src), ejecutar:
    ```sh
    npm test
    ```

Configuración y variables de entorno
-----------------------------------
- Si la API espera variables (p. ej. DATABASE_URL, FLASK_ENV), exporta o crea un archivo `.env` según sea necesario antes de ejecutar.
- Ajusta URLs del frontend a la API backend en los servicios de [frontend/src/services](frontend/src/services) o hooks en [frontend/src/hooks](frontend/src/hooks).

Archivos importantes para inspeccionar
-------------------------------------
- [backend/api_aona.py](backend/api_aona.py) — revisar punto de entrada y rutas.
- [backend/requirements.txt](backend/requirements.txt) — dependencias backend.
- [frontend/package.json](frontend/package.json) — scripts útiles (start, build, test).
- [frontend/src](frontend/src) — código React, hooks y páginas.

Resolución de problemas comunes
-------------------------------
- Error de dependencias Python: asegúrate de activar el virtualenv y usar la versión correcta de Python.
- CORS al conectar frontend con backend: habilita CORS en [backend/api_aona.py](backend/api_aona.py) o usa proxy en [frontend/package.json](frontend/package.json).
- Puerto en uso: cambia el puerto en la configuración de la API o del servidor de desarrollo React.

Comandos rápidos
----------------
- Instalar backend y ejecutar:
  ```sh
  python -m venv .venv && .venv\Scripts\activate && pip install -r backend/requirements.txt && python backend/api_aona.py
  ```
- Instalar frontend y ejecutar:
  ```sh
  cd frontend && npm install && npm start
  ```
- Ejecutar tests (root):
  ```sh
  pytest -q
  ```

Contacto / Contribución
-----------------------
Para contribuir, crear ramas por feature/bugfix y abrir pull requests. Revisa y ejecuta tests antes de enviar PR.

Licencia
--------
Incluye aquí la licencia del proyecto si aplica.
