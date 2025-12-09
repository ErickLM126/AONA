const API = "http://localhost:5000/api";

export async function reportPublicacion(id_publicacion, payload) {
  const res = await fetch(`${API}/publicaciones/${id_publicacion}/denunciar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.ok ? res.json() : { success: false };
}