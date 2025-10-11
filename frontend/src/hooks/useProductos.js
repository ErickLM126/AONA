import { useState, useEffect } from 'react';
import { obtenerProductos } from '../services/productosService';

export function useProductos() {
  const [productos, setProductos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    obtenerProductos()
      .then(setProductos)
      .catch((e) => setError(e.message || 'Error desconocido'))
      .finally(() => setCargando(false));
  }, []);

  return { productos, cargando, error };
}