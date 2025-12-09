from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid


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
            SELECT p.id, p.titulo, p.contenido, p.fecha_publicacion, u.nombre AS autor, u.id AS id_autor,
                   u.imagen_perfil_url AS imagen_perfil,
                   (SELECT url FROM imagenes_publicacion WHERE id_publicacion = p.id LIMIT 1) AS imagen_url
            FROM publicaciones p
            JOIN usuarios u ON p.id_autor = u.id
            ORDER BY p.fecha_publicacion DESC
        """)
        publicaciones = cursor.fetchall()
        
        # Procesar URLs de imágenes
        for pub in publicaciones:
            if pub['imagen_url'] and not pub['imagen_url'].startswith('http'):
                pub['imagen_url'] = f"http://localhost:5000{pub['imagen_url']}"
            if pub['imagen_perfil'] and not pub['imagen_perfil'].startswith('http'):
                pub['imagen_perfil'] = f"http://localhost:5000{pub['imagen_perfil']}"
        
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

# Endpoints para Chats

@app.route('/api/chats', methods=['GET'])
def obtener_chats():
    """Obtiene los chats del usuario actual con último mensaje"""
    try:
        usuario_id = request.args.get('usuario_id')
        if not usuario_id:
            return jsonify({"success": False, "message": "usuario_id requerido"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Obtener contactos (usuarios con los que ha chateado)
        cursor.execute("""
            SELECT DISTINCT 
                CASE 
                    WHEN id_emisor = %s THEN id_receptor 
                    ELSE id_emisor 
                END as id_contacto,
                u.nombre as nombre_contacto,
                u.imagen_perfil_url as imagen_contacto,
                MAX(c.fecha_envio) as ultima_interaccion
            FROM chats c
            JOIN usuarios u ON (
                (c.id_emisor = %s AND u.id = c.id_receptor) OR
                (c.id_receptor = %s AND u.id = c.id_emisor)
            )
            WHERE c.id_emisor = %s OR c.id_receptor = %s
            GROUP BY id_contacto, u.nombre, u.imagen_perfil_url
            ORDER BY ultima_interaccion DESC
        """, (usuario_id, usuario_id, usuario_id, usuario_id, usuario_id))
        
        chats = cursor.fetchall()
        
        # Procesar URLs de imágenes
        for chat in chats:
            if chat['imagen_contacto'] and not chat['imagen_contacto'].startswith('http'):
                chat['imagen_contacto'] = f"http://localhost:5000{chat['imagen_contacto']}"
        
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "chats": chats}), 200
    except Exception as e:
        print(f"[CHATS] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/chats/mensajes', methods=['GET'])
def obtener_mensajes():
    usuario1 = request.args.get('usuario1')
    usuario2 = request.args.get('usuario2')
    
    if not usuario1 or not usuario2:
        return jsonify({"success": False, "message": "usuario1 y usuario2 requeridos"}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.id, c.id_emisor, c.id_receptor, c.mensaje, c.fecha_envio,
                   u_emisor.nombre AS nombre_emisor, u_receptor.nombre AS nombre_receptor
            FROM chats c
            JOIN usuarios u_emisor ON c.id_emisor = u_emisor.id
            JOIN usuarios u_receptor ON c.id_receptor = u_receptor.id
            WHERE (c.id_emisor = %s AND c.id_receptor = %s) 
               OR (c.id_emisor = %s AND c.id_receptor = %s)
            ORDER BY c.fecha_envio ASC
        """, (usuario1, usuario2, usuario2, usuario1))
        
        mensajes = cursor.fetchall()
        return jsonify({"success": True, "mensajes": mensajes}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/chats/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    id_emisor = data.get('id_emisor')
    id_receptor = data.get('id_receptor')
    mensaje = data.get('mensaje')
    fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not all([id_emisor, id_receptor, mensaje]):
        return jsonify({"success": False, "message": "Datos incompletos"}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO chats (id_emisor, id_receptor, mensaje, fecha_envio)
            VALUES (%s, %s, %s, %s)
        """, (id_emisor, id_receptor, mensaje, fecha_envio))
        connection.commit()
        
        return jsonify({
            "success": True, 
            "message": "Mensaje enviado",
            "id_mensaje": cursor.lastrowid
        }), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/chats/buscar', methods=['GET'])
def buscar_chats():
    usuario_id = request.args.get('usuario_id')
    termino = request.args.get('termino', '')
    
    if not usuario_id:
        return jsonify({"success": False, "message": "usuario_id requerido"}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT DISTINCT 
                CASE 
                    WHEN c.id_emisor = %s THEN c.id_receptor
                    ELSE c.id_emisor
                END AS id_contacto
            FROM chats c
            WHERE (c.id_emisor = %s OR c.id_receptor = %s)
        """, (usuario_id, usuario_id, usuario_id))
        
        contactos_ids = cursor.fetchall()
        chats = []
        
        for contacto in contactos_ids:
            cursor.execute(
                "SELECT id, nombre FROM usuarios WHERE id = %s AND nombre LIKE %s",
                (contacto['id_contacto'], f"%{termino}%")
            )
            usuario_info = cursor.fetchone()
            if usuario_info:
                chats.append({
                    "id_contacto": usuario_info['id'],
                    "nombre_contacto": usuario_info['nombre']
                })
        
        return jsonify({"success": True, "chats": chats}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/perfil/<int:usuario_id>', methods=['GET'])
def obtener_perfil(usuario_id):
    """Obtiene los datos del perfil de un usuario"""
    try:
        print(f"[PERFIL GET] Iniciando - usuario_id: {usuario_id}")
        connection = get_db_connection()
        if not connection:
            print("[PERFIL GET] Error: No se pudo conectar a la BD")
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        cursor = connection.cursor(dictionary=True)
        # Obtener datos del usuario incluyendo imagen
        cursor.execute("""
            SELECT id, nombre, usuario, email, numero_contacto, documento, 
                   fecha_registro, imagen_perfil_url
            FROM usuarios
            WHERE id = %s
        """, (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            print(f"[PERFIL GET] Usuario {usuario_id} no encontrado")
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
        print(f"[PERFIL GET] Usuario ID: {usuario['id']}")
        # Obtener publicaciones del usuario incluyendo conteo de reacciones
        cursor.execute("""
            SELECT p.id, p.titulo, p.contenido, p.fecha_publicacion, p.tipo,
                   (SELECT url FROM imagenes_publicacion WHERE id_publicacion = p.id LIMIT 1) AS imagen_url,
                   (SELECT COUNT(*) FROM reacciones WHERE id_publicacion = p.id) AS total_reacciones
            FROM publicaciones p
            WHERE p.id_autor = %s AND p.estado_aprobacion = 'aprobado'
            ORDER BY p.fecha_publicacion DESC
        """, (usuario_id,))
        publicaciones = cursor.fetchall()
        # Obtener productos (sencillos musicales) del usuario
        cursor.execute("""
            SELECT p.id, p.nombre as titulo, p.descripcion,
                   (SELECT url FROM imagenes_producto WHERE id_producto = p.id LIMIT 1) AS imagen_url
            FROM productos p
            WHERE p.id_artista = %s AND p.estado = 'activo'
            ORDER BY p.fecha_creacion DESC
            LIMIT 6
        """, (usuario_id,))
        productos = cursor.fetchall()
        # Obtener comentarios sobre publicaciones del usuario (desde tabla comentarios)
        cursor.execute("""
            SELECT c.id, c.comentario, u.nombre as autor, u.id as autor_id
            FROM comentarios c
            JOIN usuarios u ON c.id_usuario = u.id
            JOIN publicaciones p ON c.id_publicacion = p.id
            WHERE p.id_autor = %s
            ORDER BY c.fecha DESC
            LIMIT 5
        """, (usuario_id,))
        comentarios = cursor.fetchall()
        # Obtener estadísticas
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM publicaciones WHERE id_autor = %s AND estado_aprobacion = 'aprobado') AS publicaciones_count,
                (SELECT COUNT(*) FROM seguimientos WHERE id_seguido = %s) AS seguidores_count,
                (SELECT COUNT(*) FROM seguimientos WHERE id_usuario = %s) AS seguidos_count
        """, (usuario_id, usuario_id, usuario_id))
        stats = cursor.fetchone()
        # Procesar URLs de imágenes en publicaciones y productos
        for pub in publicaciones:
            if pub['imagen_url'] and not pub['imagen_url'].startswith('http'):
                pub['imagen_url'] = f"http://localhost:5000{pub['imagen_url']}"
        for prod in productos:
            if prod['imagen_url'] and not prod['imagen_url'].startswith('http'):
                prod['imagen_url'] = f"http://localhost:5000{prod['imagen_url']}"
        # Procesar imagen de perfil
        if usuario['imagen_perfil_url'] and not usuario['imagen_perfil_url'].startswith('http'):
            usuario['imagen_perfil_url'] = f"http://localhost:5000{usuario['imagen_perfil_url']}"
        # Agregar estadísticas al usuario
        usuario['publicaciones_count'] = stats['publicaciones_count'] if stats else 0
        usuario['seguidores_count'] = stats['seguidores_count'] if stats else 0
        usuario['seguidos_count'] = stats['seguidos_count'] if stats else 0
        perfil = {
            "success": True,
            "usuario": usuario,
            "publicaciones": publicaciones,
            "productos": productos,
            "comentarios": comentarios
        }
        print("[PERFIL GET] Respondiendo con exito")
        return jsonify(perfil), 200
    except Exception as e:
        print(f"[PERFIL GET] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

@app.route('/api/perfil/<int:usuario_id>', methods=['PUT'])
def actualizar_perfil(usuario_id):
    """Actualiza los datos del perfil de un usuario"""
    try:
        nombre = request.form.get('nombre')
        imagen = request.files.get('imagen')
        
        if not nombre:
            return jsonify({"success": False, "message": "El nombre es requerido"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        imagen_url = None
        
        # Actualizar nombre del usuario
        cursor.execute("""
            UPDATE usuarios
            SET nombre = %s
            WHERE id = %s
        """, (nombre, usuario_id))
        
        # Si hay imagen, guardarla
        if imagen:
            filename = secure_filename(imagen.filename)
            import uuid
            nombre_unico = f"{uuid.uuid4()}_{filename}"
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_unico)
            imagen.save(ruta)
            imagen_url = f"/uploads/{nombre_unico}"
            
            # Primero, desmarcar todas las imágenes anteriores como no principales
            cursor.execute("""
                UPDATE imagenes_perfil
                SET es_principal = 0
                WHERE id_usuario = %s
            """, (usuario_id,))
            
            # Guardar la nueva imagen en la tabla imagenes_perfil
            cursor.execute("""
                INSERT INTO imagenes_perfil (id_usuario, url, es_principal)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE url = %s
            """, (usuario_id, imagen_url, imagen_url))
            
            # Actualizar la columna imagen_perfil_url en usuarios
            cursor.execute("""
                UPDATE usuarios
                SET imagen_perfil_url = %s, fecha_actualizacion = NOW()
                WHERE id = %s
            """, (imagen_url, usuario_id))
            
            print(f"[PERFIL] Imagen guardada en: {imagen_url}")
        else:
            # Actualizar solo la fecha de actualizacion
            cursor.execute("""
                UPDATE usuarios
                SET fecha_actualizacion = NOW()
                WHERE id = %s
            """, (usuario_id,))
        
        connection.commit()
        
        # Obtener datos actualizados del usuario
        cursor.execute("""
            SELECT id, nombre, usuario, email, numero_contacto, documento, 
                   fecha_registro, imagen_perfil_url
            FROM usuarios
            WHERE id = %s
        """, (usuario_id,))
        usuario_actualizado = cursor.fetchone()
        
        print(f"[PERFIL] Usuario actualizado, imagen: {usuario_actualizado['imagen_perfil_url']}")
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "message": "Perfil actualizado correctamente",
            "usuario": {
                "id": usuario_actualizado['id'],
                "nombre": usuario_actualizado['nombre'],
                "usuario": usuario_actualizado['usuario'],
                "email": usuario_actualizado['email'],
                "numero_contacto": usuario_actualizado['numero_contacto'],
                "documento": usuario_actualizado['documento'],
                "fecha_registro": usuario_actualizado['fecha_registro'],
                "imagen_url": usuario_actualizado['imagen_perfil_url']
            }
        }), 200
    except Exception as e:
        print(f"[PERFIL] Error al actualizar: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

# ===== ENDPOINTS PARA GESTIÓN DE PUBLICACIONES =====

@app.route('/api/publicaciones/<int:publicacion_id>', methods=['PUT'])
def editar_publicacion(publicacion_id):
    """Edita una publicación existente"""
    try:
        data = request.form
        titulo = data.get('titulo')
        contenido = data.get('contenido')
        imagen = request.files.get('imagen')
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión"}), 500
        
        cursor = connection.cursor()
        
        # Verificar que la publicación existe
        cursor.execute("SELECT id_autor FROM publicaciones WHERE id = %s", (publicacion_id,))
        pub = cursor.fetchone()
        
        if not pub:
            return jsonify({"success": False, "message": "Publicación no encontrada"}), 404
        
        # Actualizar publicación
        cursor.execute("""
            UPDATE publicaciones
            SET titulo = %s, contenido = %s
            WHERE id = %s
        """, (titulo, contenido, publicacion_id))
        
        # Si hay imagen, guardarla
        if imagen:
            filename = secure_filename(imagen.filename)
            nombre_unico = f"{uuid.uuid4()}_{filename}"
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_unico)
            imagen.save(ruta)
            imagen_url = f"/uploads/{nombre_unico}"
            
            # Eliminar imagen anterior si existe
            cursor.execute("SELECT url FROM imagenes_publicacion WHERE id_publicacion = %s", (publicacion_id,))
            imagen_anterior = cursor.fetchone()
            if imagen_anterior:
                cursor.execute("DELETE FROM imagenes_publicacion WHERE id_publicacion = %s", (publicacion_id,))
            
            # Guardar nueva imagen
            cursor.execute("""
                INSERT INTO imagenes_publicacion (id_publicacion, url)
                VALUES (%s, %s)
            """, (publicacion_id, imagen_url))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Publicación actualizada"}), 200
        
    except Exception as e:
        print(f"[PUBLICACIONES] Error al editar: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/publicaciones/<int:publicacion_id>', methods=['DELETE'])
def eliminar_publicacion(publicacion_id):
    """Elimina una publicación"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión"}), 500
        
        cursor = connection.cursor()
        
        # Obtener imagen para eliminar del servidor
        cursor.execute("SELECT url FROM imagenes_publicacion WHERE id_publicacion = %s", (publicacion_id,))
        imagen = cursor.fetchone()
        
        if imagen:
            # Extraer nombre del archivo
            filename = imagen[0].split('/')[-1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Intentar eliminar archivo
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
            
            cursor.execute("DELETE FROM imagenes_publicacion WHERE id_publicacion = %s", (publicacion_id,))
        
        # Eliminar reacciones/comentarios
        cursor.execute("DELETE FROM reacciones WHERE id_publicacion = %s", (publicacion_id,))
        
        # Eliminar publicación
        cursor.execute("DELETE FROM publicaciones WHERE id = %s", (publicacion_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Publicación eliminada"}), 200
        
    except Exception as e:
        print(f"[PUBLICACIONES] Error al eliminar: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/publicaciones/<int:publicacion_id>/fijar', methods=['POST'])
def fijar_publicacion(publicacion_id):
    """Fija una publicación (marca como destacada)"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión"}), 500
        
        cursor = connection.cursor()
        
        # Actualizar estado de fijación
        cursor.execute("""
            UPDATE publicaciones
            SET fijada = IF(fijada = 1, 0, 1)
            WHERE id = %s
        """, (publicacion_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Publicación actualizada"}), 200
        
    except Exception as e:
        print(f"[PUBLICACIONES] Error al fijar: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/publicaciones/<int:publicacion_id>/denunciar', methods=['POST'])
def denunciar_publicacion(publicacion_id):
    """Denuncia una publicación"""
    try:
        data = request.get_json()
        motivo = data.get('motivo', 'Sin especificar')
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión"}), 500
        
        cursor = connection.cursor()
        
        # Crear tabla de denuncias si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS denuncias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_publicacion INT NOT NULL,
                motivo VARCHAR(255),
                fecha_denuncia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_publicacion) REFERENCES publicaciones(id)
            )
        """)
        
        # Guardar denuncia
        cursor.execute("""
            INSERT INTO denuncias (id_publicacion, motivo)
            VALUES (%s, %s)
        """, (publicacion_id, motivo))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Denuncia registrada"}), 200
        
    except Exception as e:
        print(f"[PUBLICACIONES] Error al denunciar: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/seguir/<int:usuario_id_a_seguir>', methods=['POST'])
def seguir_usuario(usuario_id_a_seguir):
    """Permite que un usuario siga a otro"""
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        
        if not id_usuario or not usuario_id_a_seguir:
            return jsonify({"success": False, "message": "IDs requeridos"}), 400
        
        if id_usuario == usuario_id_a_seguir:
            return jsonify({"success": False, "message": "No puedes seguirte a ti mismo"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO seguimientos (id_usuario, id_seguido)
                VALUES (%s, %s)
            """, (id_usuario, usuario_id_a_seguir))
            connection.commit()
            
            print(f"[SEGUIR] Usuario {id_usuario} ahora sigue a {usuario_id_a_seguir}")
            
            return jsonify({
                "success": True,
                "message": "Usuario seguido correctamente"
            }, 200)
        except Exception as e:
            if "Duplicate entry" in str(e):
                return jsonify({"success": False, "message": "Ya sigues a este usuario"}), 400
            raise
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"[SEGUIR] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/dejar-seguir/<int:usuario_id>', methods=['POST'])
def dejar_seguir_usuario(usuario_id):
    """Permite que un usuario deje de seguir a otro"""
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        
        if not id_usuario or not usuario_id:
            return jsonify({"success": False, "message": "IDs requeridos"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                DELETE FROM seguimientos
                WHERE id_usuario = %s AND id_seguido = %s
            """, (id_usuario, usuario_id))
            connection.commit()
            
            if cursor.rowcount == 0:
                return jsonify({"success": False, "message": "No seguias a este usuario"}), 400
            
            print(f"[DEJAR-SEGUIR] Usuario {id_usuario} dejo de seguir a {usuario_id}")
            
            return jsonify({
                "success": True,
                "message": "Dejas de seguir al usuario"
            }, 200)
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"[DEJAR-SEGUIR] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/verificar-seguimiento/<int:usuario_id>', methods=['GET'])
def verificar_seguimiento(usuario_id):
    """Verifica si un usuario sigue a otro"""
    try:
        id_usuario = request.args.get('id_usuario')
        
        if not id_usuario or not usuario_id:
            return jsonify({"success": False, "message": "IDs requeridos"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id FROM seguimientos
                WHERE id_usuario = %s AND id_seguido = %s
            """, (id_usuario, usuario_id))
            resultado = cursor.fetchone()
            
            return jsonify({
                "success": True,
                "siguiendo": resultado is not None
            }), 200
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"[VERIFICAR-SEGUIMIENTO] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/obtener-seguimientos/<int:usuario_id>', methods=['GET'])
def obtener_seguimientos(usuario_id):
    """Obtiene los usuarios que sigue y sus seguidores"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Usuarios que sigue
            cursor.execute("""
                SELECT u.id, u.nombre, u.imagen_perfil_url
                FROM seguimientos s
                JOIN usuarios u ON s.id_seguido = u.id
                WHERE s.id_usuario = %s
                ORDER BY s.fecha_seguimiento DESC
            """, (usuario_id,))
            siguiendo = cursor.fetchall()
            
            # Seguidores
            cursor.execute("""
                SELECT u.id, u.nombre, u.imagen_perfil_url
                FROM seguimientos s
                JOIN usuarios u ON s.id_usuario = u.id
                WHERE s.id_seguido = %s
                ORDER BY s.fecha_seguimiento DESC
            """, (usuario_id,))
            seguidores = cursor.fetchall()
            
            # Feed personalizado (publicaciones de usuarios que sigue)
            cursor.execute("""
                SELECT p.id, p.titulo, p.contenido, p.fecha_publicacion, u.nombre AS autor, 
                       u.id AS id_autor, u.imagen_perfil_url AS imagen_perfil,
                       (SELECT url FROM imagenes_publicacion WHERE id_publicacion = p.id LIMIT 1) AS imagen_url,
                       (SELECT COUNT(*) FROM reacciones WHERE id_publicacion = p.id) AS total_reacciones
                FROM publicaciones p
                JOIN usuarios u ON p.id_autor = u.id
                WHERE u.id IN (
                    SELECT id_seguido FROM seguimientos WHERE id_usuario = %s
                ) OR u.id = %s
                AND p.estado_aprobacion = 'aprobado'
                ORDER BY p.fecha_publicacion DESC
                LIMIT 50
            """, (usuario_id, usuario_id))
            feed_personalizado = cursor.fetchall()
            
            # Procesar URLs de imágenes en feed
            for pub in feed_personalizado:
                if pub['imagen_url'] and not pub['imagen_url'].startswith('http'):
                    pub['imagen_url'] = f"http://localhost:5000{pub['imagen_url']}"
                if pub['imagen_perfil'] and not pub['imagen_perfil'].startswith('http'):
                    pub['imagen_perfil'] = f"http://localhost:5000{pub['imagen_perfil']}"
            
            return jsonify({
                "success": True,
                "siguiendo": siguiendo,
                "seguidores": seguidores,
                "total_siguiendo": len(siguiendo) if siguiendo else 0,
                "total_seguidores": len(seguidores) if seguidores else 0,
                "feed_personalizado": feed_personalizado
            }), 200
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"[OBTENER-SEGUIMIENTOS] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/sugerencias-seguir/<int:usuario_id>', methods=['GET'])
def obtener_sugerencias_seguir(usuario_id):
    """Obtiene sugerencias de usuarios a seguir"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Usuarios populares que no sigue
            cursor.execute("""
                SELECT u.id, u.nombre, u.imagen_perfil_url,
                       (SELECT COUNT(*) FROM seguimientos WHERE id_seguido = u.id) AS total_seguidores
                FROM usuarios u
                WHERE u.id NOT IN (
                    SELECT id_seguido FROM seguimientos WHERE id_usuario = %s
                ) AND u.id != %s
                ORDER BY total_seguidores DESC
                LIMIT 10
            """, (usuario_id, usuario_id))
            sugerencias = cursor.fetchall()
            
            return jsonify({
                "success": True,
                "sugerencias": sugerencias
            }), 200
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"[SUGERENCIAS-SEGUIR] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/estadisticas-usuario/<int:usuario_id>', methods=['GET'])
def obtener_estadisticas_usuario(usuario_id):
    """Obtiene estadisticas del usuario (seguidores, publicaciones, etc)"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexion a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Total de seguidores
            cursor.execute("""
                SELECT COUNT(*) as total FROM seguimientos WHERE id_seguido = %s
            """, (usuario_id,))
            total_seguidores = cursor.fetchone()['total'] or 0
            
            # Total que sigue
            cursor.execute("""
                SELECT COUNT(*) as total FROM seguimientos WHERE id_usuario = %s
            """, (usuario_id,))
            total_siguiendo = cursor.fetchone()['total'] or 0
            
            # Total publicaciones
            cursor.execute("""
                SELECT COUNT(*) as total FROM publicaciones 
                WHERE id_autor = %s AND estado_aprobacion = 'aprobado'
            """, (usuario_id,))
            total_publicaciones = cursor.fetchone()['total'] or 0
            
            # Total reacciones recibidas
            cursor.execute("""
                SELECT COUNT(*) as total FROM reacciones r
                JOIN publicaciones p ON r.id_publicacion = p.id
                WHERE p.id_autor = %s
            """, (usuario_id,))
            total_reacciones = cursor.fetchone()['total'] or 0
            
            return jsonify({
                "success": True,
                "estadisticas": {
                    "total_seguidores": total_seguidores,
                    "total_siguiendo": total_siguiendo,
                    "total_publicaciones": total_publicaciones,
                    "total_reacciones": total_reacciones
                }
            }), 200
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"[ESTADISTICAS-USUARIO] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

def add_base_url_to_images(data, image_field='imagen_url'):
    """Agrega la URL base a las imágenes si no la tienen"""
    if isinstance(data, dict):
        if image_field in data and data[image_field]:
            if not data[image_field].startswith('http'):
                data[image_field] = f"http://localhost:5000{data[image_field]}"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if image_field in item and item[image_field]:
                    if not item[image_field].startswith('http'):
                        item[image_field] = f"http://localhost:5000{item[image_field]}"
    return data

@app.route('/api/usuarios-disponibles', methods=['GET'])
def obtener_usuarios_disponibles():
    """Obtiene usuarios que se siguen mutuamente con el usuario actual"""
    usuario_id = request.args.get('usuario_id')
    
    if not usuario_id:
        return jsonify({"success": False, "message": "usuario_id requerido"}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        # Obtener usuarios que se siguen mutuamente
        cursor.execute("""
            SELECT DISTINCT u.id, u.nombre, u.imagen_perfil_url
            FROM usuarios u
            WHERE u.id != %s
            AND EXISTS (
                SELECT 1 FROM seguimientos s1 
                WHERE s1.id_usuario = %s AND s1.id_seguido = u.id
            )
            AND EXISTS (
                SELECT 1 FROM seguimientos s2 
                WHERE s2.id_usuario = u.id AND s2.id_seguido = %s
            )
            ORDER BY u.nombre ASC
        """, (usuario_id, usuario_id, usuario_id))
        
        usuarios = cursor.fetchall()
        
        # Procesar URLs de imágenes
        for usuario in usuarios:
            if usuario['imagen_perfil_url'] and not usuario['imagen_perfil_url'].startswith('http'):
                usuario['imagen_perfil_url'] = f"http://localhost:5000{usuario['imagen_perfil_url']}"
        
        return jsonify({"success": True, "usuarios": usuarios}), 200
    except Exception as e:
        print(f"[USUARIOS] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/reacciones/publicacion/<int:publicacion_id>', methods=['GET'])
def obtener_reacciones_publicacion(publicacion_id):
    """Devuelve conteo de reacciones por tipo y (opcional) reacción del usuario"""
    usuario_id = request.args.get('usuario_id')
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT tipo, COUNT(*) as total
            FROM reacciones
            WHERE id_publicacion = %s
            GROUP BY tipo
        """, (publicacion_id,))
        filas = cursor.fetchall()
        conteo = {f['tipo']: f['total'] for f in filas}
        user_reaction = None
        if usuario_id:
            cursor.execute("""
                SELECT tipo FROM reacciones
                WHERE id_publicacion = %s AND id_usuario = %s
                LIMIT 1
            """, (publicacion_id, usuario_id))
            ur = cursor.fetchone()
            if ur:
                user_reaction = ur['tipo']
        cursor.close()
        connection.close()
        return jsonify({"success": True, "conteo": conteo, "user_reaction": user_reaction}), 200
    except Exception as e:
        print(f"[REACCIONES] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/reacciones', methods=['POST'])
def crear_o_toggle_reaccion():
    """Crea o togglea una reacción"""
    try:
        data = request.get_json()
        id_publicacion = data.get('id_publicacion')
        id_usuario = data.get('id_usuario')
        tipo = data.get('tipo')
        if not all([id_publicacion, id_usuario, tipo]):
            return jsonify({"success": False, "message": "Campos requeridos"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, tipo FROM reacciones
            WHERE id_publicacion = %s AND id_usuario = %s
            LIMIT 1
        """, (id_publicacion, id_usuario))
        existente = cursor.fetchone()
        if existente:
            if existente[1] == tipo:
                cursor.execute("DELETE FROM reacciones WHERE id = %s", (existente[0],))
                action = "deleted"
            else:
                cursor.execute("UPDATE reacciones SET tipo = %s, fecha = NOW() WHERE id = %s", (tipo, existente[0]))
                action = "updated"
        else:
            cursor.execute("""
                INSERT INTO reacciones (id_publicacion, id_usuario, tipo, fecha)
                VALUES (%s, %s, %s, NOW())
            """, (id_publicacion, id_usuario, tipo))
            action = "inserted"
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True, "action": action}), 200
    except Exception as e:
        print(f"[REACCIONES-POST] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/comentarios', methods=['POST'])
def crear_comentario():
    """Crea un comentario en una publicación"""
    try:
        data = request.get_json()
        id_publicacion = data.get('id_publicacion')
        id_usuario = data.get('id_usuario')
        comentario = data.get('comentario')
        
        if not all([id_publicacion, id_usuario, comentario]):
            return jsonify({"success": False, "message": "Campos requeridos"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO comentarios (id_publicacion, id_usuario, comentario, fecha)
                VALUES (%s, %s, %s, NOW())
            """, (id_publicacion, id_usuario, comentario))
            connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return jsonify({"success": True, "id": last_id, "message": "Comentario creado"}), 201
        except Exception as e:
            print(f"[COMENTARIOS-POST] Error en BD: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        print(f"[COMENTARIOS-POST] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/comentarios/publicacion/<int:publicacion_id>', methods=['GET'])
def obtener_comentarios_publicacion(publicacion_id):
    """Obtiene todos los comentarios de una publicación"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    c.id, 
                    c.comentario, 
                    c.fecha,
                    u.id AS autor_id, 
                    u.nombre AS autor, 
                    u.imagen_perfil_url
                FROM comentarios c
                JOIN usuarios u ON c.id_usuario = u.id
                WHERE c.id_publicacion = %s
                ORDER BY c.fecha ASC
            """, (publicacion_id,))
            
            comentarios = cursor.fetchall()
            
            # Procesar URLs de imágenes
            for c in comentarios:
                if c['imagen_perfil_url'] and not c['imagen_perfil_url'].startswith('http'):
                    c['imagen_perfil_url'] = f"http://localhost:5000{c['imagen_perfil_url']}"
            
            cursor.close()
            connection.close()
            return jsonify({"success": True, "comentarios": comentarios}), 200
        except Exception as e:
            print(f"[COMENTARIOS-GET] Error en BD: {e}")
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        print(f"[COMENTARIOS-GET] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/comentarios/<int:comentario_id>', methods=['DELETE'])
def eliminar_comentario(comentario_id):
    """Elimina un comentario (solo el autor o admin puede)"""
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        
        if not id_usuario:
            return jsonify({"success": False, "message": "Usuario no identificado"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Verificar que el usuario sea el autor del comentario
            cursor.execute("SELECT id_usuario FROM comentarios WHERE id = %s", (comentario_id,))
            comentario = cursor.fetchone()
            
            if not comentario:
                cursor.close()
                connection.close()
                return jsonify({"success": False, "message": "Comentario no encontrado"}), 404
            
            if comentario['id_usuario'] != int(id_usuario):
                cursor.close()
                connection.close()
                return jsonify({"success": False, "message": "No tienes permiso para eliminar este comentario"}), 403
            
            # Eliminar comentario
            cursor.execute("DELETE FROM comentarios WHERE id = %s", (comentario_id,))
            connection.commit()
            
            cursor.close()
            connection.close()
            return jsonify({"success": True, "message": "Comentario eliminado"}), 200
        except Exception as e:
            print(f"[COMENTARIOS-DELETE] Error en BD: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        print(f"[COMENTARIOS-DELETE] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/comentarios-perfil/<int:id_perfil>', methods=['GET'])
def obtener_comentarios_perfil(id_perfil):
    """Obtiene comentarios del perfil de un usuario"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                cp.id,
                cp.comentario,
                cp.fecha,
                u.id AS autor_id,
                u.nombre AS autor,
                u.imagen_perfil_url
            FROM comentarios_perfil cp
            JOIN usuarios u ON cp.id_usuario_comentario = u.id
            WHERE cp.id_perfil_usuario = %s
            ORDER BY cp.fecha DESC
        """, (id_perfil,))
        
        comentarios = cursor.fetchall()
        
        # Procesar URLs de imágenes
        for c in comentarios:
            if c['imagen_perfil_url'] and not c['imagen_perfil_url'].startswith('http'):
                c['imagen_perfil_url'] = f"http://localhost:5000{c['imagen_perfil_url']}"
        
        cursor.close()
        connection.close()
        return jsonify({"success": True, "comentarios": comentarios}), 200
    except Exception as e:
        print(f"[COMENTARIOS-PERFIL-GET] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/comentarios-perfil', methods=['POST'])
def crear_comentario_perfil():
    """Crea un comentario en el perfil de un usuario"""
    try:
        data = request.get_json()
        id_perfil = data.get('id_perfil_usuario')
        id_usuario = data.get('id_usuario_comentario')
        comentario = data.get('comentario')
        
        if not all([id_perfil, id_usuario, comentario]):
            return jsonify({"success": False, "message": "Campos requeridos"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO comentarios_perfil (id_perfil_usuario, id_usuario_comentario, comentario, fecha)
                VALUES (%s, %s, %s, NOW())
            """, (id_perfil, id_usuario, comentario))
            connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return jsonify({"success": True, "id": last_id, "message": "Comentario creado"}), 201
        except Exception as e:
            print(f"[COMENTARIOS-PERFIL-POST] Error en BD: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        print(f"[COMENTARIOS-PERFIL-POST] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/comentarios-perfil/<int:comentario_id>', methods=['DELETE'])
def eliminar_comentario_perfil(comentario_id):
    """Elimina un comentario del perfil"""
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario_comentario')
        
        if not id_usuario:
            return jsonify({"success": False, "message": "Usuario no identificado"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"success": False, "message": "Error de conexión a la BD"}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Verificar que el usuario sea el autor del comentario
            cursor.execute("SELECT id_usuario_comentario FROM comentarios_perfil WHERE id = %s", (comentario_id,))
            comentario = cursor.fetchone()
            
            if not comentario:
                cursor.close()
                connection.close()
                return jsonify({"success": False, "message": "Comentario no encontrado"}), 404
            
            if comentario['id_usuario_comentario'] != int(id_usuario):
                cursor.close()
                connection.close()
                return jsonify({"success": False, "message": "No tienes permiso para eliminar este comentario"}), 403
            
            # Eliminar comentario
            cursor.execute("DELETE FROM comentarios_perfil WHERE id = %s", (comentario_id,))
            connection.commit()
            
            cursor.close()
            connection.close()
            return jsonify({"success": True, "message": "Comentario eliminado"}), 200
        except Exception as e:
            print(f"[COMENTARIOS-PERFIL-DELETE] Error en BD: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        print(f"[COMENTARIOS-PERFIL-DELETE] Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
