import React from "react";

const Registro = () => {
  return (
    <div className="registro-page">
      <div className="background-container"></div>

      <div className="main-title">
        Harmonics Of <br /> Natural Art
      </div>

      <nav className="top-nav">
        <a href="/login" className="nav-btn">
          Inicio Sesión
        </a>
      </nav>

      <div className="form-wrapper">
        <form id="create-account-form" className="login-form">
          <h2 className="form-title">Crear una cuenta</h2>
          <p className="form-subtitle">Entra de manera gratuita con tu E-mail</p>

          <div className="input-group">
            <input type="text" id="nombre" placeholder="Nombre completo" required />
          </div>

          <div className="input-group">
            <input type="text" id="contacto" placeholder="Número de contacto" required />
          </div>

          <div className="input-group">
            <input type="text" id="documento" placeholder="Documento" required />
          </div>

          <div className="input-group">
            <input type="password" id="contrasena" placeholder="Contraseña" required />
          </div>

          <button type="submit" className="create-account-btn">
            Registrar
          </button>

          <p className="terms-text">
            Al hacer clic en continuar, aceptas nuestros{" "}
            <a href="/terminos">Términos de servicio</a> y{" "}
            <a href="/privacidad">Política de privacidad</a>.
          </p>

          <p id="registerMessage" className="message"></p>
        </form>
      </div>
    </div>
  );
};

export default Registro;
