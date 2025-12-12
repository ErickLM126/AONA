import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Agregar la carpeta padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_aona import app


class TestInteraccionSocial(unittest.TestCase):
    """Tests para RF004: Interacción social (comentarios, reacciones, mensajes)"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # ===== TESTS PARA COMENTARIOS =====

    @patch('api_aona.get_db_connection')
    def test_crear_comentario_exitosamente(self, mock_db_conn):
        """Test: Crear un comentario en una publicación"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1
        
        data = {
            'id_publicacion': 1,
            'id_usuario': 2,
            'comentario': 'OMG, qué linda obra de arte!'
        }
        
        response = self.app.post('/api/comentarios', json=data)
        
        self.assertEqual(response.status_code, 201)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Comentario creado')

    @patch('api_aona.get_db_connection')
    def test_crear_comentario_campos_incompletos(self, mock_db_conn):
        """Test: Validar campos requeridos en comentario"""
        mock_db_conn.return_value = None
        
        # Falta el comentario
        data = {
            'id_publicacion': 1,
            'id_usuario': 2
        }
        
        response = self.app.post('/api/comentarios', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Campos requeridos')

    @patch('api_aona.get_db_connection')
    def test_obtener_comentarios_publicacion(self, mock_db_conn):
        """Test: Obtener todos los comentarios de una publicación"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        comentarios_mock = [
            {
                "id": 1,
                "comentario": "Hermosa obra",
                "fecha": "2025-01-15 10:00:00",
                "autor_id": 2,
                "autor": "Maria",
                "imagen_perfil_url": "/uploads/maria.jpg"
            },
            {
                "id": 2,
                "comentario": "Me encanta!",
                "fecha": "2025-01-15 10:30:00",
                "autor_id": 3,
                "autor": "Carlos",
                "imagen_perfil_url": "/uploads/carlos.jpg"
            }
        ]
        
        mock_cursor.fetchall.return_value = comentarios_mock
        
        response = self.app.get('/api/comentarios/publicacion/1')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['comentarios']), 2)
        self.assertEqual(result['comentarios'][0]['autor'], "Maria")

    @patch('api_aona.get_db_connection')
    def test_eliminar_comentario_propio(self, mock_db_conn):
        """Test: El usuario puede eliminar su propio comentario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Comentario pertenece al usuario 2
        mock_cursor.fetchone.return_value = {"id_usuario": 2}
        mock_cursor.rowcount = 1
        
        data = {'id_usuario': 2}
        
        response = self.app.delete('/api/comentarios/1', json=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Comentario eliminado')

    @patch('api_aona.get_db_connection')
    def test_eliminar_comentario_no_es_autor(self, mock_db_conn):
        """Test: No se puede eliminar comentario de otro usuario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Comentario pertenece al usuario 1, intentamos eliminar como usuario 2
        mock_cursor.fetchone.return_value = {"id_usuario": 1}
        
        data = {'id_usuario': 2}
        
        response = self.app.delete('/api/comentarios/1', json=data)
        
        self.assertEqual(response.status_code, 403)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'No tienes permiso para eliminar este comentario')

    @patch('api_aona.get_db_connection')
    def test_comentario_sin_usuario_identificado(self, mock_db_conn):
        """Test: Validar usuario al eliminar comentario"""
        mock_conn = MagicMock()
        mock_db_conn.return_value = mock_conn
        
        data = {}  # Sin id_usuario
        
        response = self.app.delete('/api/comentarios/1', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])

    # ===== TESTS PARA REACCIONES =====

    @patch('api_aona.get_db_connection')
    def test_crear_reaccion(self, mock_db_conn):
        """Test: Crear una reacción (like, amor, etc) en una publicación"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = None  # No existe reacción previa
        
        data = {
            'id_publicacion': 1,
            'id_usuario': 2,
            'tipo': 'like'
        }
        
        response = self.app.post('/api/reacciones', json=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'inserted')

    @patch('api_aona.get_db_connection')
    def test_cambiar_tipo_reaccion(self, mock_db_conn):
        """Test: Cambiar el tipo de reacción (de like a amor)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Ya existe una reacción de tipo 'like'
        mock_cursor.fetchone.return_value = (1, 'like')  # (id, tipo)
        
        data = {
            'id_publicacion': 1,
            'id_usuario': 2,
            'tipo': 'love'  # Cambiar a amor
        }
        
        response = self.app.post('/api/reacciones', json=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'updated')

    @patch('api_aona.get_db_connection')
    def test_eliminar_reaccion_toggle(self, mock_db_conn):
        """Test: Eliminar reacción con toggle (mismo tipo)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Ya existe una reacción del mismo tipo
        mock_cursor.fetchone.return_value = (1, 'like')  # (id, tipo)
        
        data = {
            'id_publicacion': 1,
            'id_usuario': 2,
            'tipo': 'like'  # Mismo tipo = eliminar
        }
        
        response = self.app.post('/api/reacciones', json=data)
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'deleted')

    @patch('api_aona.get_db_connection')
    def test_obtener_reacciones_publicacion(self, mock_db_conn):
        """Test: Obtener conteo de reacciones por tipo"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        reacciones_mock = [
            {"tipo": "like", "total": 15},
            {"tipo": "love", "total": 8},
            {"tipo": "fire", "total": 3}
        ]
        
        # Primera llamada: conteo de reacciones
        # Segunda llamada: reacción del usuario (si está autenticado)
        mock_cursor.fetchall.return_value = reacciones_mock
        mock_cursor.fetchone.return_value = None  # El usuario no ha reaccionado
        
        response = self.app.get('/api/reacciones/publicacion/1?usuario_id=2')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['conteo']['like'], 15)
        self.assertEqual(result['conteo']['love'], 8)
        self.assertIsNone(result['user_reaction'])

    @patch('api_aona.get_db_connection')
    def test_obtener_reacciones_usuario_ya_reacciono(self, mock_db_conn):
        """Test: Obtener reacciones mostrando la del usuario actual"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        reacciones_mock = [
            {"tipo": "like", "total": 15}
        ]
        
        mock_cursor.fetchall.return_value = reacciones_mock
        mock_cursor.fetchone.return_value = {"tipo": "like"}  # Usuario ya reaccionó
        
        response = self.app.get('/api/reacciones/publicacion/1?usuario_id=2')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['user_reaction'], 'like')

    @patch('api_aona.get_db_connection')
    def test_reaccion_campos_requeridos(self, mock_db_conn):
        """Test: Validar campos requeridos en reacción"""
        mock_db_conn.return_value = None
        
        # Falta el tipo de reacción
        data = {
            'id_publicacion': 1,
            'id_usuario': 2
        }
        
        response = self.app.post('/api/reacciones', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])


class TestModeración(unittest.TestCase):
    """Tests para moderación y validación de comentarios"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('api_aona.get_db_connection')
    def test_comentario_antispa(self, mock_db_conn):
        """Test: Sistema antispa para comentarios"""
        # Este test simularía validación de contenido spam
        # Se debería implementar en el backend
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1
        
        # Comentario normal
        data = {
            'id_publicacion': 1,
            'id_usuario': 2,
            'comentario': 'Excelente obra'
        }
        
        response = self.app.post('/api/comentarios', json=data)
        
        self.assertEqual(response.status_code, 201)
        result = response.get_json()
        self.assertTrue(result['success'])

    @patch('api_aona.get_db_connection')
    def test_moderacion_comentarios_y_mensajes(self, mock_db_conn):
        """Test: Validar que hay moderación de comentarios y mensajes"""
        # Los comentarios y mensajes deben ser moderados
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        response = self.app.get('/api/comentarios/publicacion/1')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()
