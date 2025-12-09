import { useState } from "react";

const API_URL = "http://localhost:5000";

export function usePublicaciones() {
  const [publicaciones, setPublicaciones] = useState([]);
  const [mensaje, setMensaje] = useState("");

  const cargarPublicaciones = async () => {
    try {
      const response = await fetch(`${API_URL}/publicaciones`);
      const data = await response.json();
      if (data.success) {
        setPublicaciones(data.publicaciones);
      }
    } catch (error) {
      console.error("Error al cargar publicaciones:", error);
    }
  };

  const publicar = async ({ usuario, texto, imagen }) => {
    const formData = new FormData();
    formData.append("usuario", usuario);
    formData.append("texto", texto);
    if (imagen) {
      formData.append("imagen", imagen);
    }

    try {
      const response = await fetch(`${API_URL}/publicar`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.success) {
        setMensaje("Publicacion realizada con exito");
        cargarPublicaciones();
        return true;
      } else {
        setMensaje(data.message || "Error al publicar");
        return false;
      }
    } catch (error) {
      setMensaje("Error de conexion");
      console.error("Error:", error);
      return false;
    }
  };

  return {
    publicaciones,
    mensaje,
    setMensaje,
    cargarPublicaciones,
    publicar,
  };
}