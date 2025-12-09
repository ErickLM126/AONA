const API = "http://localhost:5000/api";

export async function getReaccionesByPublicacion(id_publicacion, usuario_id = null) {
  const url = usuario_id
    ? `${API}/reacciones/publicacion/${id_publicacion}?usuario_id=${usuario_id}`
    : `${API}/reacciones/publicacion/${id_publicacion}`;
  const res = await fetch(url);
  return res.ok ? res.json() : { success: false };
}

export async function postReaccion(payload) {
  const res = await fetch("http://localhost:5000/api/reacciones", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.ok ? res.json() : { success: false };
}