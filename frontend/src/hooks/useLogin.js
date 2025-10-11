import { useState } from "react";
import { loginUsuario } from "../services/registroService";

export function useLogin() {
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  const login = async ({ identificador, contrasena }) => {
    setCargando(true);
    setMensaje("");
    try {
      const data = await loginUsuario({ identificador, contrasena });
      if (data.success) {
        setMensaje("¡Inicio de sesión exitoso! Redirigiendo...");
        return { exito: true, usuario: data.usuario, mensaje: data.message };
      } else {
        setMensaje(data.message || "Credenciales incorrectas.");
        return { exito: false, mensaje: data.message };
      }
    } catch (error) {
      setMensaje("Error de conexión con el servidor.");
      return { exito: false, mensaje: "Error de conexión con el servidor." };
    } finally {
      setCargando(false);
    }
  };

  return { login, mensaje, cargando, setMensaje };
}