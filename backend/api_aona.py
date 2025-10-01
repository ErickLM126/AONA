from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from werkzeug.utils import secure_filename


DB_CONFIG = {
    "host": "localhost",
    "user": "root",        
    "password": "",         
    "database": "aona"       
}

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    numero_contacto = data.get('contacto')
    documento = data.get('documento')
    contrasena = data.get('contrasena')

    if not (str(numero_contacto).isdigit() and str(documento).isdigit()):
        return jsonify({"success": False, "message": "Documento y número de contacto solo deben contener números."}), 400

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

@app.route('/login', methods=['GET','POST'])
def login_usuario():
    data = request.get_json()
    identificador = data.get('identificador')
    contrasena = data.get('contrasena')

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM artistas 
            WHERE (documento = %s OR nombre = %s) AND contrasena = %s
        """, (identificador, identificador, contrasena))
        usuario = cursor.fetchone()

        if usuario:
            return jsonify({
                "success": True,
                "message": "Inicio de sesión exitoso",
                "usuario": {
                    "id": usuario["id"],
                    "nombre": usuario["nombre"],
                    "documento": usuario["documento"]
                }
            }), 200
        else:
            return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "No se pudo iniciar sesión"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/publicar', methods=['POST'])
def publicar():
    id_artista = None
    texto = request.form.get('texto')
    usuario = request.form.get('usuario')
    fecha_publicacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    imagen_url = None

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM artistas WHERE nombre = %s", (usuario,))
        artista = cursor.fetchone()
        if not artista:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 400
        id_artista = artista["id"]

        if 'imagen' in request.files and request.files['imagen']:
            imagen = request.files['imagen']
            filename = secure_filename(imagen.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(ruta)
            imagen_url = f"/uploads/{filename}"

        cursor.execute("""
            INSERT INTO publicaciones (id_artista, titulo, tipo, contenido, fecha_publicacion, estado_aprobacion, vistas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_artista,
            texto[:50] if texto else "Sin título",
            "normal",
            texto,
            fecha_publicacion,
            "aprobado",
            0
        ))
        connection.commit()
        id_publicacion = cursor.lastrowid

        if imagen_url:
            cursor.execute("""
                INSERT INTO imagenes (url, id_publicacion)
                VALUES (%s, %s)
            """, (imagen_url, id_publicacion))
            connection.commit()

        return jsonify({"success": True, "message": "Publicación guardada"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "No se pudo guardar la publicación"}), 500
    finally:
        cursor.close()
        connection.close()

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/publicaciones', methods=['GET'])
def obtener_publicaciones():
    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, p.titulo, p.contenido, p.fecha_publicacion, a.nombre AS autor,
                (SELECT url FROM imagenes WHERE id_publicacion = p.id LIMIT 1) AS imagen_url
            FROM publicaciones p
            JOIN artistas a ON p.id_artista = a.id
            ORDER BY p.fecha_publicacion DESC
        """)
        publicaciones = cursor.fetchall()
        return jsonify({"success": True, "publicaciones": publicaciones}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "No se pudieron obtener las publicaciones"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

