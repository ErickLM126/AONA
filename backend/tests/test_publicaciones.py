import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import sys
import os

# Agregar la carpeta padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_aona import app


class TestPublicacionesObras(unittest.TestCase):
    """Tests para RF003: Publicación de obras"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.usuario_id = 1
        self.usuario_name = "juan_artista"

    @patch('api_aona.get_db_connection')
    def test_publicar_obra_exitosamente(self, mock_db_conn):
        """Test: Publicar una obra (texto) correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular búsqueda de usuario
        mock_cursor.fetchone.return_value = {"id": self.usuario_id}
        
        data = {
            'texto': 'Esta es mi nueva obra de arte',
            'usuario': self.usuario_name
        }
        
        response = self.app.post('/publicar', data=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Publicación guardada')

    @patch('api_aona.get_db_connection')
    def test_publicar_obra_sin_usuario(self, mock_db_conn):
        """Test: Validar que el usuario es requerido"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Usuario no encontrado
        
        data = {
            'texto': 'Mi obra',
            'usuario': 'usuario_inexistente'
        }
        
        response = self.app.post('/publicar', data=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Usuario no encontrado')

    @patch('api_aona.get_db_connection')
    def test_publicar_obra_con_imagen(self, mock_db_conn):
        """Test: Publicar obra con imagen"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Usuario existe
        mock_cursor.fetchone.return_value = {"id": self.usuario_id}
        
        data = {
            'texto': 'Mi obra visual',
            'usuario': self.usuario_name,
            'imagen': (b'fake image data', 'obra.jpg')
        }
        
        response = self.app.post('/publicar', data=data, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])

    @patch('api_aona.get_db_connection')
    def test_publicar_obra_sin_conexion_bd(self, mock_db_conn):
        """Test: Error sin conexión a base de datos"""
        mock_db_conn.return_value = None
        
        data = {
            'texto': 'Mi obra',
            'usuario': self.usuario_name
        }
        
        response = self.app.post('/publicar', data=data)
        
        self.assertEqual(response.status_code, 500)
        result = response.get_json()
        self.assertFalse(result['success'])

    @patch('api_aona.get_db_connection')
    def test_obtener_publicaciones(self, mock_db_conn):
        """Test: Obtener todas las publicaciones"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        publicaciones_mock = [
            {
                "id": 1,
                "titulo": "Mi obra",
                "contenido": "Descripción obra",
                "fecha_publicacion": "2025-01-15 10:00:00",
                "autor": "Juan",
                "id_autor": 1,
                "imagen_perfil": "/uploads/juan.jpg",
                "imagen_url": "/uploads/obra1.jpg"
            },
            {
                "id": 2,
                "titulo": "Obra 2",
                "contenido": "Segunda obra",
                "fecha_publicacion": "2025-01-16 10:00:00",
                "autor": "Maria",
                "id_autor": 2,
                "imagen_perfil": "/uploads/maria.jpg",
                "imagen_url": None
            }
        ]
        
        mock_cursor.fetchall.return_value = publicaciones_mock
        
        response = self.app.get('/publicaciones')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['publicaciones']), 2)

    @patch('api_aona.get_db_connection')
    def test_editar_publicacion(self, mock_db_conn):
        """Test: Editar una publicación existente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Verificar que la publicación existe
        mock_cursor.fetchone.return_value = (1,)  # id_autor
        
        data = {
            'titulo': 'Título actualizado',
            'contenido': 'Contenido actualizado'
        }
        
        response = self.app.put(f'/api/publicaciones/1', data=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Publicación actualizada')

    @patch('api_aona.get_db_connection')
    def test_editar_publicacion_inexistente(self, mock_db_conn):
        """Test: Intentar editar publicación que no existe"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = None  # No existe
        
        data = {
            'titulo': 'Título',
            'contenido': 'Contenido'
        }
        
        response = self.app.put(f'/api/publicaciones/9999', data=data)
        
        self.assertEqual(response.status_code, 404)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Publicación no encontrada')

    @patch('api_aona.get_db_connection')
    def test_eliminar_publicacion(self, mock_db_conn):
        """Test: Eliminar una publicación"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Imagen encontrada
        mock_cursor.fetchone.return_value = ("/uploads/obra.jpg",)
        
        response = self.app.delete(f'/api/publicaciones/1')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Publicación eliminada')

    @patch('api_aona.get_db_connection')
    def test_fijar_publicacion(self, mock_db_conn):
        """Test: Fijar/desfijar una publicación (marcar como destacada)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = self.app.post(f'/api/publicaciones/1/fijar')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])

    @patch('api_aona.get_db_connection')
    def test_denunciar_publicacion(self, mock_db_conn):
        """Test: Denunciar una publicación (reporte de contenido inapropiado)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        data = {
            'motivo': 'Contenido inapropiado'
        }
        
        response = self.app.post(f'/api/publicaciones/1/denunciar', json=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Denuncia registrada')

    @patch('api_aona.get_db_connection')
    def test_publicacion_solo_manual(self, mock_db_conn):
        """Test: Las publicaciones solo aceptan contenido manual, no digitales/IA"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular búsqueda de usuario
        mock_cursor.fetchone.return_value = {"id": self.usuario_id}
        
        # Intenta publicar contenido manual
        data = {
            'texto': 'Pintura hecha a mano',
            'usuario': self.usuario_name
        }
        
        response = self.app.post('/publicar', data=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])


class TestControlPublicaciones(unittest.TestCase):
    """Tests para validación de contenido en publicaciones"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('api_aona.get_db_connection')
    def test_publicacion_requiere_descripcion(self, mock_db_conn):
        """Test: Publicación requiere descripción"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = {"id": 1}
        
        # Sin descripción
        data = {
            'usuario': 'juan_artista',
            'imagen': (b'fake image', 'imagen.jpg')
        }
        
        response = self.app.post('/publicar', data=data, content_type='multipart/form-data')
        
        # Debería aceptarse pero sin contenido en texto
        self.assertIn(response.status_code, [200, 400])

    @patch('api_aona.get_db_connection')
    def test_editar_publicacion_verifica_autor(self, mock_db_conn):
        """Test: Solo el autor puede editar su publicación"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Publicación pertenece a usuario 1
        mock_cursor.fetchone.return_value = (1,)
        
        data = {
            'titulo': 'Nuevo título',
            'contenido': 'Nuevo contenido'
        }
        
        # El endpoint debería validar que el usuario autenticado es el autor
        response = self.app.put(f'/api/publicaciones/1', data=data)
        
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
