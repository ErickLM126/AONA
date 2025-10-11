export async function obtenerPublicaciones() {
  const res = await fetch("http://localhost:5000/publicaciones");
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