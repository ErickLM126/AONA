import { useState } from "react";
import { obtenerPublicaciones, publicarContenido } from "../services/publicacionesService";

export function usePublicaciones() {
  const [publicaciones, setPublicaciones] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  const cargarPublicaciones = async () => {
    setCargando(true);
    try {
      const data = await obtenerPublicaciones();
      if (data.success) setPublicaciones(data.publicaciones);
    } catch {
      setMensaje("Error al cargar publicaciones");
    } finally {
      setCargando(false);
    }
  };

  const publicar = async ({ usuario, texto, imagen }) => {
    setCargando(true);
    setMensaje("");
    try {
      const data = await publicarContenido({ usuario, texto, imagen });
      if (data.success) {
        setMensaje("¡Publicación subida!");
        await cargarPublicaciones();
      } else {
        setMensaje(data.message || "Error al publicar.");
      }
    } catch {
      setMensaje("Error de conexión.");
    } finally {
      setCargando(false);
    }
  };

  return {
    publicaciones,
    mensaje,
    cargando,
    setMensaje,
    cargarPublicaciones,
    publicar,
    setPublicaciones,
  };
}