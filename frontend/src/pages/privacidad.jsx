import React from "react";

const PoliticaPrivacidad = () => {
  return (
    <div className="privacy-page">
      <header className="header">
        <h1 className="main-title">Política de Privacidad</h1>
        <p className="update-date">
          <strong>Última actualización:</strong> 15/09/2025
        </p>
      </header>

      <main className="privacy-content">
        <section>
          <h2>1. Información que recopilamos</h2>
          <p>
            Datos de registro: nombre, documento, contraseña y datos de contacto. También el contenido que los usuarios publiquen en la plataforma.
          </p>
        </section>

        <section>
          <h2>2. Uso de la información</h2>
          <p>
            Utilizamos los datos para administrar las cuentas, permitir la interacción entre usuarios y mejorar la experiencia en la plataforma.
          </p>
        </section>

        <section>
          <h2>3. Protección de datos</h2>
          <p>
            Implementamos medidas de seguridad para proteger tu información. Nunca compartiremos datos personales con terceros sin tu consentimiento, salvo obligación legal.
          </p>
        </section>

        <section>
          <h2>4. Derechos de los usuarios</h2>
          <p>
            Puedes acceder, modificar o eliminar tus datos desde tu cuenta. También puedes solicitar la eliminación total de tu información contactándonos.
          </p>
        </section>

        <section>
          <h2>5. Cookies</h2>
          <p>
            Podemos utilizar cookies para mejorar la navegación y experiencia de usuario. El usuario puede configurar su navegador para rechazar cookies si lo desea.
          </p>
        </section>

        <section>
          <h2>6. Contacto</h2>
          <p>
            Si tienes dudas sobre estos términos o el manejo de tu información, puedes escribirnos a través de los canales de contacto disponibles en la plataforma.
          </p>
        </section>
      </main>

      <footer className="footer">
        <p>&copy; 2025 Harmonics of Natural Art - Todos los derechos reservados</p>
      </footer>
    </div>
  );
};

export default PoliticaPrivacidad;
