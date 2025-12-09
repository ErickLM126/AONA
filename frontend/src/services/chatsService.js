const API_URL = "http://localhost:5000/api/chats";

export const getChats = async (userId) => {
  try {
    const response = await fetch(`${API_URL}?usuario_id=${userId}`);
    if (!response.ok) throw new Error("Error al obtener chats");
    return await response.json();
  } catch (error) {
    console.error("Error en getChats:", error);
    throw error;
  }
};

export const getMessages = async (userId, otroUsuarioId) => {
  try {
    const response = await fetch(
      `${API_URL}/mensajes?usuario1=${userId}&usuario2=${otroUsuarioId}`
    );
    if (!response.ok) throw new Error("Error al obtener mensajes");
    return await response.json();
  } catch (error) {
    console.error("Error en getMessages:", error);
    throw error;
  }
};

export const enviarMensaje = async (idEmisor, idReceptor, mensaje) => {
  try {
    const response = await fetch(`${API_URL}/enviar`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id_emisor: idEmisor,
        id_receptor: idReceptor,
        mensaje: mensaje,
      }),
    });
    if (!response.ok) throw new Error("Error al enviar mensaje");
    return await response.json();
  } catch (error) {
    console.error("Error en enviarMensaje:", error);
    throw error;
  }
};

export const buscarChats = async (userId, termino) => {
  try {
    const response = await fetch(
      `${API_URL}/buscar?usuario_id=${userId}&termino=${encodeURIComponent(
        termino
      )}`
    );
    if (!response.ok) throw new Error("Error al buscar chats");
    return await response.json();
  } catch (error) {
    console.error("Error en buscarChats:", error);
    throw error;
  }
};

export const obtenerUsuariosDisponibles = async (userId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/usuarios-disponibles?usuario_id=${userId}`);
    if (!response.ok) throw new Error("Error al obtener usuarios disponibles");
    return await response.json();
  } catch (error) {
    console.error("Error en obtenerUsuariosDisponibles:", error);
    throw error;
  }
};