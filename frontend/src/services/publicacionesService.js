const API_URL = "http://localhost:5000/api/publicaciones";

export async function obtenerPublicaciones() {
  const res = await fetch(API_URL);
  return res.json();
}

export async function publicarContenido({ usuario, texto, imagen }) {
  const formData = new FormData();
  formData.append("usuario", usuario);
  formData.append("texto", texto);
  if (imagen) formData.append("imagen", imagen);

  const response = await fetch("http://localhost:5000/publicar", {
    method: "POST",
    body: formData,
  });
  return response.json();
}

export const editarPublicacion = async (idPublicacion, datos) => {
  try {
    console.log(`[PUBLICACIONES] Editando publicación ${idPublicacion}`);
    const formData = new FormData();
    formData.append("titulo", datos.titulo);
    formData.append("contenido", datos.contenido);
    if (datos.imagen) {
      formData.append("imagen", datos.imagen);
    }

    const response = await fetch(`${API_URL}/${idPublicacion}`, {
      method: "PUT",
      body: formData,
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("[PUBLICACIONES] Error al editar:", error);
    throw error;
  }
};

export const eliminarPublicacion = async (idPublicacion) => {
  try {
    console.log(`[PUBLICACIONES] Eliminando publicación ${idPublicacion}`);
    const response = await fetch(`${API_URL}/${idPublicacion}`, {
      method: "DELETE",
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("[PUBLICACIONES] Error al eliminar:", error);
    throw error;
  }
};

export const fijarPublicacion = async (idPublicacion) => {
  try {
    console.log(`[PUBLICACIONES] Fijando publicación ${idPublicacion}`);
    const response = await fetch(`${API_URL}/${idPublicacion}/fijar`, {
      method: "POST",
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("[PUBLICACIONES] Error al fijar:", error);
    throw error;
  }
};

export const denunciarPublicacion = async (idPublicacion, motivo) => {
  try {
    console.log(`[PUBLICACIONES] Denunciando publicación ${idPublicacion}`);
    const response = await fetch(`${API_URL}/${idPublicacion}/denunciar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ motivo }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("[PUBLICACIONES] Error al denunciar:", error);
    throw error;
  }
};