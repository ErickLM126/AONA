import React from "react";
import "../services/styles/home.css";

function Home() {
  return (
    <div className="main-container">
      <aside className="left-sidebar">
        <div id="user-profile-container" className="profile-hidden">
          <img
            id="profile-image"
            src="https://via.placeholder.com/60"
            alt="Foto de perfil"
          />
          <div className="user-info">
            <h2 id="user-name"></h2>
          </div>
        </div>

        <nav className="sidebar-nav">
          <ul>
            <li>
              <a href="#" className="nav-item">
                <i className="fa-solid fa-user"></i>
                <span>Perfil</span>
              </a>
            </li>
            <li>
              <a href="chats.html" className="nav-item">
                <i className="fa-solid fa-comments"></i>
                <span>Conversaciones</span>
              </a>
            </li>
            <li>
              <a href="#" className="nav-item">
                <i className="fa-solid fa-music"></i>
                <span>Música</span>
              </a>
            </li>
          </ul>
        </nav>

        <div className="logout-section">
          <a href="/paginadeinicio" className="nav-item" id="logout-button">
            <i className="fa-solid fa-arrow-right-from-bracket"></i>
            <span>Cerrar Sesión</span>
          </a>
        </div>
      </aside>

      <main className="main-content">
        <div className="search-and-create">
          <input
            type="text"
            placeholder="Búsqueda"
            className="search-input"
          />
          <button className="create-post-btn">
            <i className="fa-solid fa-plus"></i> Crear Publicación
          </button>
        </div>

        <div className="post-card">
          <div className="post-header">
            <img
              src="https://via.placeholder.com/40"
              alt="Foto de perfil de Elver G"
            />
            <div className="post-info">
              <h3>Elver G</h3>
              <span>9 Abril 2025</span>
            </div>
          </div>

          <div className="post-body">
            <h4>Mi nueva adquisición</h4>
            <img
              src="https://via.placeholder.com/400x300?text=Imagen+de+la+publicacion"
              alt="Imagen de la publicación"
            />
          </div>
        </div>
      </main>

      {/* Sidebar derecha */}
      <aside className="right-sidebar">
        <div className="chat-search">
          <i className="fa-solid fa-magnifying-glass"></i>
          <input type="text" placeholder="Búsqueda" />
        </div>

        <div className="chat-list">
          <div className="chat-item">
            <img
              src="https://via.placeholder.com/50"
              alt="Foto de perfil de Helena Hills"
            />
            <div className="chat-info">
              <h5>Helena Hills</h5>
              <p>Will head to the Help Center...</p>
            </div>
          </div>

          <div className="chat-item">
            <img
              src="https://via.placeholder.com/50"
              alt="Foto de perfil de Carlo Emilie"
            />
            <div className="chat-info">
              <h5>Carlo Emilie</h5>
              <p>Let's go</p>
            </div>
          </div>

          <div className="chat-item">
            <img
              src="https://via.placeholder.com/50"
              alt="Foto de perfil de Oscar Davis"
            />
            <div className="chat-info">
              <h5>Oscar Davis</h5>
              <p>Awesome</p>
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
}

export default Home;
