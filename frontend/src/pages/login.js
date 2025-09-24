import React, { useState } from "react";
import "../services/styles/login.css";

function Login() {
  const [documento, setDocumento] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [mensaje, setMensaje] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (documento === "" || contrasena === "") {
      setMensaje("Por favor completa todos los campos.");
    } else {
      setMensaje("Intentando iniciar sesión...");
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
            <p className="form-subtitle">Ingresa con tu documento y contraseña</p>

            <div className="input-group">
              <input
                type="text"
                id="login-documento"
                placeholder="Documento"
                value={documento}
                onChange={(e) => setDocumento(e.target.value)}
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
