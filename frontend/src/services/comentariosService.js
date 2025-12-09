const API = "http://localhost:5000/api";

export async function getComentariosByPublicacion(id_publicacion) {
  try {
    const res = await fetch(`${API}/comentarios/publicacion/${id_publicacion}`);
    return res.ok ? res.json() : { success: false, comentarios: [] };
  } catch (e) {
    console.error("[COMENTARIOS-GET] Error:", e);
    return { success: false, comentarios: [] };
  }
}

export async function postComentario(payload) {
  try {
    const res = await fetch(`${API}/comentarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return res.ok ? res.json() : { success: false };
  } catch (e) {
    console.error("[COMENTARIOS-POST] Error:", e);
    return { success: false };
  }
}

export async function deleteComentario(comentario_id, id_usuario) {
  try {
    const res = await fetch(`${API}/comentarios/${comentario_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_usuario }),
    });
    return res.ok ? res.json() : { success: false };
  } catch (e) {
    console.error("[COMENTARIOS-DELETE] Error:", e);
    return { success: false };
  }
}