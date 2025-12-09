const API = "http://localhost:5000/api";

export async function getComentariosPerfil(id_perfil) {
  try {
    const res = await fetch(`${API}/comentarios-perfil/${id_perfil}`);
    return res.ok ? res.json() : { success: false, comentarios: [] };
  } catch (e) {
    console.error("[COMENTARIOS-PERFIL-GET] Error:", e);
    return { success: false, comentarios: [] };
  }
}

export async function postComentarioPerfil(payload) {
  try {
    const res = await fetch(`${API}/comentarios-perfil`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return res.ok ? res.json() : { success: false };
  } catch (e) {
    console.error("[COMENTARIOS-PERFIL-POST] Error:", e);
    return { success: false };
  }
}

export async function deleteComentarioPerfil(comentario_id, id_usuario_comentario) {
  try {
    const res = await fetch(`${API}/comentarios-perfil/${comentario_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_usuario_comentario }),
    });
    return res.ok ? res.json() : { success: false };
  } catch (e) {
    console.error("[COMENTARIOS-PERFIL-DELETE] Error:", e);
    return { success: false };
  }
}