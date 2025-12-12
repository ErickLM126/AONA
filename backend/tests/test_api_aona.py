import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Agregar la carpeta padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_aona import app


class TestApiAona(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	@patch('api_aona.get_db_connection')
	def test_registro_usuario_exitoso(self, mock_db_conn):
		mock_conn = MagicMock()
		mock_cursor = MagicMock()
		mock_db_conn.return_value = mock_conn
		mock_conn.cursor.return_value = mock_cursor

		mock_conn.commit.return_value = None
		mock_cursor.close.return_value = None
		mock_conn.close.return_value = None

		payload = {
			'nombre': 'Test User',
			'usuario': 'testuser',
			'email': 'test@example.com',
			'contacto': '123456789',
			'documento': '999999',
			'contrasena': 'testpass'
		}
		response = self.app.post('/registro', json=payload)
		self.assertEqual(response.status_code, 201)
		data = response.get_json()
		self.assertEqual(data["message"], "Usuario registrado con éxito")
		self.assertTrue(data["success"])

	@patch('api_aona.get_db_connection')
	def test_login_usuario_exitoso(self, mock_db_conn):
		mock_conn = MagicMock()
		mock_cursor = MagicMock()
		mock_db_conn.return_value = mock_conn
		mock_conn.cursor.return_value = mock_cursor

		mock_cursor.fetchone.return_value = {
			'id': 1,
			'nombre': 'Test User',
			'documento': '999999',
			'contrasena': 'testpass'
		}
		mock_cursor.close.return_value = None
		mock_conn.close.return_value = None

		payload = {
			'identificador': '999999',
			'contrasena': 'testpass'
		}
		response = self.app.post('/login', json=payload)
		self.assertEqual(response.status_code, 200)
		data = response.get_json()
		self.assertEqual(data["message"], "Inicio de sesión exitoso")
		self.assertTrue(data["success"])
		self.assertIn("usuario", data)
		self.assertEqual(data["usuario"]["nombre"], "Test User")

	@patch('api_aona.get_db_connection')
	def test_login_usuario_fallido(self, mock_db_conn):
		mock_conn = MagicMock()
		mock_cursor = MagicMock()
		mock_db_conn.return_value = mock_conn
		mock_conn.cursor.return_value = mock_cursor

		mock_cursor.fetchone.return_value = None
		mock_cursor.close.return_value = None
		mock_conn.close.return_value = None

		payload = {
			'identificador': 'noexiste',
			'contrasena': 'incorrecta'
		}
		response = self.app.post('/login', json=payload)
		self.assertEqual(response.status_code, 401)
		data = response.get_json()
		self.assertEqual(data["message"], "Credenciales incorrectas")
		self.assertFalse(data["success"])

if __name__ == '__main__':
	unittest.main()

