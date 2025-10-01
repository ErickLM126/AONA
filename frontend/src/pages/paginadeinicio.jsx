import React from "react";
import "../services/styles/paginadeinicio.css";
import arte from "../assets/images/arte.jpg";
import guitarra from "../assets/images/guitarra.jpg";
import audifonos from "../assets/images/audifonos.jpg";
import calle from "../assets/images/calle.jpg";

function LandingPage() {
  return (
    <>
      <header className="header">
        <a href="/login" className="nav-button">
          Inicio de sesión
        </a>
        <a href="/register" className="nav-button">
          Registrarse
        </a>
      </header>

      <main className="main-content">
        <div className="background-image"></div>
        <div className="content-overlay">
          <h1 className="welcome-text">Welcome to</h1>
          <h2 className="title-text">
            Harmonics Of <br /> Natural Art
          </h2>
          <a href="#music-section" className="scroll-arrow">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="feather feather-chevron-down"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </a>
        </div>
      </main>

      {/* Section Música */}
      <section id="music-section" className="expanded-section">
        <div className="text-block">
          <p>Una comunidad para artistas y amantes del arte natural.</p>
          <p>
            Explora, conecta y comparte tu pasión por la música, la pintura, el
            teatro y la danza.
          </p>
          <p>Aquí no distorsionamos el arte con filtros: lo vivimos como es.</p>
        </div>

        <div className="music-card">
          <div className="music-card-title">Música</div>
          <div className="music-card-content">
            <div className="music-text">
              <p>Sumérgete en un espacio donde el sonido nace desde el alma.</p>
              <p>
                Aquí celebramos la música como forma pura de expresión: sin
                efectos, sin artificios, solo talento real.
              </p>
              <p>
                Comparte tus composiciones, escucha a otros artistas y conecta
                con quienes vibran al ritmo del arte auténtico.
              </p>
            </div>

            <div className="gallery">
              <img
                src={arte}
                alt="Musical art image 1"
                className="gallery-image"
              />
              <img
                src={guitarra}
                alt="Musical art image 2"
                className="gallery-image"
              />
              <img
                src={audifonos}
                alt="Musical art image 3"
                className="gallery-image"
              />
              <img
                src={calle}
                alt="Musical art image 4"
                className="gallery-image"
              />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default LandingPage;
