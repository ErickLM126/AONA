export async function obtenerProductos() {
  const response = await fetch('http://localhost:5000/api/productos');
  if (!response.ok) throw new Error('Error al obtener productos');
  return response.json();
}