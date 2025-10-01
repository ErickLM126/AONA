import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../services/styles/login.css";

function Login() {
  const [identificador, setIdentificador] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [mensaje, setMensaje] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    if (identificador === "" || contrasena === "") {
      setMensaje("Por favor completa todos los campos.");
      return;
    }
    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identificador, contrasena }),
      });
      const data = await response.json();
      if (response.ok && data.success) {
        if (data.usuario && data.usuario.nombre) {
          localStorage.setItem("nombreUsuario", data.usuario.nombre);
        }
        setMensaje("¡Inicio de sesión exitoso! Redirigiendo...");
        setTimeout(() => {
          navigate("/home");
        }, 1200);
      } else {
        setMensaje(data.message || "Credenciales incorrectas.");
      }
    } catch (error) {
      setMensaje("Error de conexión con el servidor.");
    }
  };

  return (
    <>
      <div className="background-image"></div>
      <header className="header">
        <a href="/register" className="nav-button">Registrarse</a>
      </header>
      <main className="main-content">
        <div className="content-overlay">
          <form id="login-form" className="login-form" onSubmit={handleSubmit}>
            <h2 className="form-title">Iniciar Sesión</h2>
            <p className="form-subtitle">Ingresa tu nombre de usuario o documento y contraseña</p>
            <div className="input-group">
              <input
                type="text"
                id="login-identificador"
                placeholder="Nombre de usuario o Documento"
                value={identificador}
                onChange={(e) => setIdentificador(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="password"
                id="login-contrasena"
                placeholder="Contraseña"
                value={contrasena}
                onChange={(e) => setContrasena(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="create-account-btn">
              Iniciar Sesión
            </button>
            <p className="separator"><span>o continúa con</span></p>
            <button type="button" className="google-login-btn">
              <p className="btn-text">Iniciar Sesión con Google</p>
            </button>
            <p className="terms-text">
              Al hacer clic en continuar, aceptas nuestros{" "}
              <a href="/terminos">Términos de servicio</a> y{" "}
              <a href="/privacidad">Política de privacidad</a>.
            </p>
            <p id="loginMessage">{mensaje}</p>
          </form>
        </div>
      </main>
    </>
  );
}

export default Login;
