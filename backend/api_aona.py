from flask import Flask, jsonify, request, send_from_directory
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
    usuario = data.get('usuario')
    email = data.get('email')
    contrasena = data.get('contrasena')
    contacto = data.get('contacto')
    documento = data.get('documento')
    id_rol = data.get('id_rol', 1) 
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not (str(contacto).isdigit() and str(documento).isdigit()):
        return jsonify({"success": False, "message": "Contacto y documento deben ser numéricos"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500

    print("Datos recibidos:", nombre, usuario, email, contrasena, contacto, documento, id_rol, fecha_registro)
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, usuario, email, contrasena, numero_contacto, documento, id_rol, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, usuario, email, contrasena, contacto, documento, id_rol, fecha_registro))
        connection.commit()
        return jsonify({"success": True, "message": "Usuario registrado con éxito"}), 201
    except Exception as e:
        import traceback
        print("Error en registro:", e)
        traceback.print_exc()
        return jsonify({"success": False, "message": "Error interno"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
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
            SELECT * FROM usuarios 
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
    id_autor = None
    texto = request.form.get('texto')
    usuario = request.form.get('usuario')
    fecha_publicacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    imagen_url = None

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (usuario,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 400
        id_autor = user["id"]

        tipo = "texto"
        if 'imagen' in request.files and request.files['imagen']:
            imagen = request.files['imagen']
            filename = secure_filename(imagen.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(ruta)
            imagen_url = f"/uploads/{filename}"
            tipo = "imagen"

        cursor.execute("""
            INSERT INTO publicaciones (id_autor, titulo, tipo, contenido, fecha_publicacion, estado_aprobacion, vistas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_autor,
            texto[:50] if texto else "Sin título",
            tipo,
            texto,
            fecha_publicacion,
            "aprobado",
            0
        ))
        connection.commit()
        id_publicacion = cursor.lastrowid

        if imagen_url:
            cursor.execute("""
                INSERT INTO imagenes_publicacion (id_publicacion, url)
                VALUES (%s, %s)
            """, (id_publicacion, imagen_url))
            connection.commit()

        return jsonify({"success": True, "message": "Publicación guardada"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "No se pudo guardar la publicación"}), 500
    finally:
        cursor.close()
        connection.close()

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
            SELECT p.id, p.titulo, p.contenido, p.fecha_publicacion, u.nombre AS autor,
                (SELECT url FROM imagenes_publicacion WHERE id_publicacion = p.id LIMIT 1) AS imagen_url
            FROM publicaciones p
            JOIN usuarios u ON p.id_autor = u.id
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

@app.route('/api/productos')
def get_productos():
    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                p.id, p.nombre, p.descripcion, p.precio, p.stock, p.id_categoria,
                (SELECT url FROM imagenes_producto i WHERE i.id_producto = p.id LIMIT 1) AS imagen
            FROM productos p
        """)
        productos = cursor.fetchall()
        for p in productos:
            if not p['imagen']:
                p['imagen'] = f"https://picsum.photos/seed/producto{p['id']}/200/200"
        return jsonify(productos), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "No se pudieron obtener los productos"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

