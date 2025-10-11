import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../services/styles/register.css";
import { useRegistro } from "../hooks/useRegistro";

function Registro() {
  const [nombre, setNombre] = useState("");
  const [usuario, setUsuario] = useState("");
  const [email, setEmail] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [contacto, setContacto] = useState("");
  const [documento, setDocumento] = useState("");
  const [idRol, setIdRol] = useState(1); // Por defecto 1
  const navigate = useNavigate();
  const { registrar, mensaje, cargando, setMensaje } = useRegistro();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    const res = await registrar({
      nombre,
      usuario,
      email,
      contrasena,
      contacto,
      documento,
      id_rol: idRol,
    });
    if (res.exito) {
      setTimeout(() => {
        navigate("/login");
      }, 1200);
    }
  };

  return (
    <div className="main-content">
      <div className="background-image"></div>
      <div className="content-overlay">
        <header className="header">
          <a href="/" className="nav-button">
            Inicio
          </a>
          <a href="/login" className="nav-button">
            Iniciar sesión
          </a>
        </header>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-title">Crear cuenta</div>
          <div className="form-subtitle">¡Únete a nuestra comunidad!</div>
          <div className="input-group">
            <input
              type="text"
              placeholder="Nombre"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="text"
              placeholder="Usuario"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="password"
              placeholder="Contraseña"
              value={contrasena}
              onChange={(e) => setContrasena(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="number"
              placeholder="Número de contacto"
              value={contacto}
              onChange={(e) => setContacto(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="number"
              placeholder="Documento"
              value={documento}
              onChange={(e) => setDocumento(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <input
              type="number"
              placeholder="ID Rol"
              value={idRol}
              onChange={(e) => setIdRol(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="create-account-btn" disabled={cargando}>
            {cargando ? "Registrando..." : "Crear cuenta"}
          </button>
          {mensaje && (
            <div style={{ marginTop: "1em", color: "#EB4335" }}>{mensaje}</div>
          )}
          <div className="separator">o</div>
          <button type="button" className="google-login-btn">
            <span className="btn-text">Registrarse con Google</span>
          </button>
          <div className="terms-text">
            Al registrarte, aceptas nuestros{" "}
            <a href="/terminos" style={{ color: "#EB4335" }}>
              Términos
            </a>{" "}
            y{" "}
            <a href="/privacidad" style={{ color: "#EB4335" }}>
              Política de Privacidad
            </a>
            .
          </div>
        </form>
      </div>
    </div>
  );
}

export default Registro;
