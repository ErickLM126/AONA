import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePublicaciones } from "../hooks/usePublicaciones";
import "../services/styles/home.css";

function Home() {
  const [nombreUsuario, setNombreUsuario] = useState("Usuario");
  const [showModal, setShowModal] = useState(false);
  const [texto, setTexto] = useState("");
  const [imagen, setImagen] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const navigate = useNavigate();

  const {
    publicaciones,
    mensaje,
    setMensaje,
    cargarPublicaciones,
    publicar,
  } = usePublicaciones();

  useEffect(() => {
    const nombre = localStorage.getItem("nombreUsuario");
    if (nombre) setNombreUsuario(nombre);
    cargarPublicaciones();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("nombreUsuario");
    navigate("/login");
  };

  const handleOpenModal = () => {
    setShowModal(true);
    setTexto("");
    setImagen(null);
    setMensaje("");
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setTexto("");
    setImagen(null);
    setMensaje("");
  };

  const handlePublicar = async (e) => {
    e.preventDefault();
    if (!texto && !imagen) {
      setMensaje("Agrega texto o una imagen/video.");
      return;
    }
    await publicar({ usuario: nombreUsuario, texto, imagen });
    setTimeout(() => {
      setShowModal(false);
    }, 1000);
  };

  // Filtrado de publicaciones por búsqueda
  const publicacionesFiltradas = publicaciones.filter(
    (pub) =>
      pub.titulo?.toLowerCase().includes(busqueda.toLowerCase()) ||
      pub.contenido?.toLowerCase().includes(busqueda.toLowerCase()) ||
      pub.autor?.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="main-container">
      <aside className="left-sidebar">
        <div id="user-profile-container" className="profile-visible">
          <img
            id="profile-image"
            src="https://via.placeholder.com/60"
            alt="Foto de perfil"
          />
          <div className="user-info">
            <h2 id="user-name">{nombreUsuario}</h2>
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
              <a href="/chats" className="nav-item">
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
          <button className="nav-item" id="logout-button" onClick={handleLogout}>
            <i className="fa-solid fa-arrow-right-from-bracket"></i>
            <span>Cerrar Sesión</span>
          </button>
        </div>
      </aside>

      <main className="main-content">
        <section className="search-and-create">
          <input
            type="text"
            placeholder="Buscar publicaciones..."
            className="search-input"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
          <button className="create-post-btn" onClick={handleOpenModal}>
            <i className="fa-solid fa-plus"></i> Crear Publicación
          </button>
        </section>

        {/* Modal para añadir publicación */}
        {showModal && (
          <div className="modal-overlay">
            <div className="modal-publicacion">
              <button className="modal-back" onClick={handleCloseModal}>
                <i className="fa-solid fa-arrow-left"></i>
              </button>
              <form onSubmit={handlePublicar} className="modal-form">
                <textarea
                  placeholder="Añadir Texto"
                  value={texto}
                  onChange={(e) => setTexto(e.target.value)}
                  className="modal-textarea"
                  rows={3}
                />
                <input
                  type="file"
                  accept="image/*,video/*"
                  onChange={(e) => setImagen(e.target.files[0])}
                  className="modal-file"
                />
                <button type="submit" className="modal-publicar-btn">
                  Publicar
                </button>
                {mensaje && <div className="modal-mensaje">{mensaje}</div>}
              </form>
            </div>
          </div>
        )}

        <div className="feed-publicaciones">
          {publicacionesFiltradas.length === 0 && (
            <div
              style={{
                textAlign: "center",
                color: "#888",
                marginTop: "2em",
              }}
            >
              No hay publicaciones para mostrar.
            </div>
          )}
          {publicacionesFiltradas.map((pub) => (
            <section className="post-card" key={pub.id}>
              <div className="post-header">
                <img
                  src="https://via.placeholder.com/40"
                  alt={`Foto de perfil de ${pub.autor}`}
                />
                <div className="post-info">
                  <h3>{pub.autor}</h3>
                  <span>{pub.fecha_publicacion}</span>
                </div>
              </div>
              <div className="post-body">
                <h4>{pub.titulo}</h4>
                <p>{pub.contenido}</p>
                {pub.imagen_url && (
                  <img
                    src={`http://localhost:5000${pub.imagen_url}`}
                    alt="Imagen de la publicación"
                    style={{
                      maxWidth: "100%",
                      borderRadius: "8px",
                      marginTop: "10px",
                    }}
                  />
                )}
              </div>
            </section>
          ))}
        </div>
      </main>

      <aside className="right-sidebar">
        <div className="chat-search">
          <i className="fa-solid fa-magnifying-glass"></i>
          <input type="text" placeholder="Buscar chats..." />
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
