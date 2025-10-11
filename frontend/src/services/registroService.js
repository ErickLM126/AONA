export async function registrarUsuario(datos) {
  const response = await fetch("http://localhost:5000/registro", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  return response.json();
}

export async function loginUsuario({ identificador, contrasena }) {
  const response = await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identificador, contrasena }),
  });
  return response.json();
}