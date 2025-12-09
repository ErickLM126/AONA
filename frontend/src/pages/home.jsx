import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePublicaciones } from "../hooks/usePublicaciones";
import { getChats } from "../services/chatsService";
import { obtenerPerfil } from "../services/perfilService";
import "../services/styles/home.css";

function Home() {
  const [nombreUsuario, setNombreUsuario] = useState("Usuario");
  const [imagenPerfil, setImagenPerfil] = useState("https://via.placeholder.com/80");
  const [chats, setChats] = useState([]);
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [texto, setTexto] = useState("");
  const [imagen, setImagen] = useState(null);
  const [imagenPreview, setImagenPreview] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [cargandoChats, setCargandoChats] = useState(false);
  const navigate = useNavigate();

  const {
    publicaciones,
    mensaje,
    setMensaje,
    cargarPublicaciones,
    publicar,
  } = usePublicaciones();

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        // Obtener usuario del localStorage
        const usuarioJSON = localStorage.getItem("usuario");
        if (!usuarioJSON) {
          navigate("/login");
          return;
        }

        const usuario = JSON.parse(usuarioJSON);
        setUsuarioActual(usuario);
        setNombreUsuario(usuario.nombre);

        // Cargar datos del perfil
        try {
          const datosPerfil = await obtenerPerfil(usuario.id);
          if (datosPerfil.success && datosPerfil.usuario.imagen_perfil_url) {
            setImagenPerfil(`http://localhost:5000${datosPerfil.usuario.imagen_perfil_url}`);
          }
        } catch (error) {
          console.error("Error al cargar perfil:", error);
        }

        // Cargar chats
        cargarChatsUsuario(usuario.id);

        // Cargar publicaciones
        cargarPublicaciones();
      } catch (error) {
        console.error("Error en cargarDatos:", error);
        navigate("/login");
      }
    };

    cargarDatos();
  }, []);

  const cargarChatsUsuario = async (userId) => {
    try {
      setCargandoChats(true);
      const datosChats = await getChats(userId);
      if (datosChats.success) {
        setChats(datosChats.chats || []);
        console.log("[HOME] Chats cargados:", datosChats.chats);
      }
    } catch (error) {
      console.error("[HOME] Error al cargar chats:", error);
    } finally {
      setCargandoChats(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("nombreUsuario");
    localStorage.removeItem("usuario");
    navigate("/login");
  };

  const handleOpenModal = () => {
    setShowModal(true);
    setTexto("");
    setImagen(null);
    setImagenPreview(null);
    setMensaje("");
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setTexto("");
    setImagen(null);
    setImagenPreview(null);
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

  const handleAbrirChat = (chat) => {
    navigate("/chats", { state: { chatSeleccionado: chat } });
  };

  const handleImagenChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImagen(file);
      // Crear preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagenPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
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
            src={imagenPerfil}
            alt="Foto de perfil"
            onError={(e) => {
              e.target.src = "https://via.placeholder.com/80";
            }}
          />
          <div className="user-info">
            <h2 id="user-name">{nombreUsuario}</h2>
          </div>
        </div>

        <nav className="sidebar-nav">
          <ul>
            <li>
              <a href="/PerfilPagina" className="nav-item">
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
                <div className="modal-file-section">
                  <label htmlFor="file-input" className="modal-file-label">
                    <i className="fa-solid fa-paperclip"></i> Seleccionar archivo
                  </label>
                  <input
                    id="file-input"
                    type="file"
                    accept="image/*,video/*"
                    onChange={handleImagenChange}
                    className="modal-file"
                  />
                  {imagen && <span className="modal-file-name">{imagen.name}</span>}
                </div>

                {imagenPreview && (
                  <div className="modal-preview">
                    <div className="preview-header">
                      <span>Vista Previa</span>
                      <button 
                        type="button"
                        className="preview-close"
                        onClick={() => {
                          setImagen(null);
                          setImagenPreview(null);
                        }}
                      >
                        ✕
                      </button>
                    </div>
                    {imagen.type.startsWith('image/') ? (
                      <img src={imagenPreview} alt="Preview" className="preview-image" />
                    ) : (
                      <div className="preview-video">
                        <video src={imagenPreview} controls className="preview-video-player" />
                      </div>
                    )}
                  </div>
                )}
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
          {publicacionesFiltradas.map((pub) => {
            const imagenAutor = pub.imagen_perfil 
              ? pub.imagen_perfil
              : `https://ui-avatars.com/api/?name=${encodeURIComponent(pub.autor)}&background=random&color=fff&size=40`;

            return (
              <section className="post-card" key={pub.id}>
                <div className="post-header">
                  <img
                    src={imagenAutor}
                    alt={`Foto de perfil de ${pub.autor}`}
                    style={{ cursor: 'pointer' }}
                    onClick={() => navigate(`/PerfilPagina/${pub.id_autor}`)}
                    onError={(e) => {
                      e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(pub.autor)}&background=random&color=fff&size=40`;
                    }}
                  />
                  <div className="post-info">
                    <h3 
                      style={{ cursor: 'pointer', color: '#0066cc' }}
                      onClick={() => navigate(`/PerfilPagina/${pub.id_autor}`)}
                    >
                      {pub.autor}
                    </h3>
                    <span>{pub.fecha_publicacion}</span>
                  </div>
                </div>
                <div className="post-body">
                  <h4>{pub.titulo}</h4>
                  <p>{pub.contenido}</p>
                  {pub.imagen_url && (
                    <img
                      src={pub.imagen_url}
                      alt="Imagen de la publicacion"
                      style={{
                        maxWidth: "100%",
                        borderRadius: "8px",
                        marginTop: "10px",
                      }}
                    />
                  )}
                </div>
              </section>
            );
          })}
        </div>
      </main>

      <aside className="right-sidebar">
        <div className="chat-search">
          <i className="fa-solid fa-magnifying-glass"></i>
          <input type="text" placeholder="Buscar chats..." />
        </div>
        <div className="chat-list">
          {cargandoChats ? (
            <div style={{ textAlign: "center", padding: "20px", color: "#888" }}>
              Cargando chats...
            </div>
          ) : chats.length > 0 ? (
            chats.map((chat) => (
              <div 
                key={chat.id_contacto} 
                className="chat-item"
                onClick={() => handleAbrirChat(chat)}
              >
                <img
                  src={`https://ui-avatars.com/api/?name=${encodeURIComponent(chat.nombre_contacto)}&background=random&color=fff&size=45`}
                  alt={`Foto de perfil de ${chat.nombre_contacto}`}
                />
                <div className="chat-info">
                  <h5>{chat.nombre_contacto}</h5>
                  <p>
                    {chat.ultima_interaccion
                      ? new Date(chat.ultima_interaccion).toLocaleDateString()
                      : "Sin mensajes"}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <div style={{ textAlign: "center", padding: "20px", color: "#888" }}>
              Sin chats aún
            </div>
          )}
        </div>
      </aside>
    </div>
  );
}

export default Home;
