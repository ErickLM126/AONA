from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

# Configuración de la BD
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        
    "password": "",         
    "database": "aona"       
}

app = Flask(__name__)
CORS(app)

# Función para conectar a MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Ruta para registrar artista
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    numero_contacto = data.get('contacto')
    documento = data.get('documento')
    contrasena = data.get('contrasena')

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO artistas (nombre, numero_contacto, documento, contrasena)
            VALUES (%s, %s, %s, %s)
        """, (nombre, numero_contacto, documento, contrasena))
        connection.commit()

        return jsonify({"success": True, "message": "Artista registrado con éxito"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "No se pudo registrar"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
