import { useState } from "react";
import { registrarUsuario } from "../services/registroService";

export function useRegistro() {
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  const registrar = async (datos) => {
    setCargando(true);
    setMensaje("");
    try {
      const data = await registrarUsuario(datos);
      if (data.success) {
        setMensaje("¡Registro exitoso! Redirigiendo...");
        return { exito: true, mensaje: data.message };
      } else {
        setMensaje(data.message || "Error en el registro");
        return { exito: false, mensaje: data.message };
      }
    } catch (error) {
      setMensaje("Error de conexión con el servidor");
      return { exito: false, mensaje: "Error de conexión con el servidor" };
    } finally {
      setCargando(false);
    }
  };

  return { registrar, mensaje, cargando, setMensaje };
}