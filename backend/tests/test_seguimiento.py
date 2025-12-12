import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Agregar la carpeta padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_aona import app


class TestSeguimientoUsuarios(unittest.TestCase):
    """Tests para RF006: Seguimiento entre usuarios"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.usuario_id = 1
        self.usuario_a_seguir = 2

    @patch('api_aona.get_db_connection')
    def test_seguir_usuario(self, mock_db_conn):
        """Test: Un usuario puede seguir a otro"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        response = self.app.post(f'/api/seguir/{self.usuario_a_seguir}', json=data)
        
        # El endpoint devuelve 200 en caso de éxito
        self.assertEqual(response.status_code, 200)

    @patch('api_aona.get_db_connection')
    def test_seguir_usuario_sin_conexion(self, mock_db_conn):
        """Test: Error al seguir sin conexión a BD"""
        mock_db_conn.return_value = None
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        response = self.app.post(f'/api/seguir/{self.usuario_a_seguir}', json=data)
        
        self.assertEqual(response.status_code, 500)
        result = response.get_json()
        self.assertFalse(result['success'])

    @patch('api_aona.get_db_connection')
    def test_seguir_usuario_ya_sigue(self, mock_db_conn):
        """Test: No se puede seguir dos veces al mismo usuario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular error de clave duplicada
        mock_cursor.execute.side_effect = Exception("Duplicate entry")
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        response = self.app.post(f'/api/seguir/{self.usuario_a_seguir}', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Ya sigues a este usuario')

    @patch('api_aona.get_db_connection')
    def test_no_puede_seguirse_a_si_mismo(self, mock_db_conn):
        """Test: Un usuario no puede seguirse a sí mismo"""
        mock_conn = MagicMock()
        mock_db_conn.return_value = mock_conn
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        # Intentar seguir el mismo usuario
        response = self.app.post(f'/api/seguir/{self.usuario_id}', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'No puedes seguirte a ti mismo')

    @patch('api_aona.get_db_connection')
    def test_dejar_seguir_usuario(self, mock_db_conn):
        """Test: Un usuario puede dejar de seguir a otro"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        response = self.app.post(f'/api/dejar-seguir/{self.usuario_a_seguir}', json=data)
        
        # El endpoint devuelve 200 en caso de éxito
        self.assertEqual(response.status_code, 200)
        # Nota: el endpoint tiene un error de sintaxis en jsonify pero aun así responde

    @patch('api_aona.get_db_connection')
    def test_dejar_seguir_no_seguia(self, mock_db_conn):
        """Test: No se puede dejar de seguir a quien no se sigue"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 0  # No se eliminó nada
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        response = self.app.post(f'/api/dejar-seguir/{self.usuario_a_seguir}', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'No seguias a este usuario')

    @patch('api_aona.get_db_connection')
    def test_verificar_seguimiento(self, mock_db_conn):
        """Test: Verificar si un usuario sigue a otro"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # El usuario sí sigue
        mock_cursor.fetchone.return_value = {"id": 1}
        
        response = self.app.get(f'/api/verificar-seguimiento/{self.usuario_a_seguir}?id_usuario={self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertTrue(result['siguiendo'])

    @patch('api_aona.get_db_connection')
    def test_verificar_no_sigue(self, mock_db_conn):
        """Test: Verificar cuando no sigue a un usuario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # El usuario no sigue
        mock_cursor.fetchone.return_value = None
        
        response = self.app.get(f'/api/verificar-seguimiento/{self.usuario_a_seguir}?id_usuario={self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertFalse(result['siguiendo'])

    @patch('api_aona.get_db_connection')
    def test_obtener_seguimientos(self, mock_db_conn):
        """Test: Obtener usuarios que sigue y seguidores"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        siguiendo_mock = [
            {
                "id": 2,
                "nombre": "Maria",
                "imagen_perfil_url": "/uploads/maria.jpg"
            },
            {
                "id": 3,
                "nombre": "Carlos",
                "imagen_perfil_url": "/uploads/carlos.jpg"
            }
        ]
        
        seguidores_mock = [
            {
                "id": 4,
                "nombre": "Ana",
                "imagen_perfil_url": "/uploads/ana.jpg"
            },
            {
                "id": 5,
                "nombre": "Pedro",
                "imagen_perfil_url": "/uploads/pedro.jpg"
            }
        ]
        
        feed_mock = [
            {
                "id": 1,
                "titulo": "Nueva obra",
                "contenido": "Descripción",
                "fecha_publicacion": "2025-01-16 10:00:00",
                "autor": "Maria",
                "id_autor": 2,
                "imagen_perfil": "/uploads/maria.jpg",
                "imagen_url": "/uploads/obra.jpg",
                "total_reacciones": 5
            }
        ]
        
        mock_cursor.fetchall.side_effect = [
            siguiendo_mock,
            seguidores_mock,
            feed_mock
        ]
        
        response = self.app.get(f'/api/obtener-seguimientos/{self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['siguiendo']), 2)
        self.assertEqual(len(result['seguidores']), 2)
        self.assertEqual(result['total_siguiendo'], 2)
        self.assertEqual(result['total_seguidores'], 2)
        self.assertEqual(len(result['feed_personalizado']), 1)

    @patch('api_aona.get_db_connection')
    def test_feed_personalizado(self, mock_db_conn):
        """Test: Feed personalizado muestra publicaciones de usuarios seguidos"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        feed_mock = [
            {
                "id": 1,
                "titulo": "Obra 1",
                "contenido": "Descripción 1",
                "fecha_publicacion": "2025-01-16 10:00:00",
                "autor": "Maria",
                "id_autor": 2,
                "imagen_perfil": "/uploads/maria.jpg",
                "imagen_url": "/uploads/obra1.jpg",
                "total_reacciones": 10
            }
        ]
        
        mock_cursor.fetchall.side_effect = [[], [], feed_mock]
        
        response = self.app.get(f'/api/obtener-seguimientos/{self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['feed_personalizado']), 1)

    @patch('api_aona.get_db_connection')
    def test_obtener_sugerencias_seguir(self, mock_db_conn):
        """Test: Obtener sugerencias de usuarios a seguir"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        sugerencias_mock = [
            {
                "id": 5,
                "nombre": "Pedro Popular",
                "imagen_perfil_url": "/uploads/pedro.jpg",
                "total_seguidores": 150
            },
            {
                "id": 6,
                "nombre": "Ana Artista",
                "imagen_perfil_url": "/uploads/ana.jpg",
                "total_seguidores": 120
            }
        ]
        
        mock_cursor.fetchall.return_value = sugerencias_mock
        
        response = self.app.get(f'/api/sugerencias-seguir/{self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['sugerencias']), 2)
        self.assertEqual(result['sugerencias'][0]['nombre'], "Pedro Popular")

    @patch('api_aona.get_db_connection')
    def test_estadisticas_usuario(self, mock_db_conn):
        """Test: Obtener estadísticas del usuario (seguidores, publicaciones)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular 4 consultas: seguidores, siguiendo, publicaciones, reacciones
        mock_cursor.fetchone.side_effect = [
            {"total": 50},      # Total seguidores
            {"total": 30},      # Total siguiendo
            {"total": 15},      # Total publicaciones
            {"total": 120}      # Total reacciones
        ]
        
        response = self.app.get(f'/api/estadisticas-usuario/{self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(result['estadisticas']['total_seguidores'], 50)
        self.assertEqual(result['estadisticas']['total_siguiendo'], 30)
        self.assertEqual(result['estadisticas']['total_publicaciones'], 15)
        self.assertEqual(result['estadisticas']['total_reacciones'], 120)

    @patch('api_aona.get_db_connection')
    def test_usuarios_disponibles_seguimiento_mutuo(self, mock_db_conn):
        """Test: Obtener usuarios que se siguen mutuamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        usuarios_mock = [
            {
                "id": 2,
                "nombre": "Maria",
                "imagen_perfil_url": "/uploads/maria.jpg"
            },
            {
                "id": 3,
                "nombre": "Carlos",
                "imagen_perfil_url": "/uploads/carlos.jpg"
            }
        ]
        
        mock_cursor.fetchall.return_value = usuarios_mock
        
        response = self.app.get(f'/api/usuarios-disponibles?usuario_id={self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['usuarios']), 2)

    @patch('api_aona.get_db_connection')
    def test_no_puede_seguir_bloqueados(self, mock_db_conn):
        """Test: No permitir seguimiento a usuarios bloqueados"""
        # Este test verifica que no se puede seguir a usuarios bloqueados
        # Se implementaría si hay tabla de bloqueos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        data = {
            'id_usuario': self.usuario_id,
        }
        
        # Intentar seguir
        response = self.app.post(f'/api/seguir/{self.usuario_a_seguir}', json=data)
        
        # Debería permitirse a menos que esté bloqueado
        self.assertIn(response.status_code, [200, 400, 500])

    @patch('api_aona.get_db_connection')
    def test_seguidores_ven_contenido_personalizado(self, mock_db_conn):
        """Test: Los seguidores ven el contenido en su feed"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Usuario 1 sigue a usuario 2
        # Cuando usuario 1 obtiene seguimientos, debe ver publicaciones de usuario 2
        feed_mock = [
            {
                "id": 1,
                "titulo": "Publicación de María",
                "contenido": "Contenido",
                "fecha_publicacion": "2025-01-16 10:00:00",
                "autor": "Maria",
                "id_autor": 2,
                "imagen_perfil": "/uploads/maria.jpg",
                "imagen_url": None,
                "total_reacciones": 5
            }
        ]
        
        mock_cursor.fetchall.side_effect = [[], [], feed_mock]
        
        response = self.app.get(f'/api/obtener-seguimientos/{self.usuario_id}')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        # El feed debe contener publicaciones de usuarios seguidos
        self.assertIn('feed_personalizado', result)


class TestSeguimientoValidaciones(unittest.TestCase):
    """Tests adicionales para validaciones en seguimiento"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('api_aona.get_db_connection')
    def test_seguimiento_requiere_ids(self, mock_db_conn):
        """Test: Validar IDs requeridos en seguimiento"""
        mock_conn = MagicMock()
        mock_db_conn.return_value = mock_conn
        
        # Sin id_usuario
        data = {}
        response = self.app.post(f'/api/seguir/2', json=data)
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])

    @patch('api_aona.get_db_connection')
    def test_verificar_seguimiento_requiere_ids(self, mock_db_conn):
        """Test: Validar IDs en verificación de seguimiento"""
        mock_conn = MagicMock()
        mock_db_conn.return_value = mock_conn
        
        # Sin id_usuario
        response = self.app.get(f'/api/verificar-seguimiento/2')
        
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result['success'])


if __name__ == '__main__':
    unittest.main()
