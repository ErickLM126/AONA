const API_URL = "http://localhost:5000/api/perfil";
const API_BASE = "http://localhost:5000/api";

export const obtenerPerfil = async (usuarioId) => {
  try {
    console.log(`[PERFIL] Obteniendo perfil para usuario ID: ${usuarioId}`);
    const response = await fetch(`${API_URL}/${usuarioId}`);
    
    if (!response.ok) {
      throw new Error(`Error ${response.status} al obtener el perfil`);
    }
    
    const data = await response.json();
    console.log("[PERFIL] Datos obtenidos:", data);
    return data;
  } catch (error) {
    console.error("[PERFIL] Error en obtenerPerfil:", error);
    throw error;
  }
};

export const actualizarPerfil = async (usuarioId, datos) => {
  try {
    console.log(`[PERFIL] Actualizando perfil para usuario ID: ${usuarioId}`);
    
    const formData = new FormData();
    formData.append('nombre', datos.nombre);
    if (datos.imagen) {
      formData.append('imagen', datos.imagen);
      console.log(`[PERFIL] Imagen adjunta: ${datos.imagen.name}`);
    }
    
    const response = await fetch(`${API_URL}/${usuarioId}`, {
      method: 'PUT',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status} al actualizar el perfil`);
    }
    
    const data = await response.json();
    console.log("[PERFIL] Perfil actualizado:", data);
    return data;
  } catch (error) {
    console.error("[PERFIL] Error en actualizarPerfil:", error);
    throw error;
  }
};

export const seguirUsuario = async (idUsuario, idUsuarioASeguir) => {
  try {
    console.log(`[SEGUIMIENTO] Usuario ${idUsuario} siguiendo a ${idUsuarioASeguir}`);
    const response = await fetch(`${API_BASE}/seguir/${idUsuarioASeguir}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_usuario: idUsuario })
    });
    const data = await response.json();
    console.log("[SEGUIMIENTO] Respuesta:", data);
    return data;
  } catch (error) {
    console.error("[SEGUIMIENTO] Error al seguir:", error);
    throw error;
  }
};

export const dejarSeguir = async (idUsuario, idUsuario2) => {
  try {
    console.log(`[SEGUIMIENTO] Usuario ${idUsuario} dejando de seguir a ${idUsuario2}`);
    const response = await fetch(`${API_BASE}/dejar-seguir/${idUsuario2}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_usuario: idUsuario })
    });
    const data = await response.json();
    console.log("[SEGUIMIENTO] Respuesta:", data);
    return data;
  } catch (error) {
    console.error("[SEGUIMIENTO] Error al dejar de seguir:", error);
    throw error;
  }
};

export const verificarSeguimiento = async (idUsuario, idUsuario2) => {
  try {
    const response = await fetch(`${API_BASE}/verificar-seguimiento/${idUsuario2}?id_usuario=${idUsuario}`);
    return await response.json();
  } catch (error) {
    console.error("[SEGUIMIENTO] Error al verificar:", error);
    throw error;
  }
};

export const obtenerSeguimientos = async (idUsuario) => {
  try {
    const response = await fetch(`${API_BASE}/obtener-seguimientos/${idUsuario}`);
    return await response.json();
  } catch (error) {
    console.error("[SEGUIMIENTO] Error al obtener:", error);
    throw error;
  }
};

export const obtenerSugerencias = async (idUsuario) => {
  try {
    const response = await fetch(`${API_BASE}/sugerencias-seguir/${idUsuario}`);
    return await response.json();
  } catch (error) {
    console.error("[SUGERENCIAS] Error:", error);
    throw error;
  }
};

export const obtenerEstadisticas = async (idUsuario) => {
  try {
    const response = await fetch(`${API_BASE}/estadisticas-usuario/${idUsuario}`);
    return await response.json();
  } catch (error) {
    console.error("[ESTADISTICAS] Error:", error);
    throw error;
  }
};

export const editarPublicacion = async (idPublicacion, datos) => {
  try {
    console.log(`[PUBLICACIONES] Editando publicación ${idPublicacion}`);
    const formData = new FormData();
    formData.append('titulo', datos.titulo);
    formData.append('contenido', datos.contenido);
    if (datos.imagen) {
      formData.append('imagen', datos.imagen);
    }
    
    const response = await fetch(`http://localhost:5000/api/publicaciones/${idPublicacion}`, {
      method: 'PUT',
      body: formData
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
    const response = await fetch(`http://localhost:5000/api/publicaciones/${idPublicacion}`, {
      method: 'DELETE'
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
    const response = await fetch(`http://localhost:5000/api/publicaciones/${idPublicacion}/fijar`, {
      method: 'POST'
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
    const response = await fetch(`http://localhost:5000/api/publicaciones/${idPublicacion}/denunciar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ motivo })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("[PUBLICACIONES] Error al denunciar:", error);
    throw error;
  }
};