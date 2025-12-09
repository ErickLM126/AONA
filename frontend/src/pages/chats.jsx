import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "../services/styles/chats.css";
import {
  getChats,
  getMessages,
  enviarMensaje,
  buscarChats,
  obtenerUsuariosDisponibles,
} from "../services/chatsService";
import { obtenerPerfil } from "../services/perfilService";

function Chats() {
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [mensajes, setMensajes] = useState([]);
  const [inputMensaje, setInputMensaje] = useState("");
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [usuariosDisponibles, setUsuariosDisponibles] = useState([]);
  const [mostrarUsuariosDisponibles, setMostrarUsuariosDisponibles] = useState(
    false
  );
  const [perfilContacto, setPerfilContacto] = useState(null);
  const [cargandoPerfil, setCargandoPerfil] = useState(false);
  const ultimoIdMensajeRef = useRef(0);
  const navigate = useNavigate();

  // Obtener usuario actual del localStorage
  useEffect(() => {
    const usuario = JSON.parse(localStorage.getItem("usuario"));
    console.log("Usuario del localStorage:", usuario);

    if (usuario && usuario.id) {
      setUsuarioActual(usuario);
      cargarChatsInicial(usuario.id);
      cargarUsuariosDisponibles(usuario.id);
    } else {
      setError("No hay usuario activo. Por favor inicia sesión.");
      setCargando(false);
    }
  }, []);

  // Cargar perfil del contacto cuando se selecciona un chat
  useEffect(() => {
    if (selectedChat && selectedChat.id_contacto) {
      cargarPerfilContacto(selectedChat.id_contacto);
    }
  }, [selectedChat]);

  // Cargar chats inicialmente
  const cargarChatsInicial = async (userId) => {
    try {
      setCargando(true);
      setError(null);
      console.log("Cargando chats para usuario:", userId);
      const datos = await getChats(userId);
      console.log("Respuesta de chats:", datos);

      if (datos.success) {
        setChats(datos.chats || []);
        if (datos.chats && datos.chats.length > 0 && !selectedChat) {
          setSelectedChat(datos.chats[0]);
          await cargarMensajesChat(datos.chats[0]);
        }
      } else {
        setError(datos.message || "Error al cargar chats");
      }
    } catch (error) {
      console.error("Error al cargar chats:", error);
      setError("Error al conectar con el servidor");
    } finally {
      setCargando(false);
    }
  };

  // Cargar solo mensajes de un chat
  const cargarMensajesChat = async (chat) => {
    if (!chat || !usuarioActual) return; // ← PROTECCIÓN AQUÍ
    try {
      const datos = await getMessages(usuarioActual.id, chat.id_contacto);
      console.log("Mensajes obtenidos:", datos);

      if (datos.success) {
        setMensajes(datos.mensajes || []);
        if (datos.mensajes && datos.mensajes.length > 0) {
          ultimoIdMensajeRef.current = datos.mensajes[datos.mensajes.length - 1].id;
        }
      } else {
        setMensajes([]);
      }
    } catch (error) {
      console.error("Error al cargar mensajes:", error);
      setMensajes([]);
    }
  };

  // Cargar perfil del contacto
  const cargarPerfilContacto = async (contactoId) => {
    try {
      setCargandoPerfil(true);
      const datos = await obtenerPerfil(contactoId);
      if (datos && datos.success) {
        setPerfilContacto(datos.usuario);
      } else {
        setPerfilContacto(null);
      }
    } catch (error) {
      console.error("Error al cargar perfil del contacto:", error);
      setPerfilContacto(null);
    } finally {
      setCargandoPerfil(false);
    }
  };

  // Seleccionar chat
  const seleccionarChat = async (chat) => {
    setSelectedChat(chat);
    ultimoIdMensajeRef.current = 0;
    await cargarMensajesChat(chat);
  };

  // Polling inteligente SOLO para nuevos mensajes
  useEffect(() => {
    if (!selectedChat || !usuarioActual) return;

    const intervalo = setInterval(async () => {
      try {
        const datos = await getMessages(usuarioActual.id, selectedChat.id_contacto);
        if (datos.success && datos.mensajes && datos.mensajes.length > 0) {
          const nuevosMensajes = datos.mensajes.filter(
            msg => msg.id > ultimoIdMensajeRef.current
          );

          if (nuevosMensajes.length > 0) {
            console.log("Nuevos mensajes encontrados:", nuevosMensajes.length);
            setMensajes(prev => [...prev, ...nuevosMensajes]);
            ultimoIdMensajeRef.current = datos.mensajes[datos.mensajes.length - 1].id;
          }
        }
      } catch (error) {
        console.error("Error verificando nuevos mensajes:", error);
      }
    }, 2000);

    return () => clearInterval(intervalo);
  }, [selectedChat, usuarioActual]);

  // Enviar mensaje
  const handleEnviarMensaje = async (e) => {
    e.preventDefault();
    if (!inputMensaje.trim() || !selectedChat) return;

    try {
      const datos = await enviarMensaje(
        usuarioActual.id,
        selectedChat.id_contacto,
        inputMensaje
      );
      if (datos.success) {
        setInputMensaje("");
        await cargarMensajesChat(selectedChat);
        const datosChats = await getChats(usuarioActual.id);
        if (datosChats.success) {
          setChats(datosChats.chats || []);
        }
      }
    } catch (error) {
      console.error("Error al enviar mensaje:", error);
      setError("Error al enviar mensaje");
    }
  };

  // Buscar chats
  const handleBusqueda = async (valor) => {
    setBusqueda(valor);
    if (valor.trim() === "") {
      const datosChats = await getChats(usuarioActual.id);
      if (datosChats.success) {
        setChats(datosChats.chats || []);
      }
    } else {
      try {
        const datos = await buscarChats(usuarioActual.id, valor);
        if (datos.success) {
          setChats(datos.chats || []);
        }
      } catch (error) {
        console.error("Error al buscar chats:", error);
      }
    }
  };

  // Cargar usuarios disponibles
  const cargarUsuariosDisponibles = async (userId) => {
    try {
      const datos = await obtenerUsuariosDisponibles(userId);
      if (datos.success) {
        setUsuariosDisponibles(datos.usuarios || []);
      }
    } catch (error) {
      console.error("Error al cargar usuarios disponibles:", error);
    }
  };

  if (cargando) {
    return (
      <div className="chat-container">
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          height: "100vh",
        }}>
          <div style={{ textAlign: "center" }}>
            <p>Cargando chats...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chat-container">
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          height: "100vh",
        }}>
          <div style={{ textAlign: "center" }}>
            <p style={{ color: "red" }}>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <aside className="chat-list-sidebar">
        <div className="chat-header">
          <h3>Chats</h3>
          <i className="fa-solid fa-gear"></i>
        </div>

        <div className="chat-search">
          <i className="fa-solid fa-magnifying-glass"></i>
          <input
            type="text"
            placeholder="Búsqueda"
            value={busqueda}
            onChange={(e) => handleBusqueda(e.target.value)}
          />
        </div>

        <div className="chat-list-tabs">
          <button
            className={`tab-btn ${!mostrarUsuariosDisponibles ? "active" : ""}`}
            onClick={() => setMostrarUsuariosDisponibles(false)}
          >
            Chats ({chats?.length || 0})
          </button>
          <button
            className={`tab-btn ${mostrarUsuariosDisponibles ? "active" : ""}`}
            onClick={() => setMostrarUsuariosDisponibles(true)}
          >
            Usuarios ({usuariosDisponibles?.length || 0})
          </button>
        </div>

        {!mostrarUsuariosDisponibles ? (
          <div className="chat-list">
            {chats && chats.length > 0 ? (
              chats.map((chat) => (
                <div
                  key={chat.id_contacto}
                  className={`chat-item ${
                    selectedChat?.id_contacto === chat.id_contacto ? "active" : ""
                  }`}
                  onClick={() => seleccionarChat(chat)}
                >
                  <img
                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(
                      chat.nombre_contacto
                    )}&background=random&color=fff&size=50`}
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
              <div className="empty-chats-state">
                <i className="fa-solid fa-comments"></i>
                <p>Sin chats aún</p>
                <span>Inicia una conversación con alguien</span>
              </div>
            )}
          </div>
        ) : (
          <div className="chat-list">
            {usuariosDisponibles && usuariosDisponibles.length > 0 ? (
              usuariosDisponibles.map((usuario) => (
                <div
                  key={usuario.id}
                  className={`chat-item ${
                    selectedChat?.id_contacto === usuario.id ? "active" : ""
                  }`}
                  onClick={() =>
                    seleccionarChat({
                      id_contacto: usuario.id,
                      nombre_contacto: usuario.nombre,
                    })
                  }
                >
                  <img
                    src={
                      usuario.imagen_perfil_url ||
                      `https://ui-avatars.com/api/?name=${encodeURIComponent(
                        usuario.nombre
                      )}&background=random&color=fff&size=50`
                    }
                    alt={`Foto de perfil de ${usuario.nombre}`}
                  />
                  <div className="chat-info">
                    <h5>{usuario.nombre}</h5>
                    <p>Se siguen mutuamente</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-chats-state">
                <i className="fa-solid fa-users"></i>
                <p>Sin usuarios disponibles</p>
                <span>Sigue a alguien que te siga para chatear</span>
              </div>
            )}
          </div>
        )}
      </aside>

      <main className="chat-window">
        {selectedChat ? (
          <>
            <div className="chat-window-header">
              <img
                src={
                  perfilContacto?.imagen_perfil_url ||
                  `https://ui-avatars.com/api/?name=${encodeURIComponent(
                    selectedChat.nombre_contacto
                  )}&background=random&color=fff&size=50`
                }
                alt={`Foto de perfil de ${selectedChat.nombre_contacto}`}
              />
              <div className="chat-info">
                <h5>{selectedChat.nombre_contacto}</h5>
                <span>Activo</span>
              </div>
              <div className="chat-actions">
                <i className="fa-solid fa-video"></i>
                <i className="fa-solid fa-phone"></i>
                <i className="fa-solid fa-ellipsis-v"></i>
              </div>
            </div>

            <div className="chat-messages">
              {mensajes && mensajes.length > 0 ? (
                mensajes.map((msg) => (
                  <div
                    key={msg.id}
                    className={`message ${
                      msg.id_emisor === usuarioActual.id ? "sent" : "received"
                    }`}
                  >
                    <p>{msg.mensaje}</p>
                    <span>
                      {new Date(msg.fecha_envio).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>
                ))
              ) : (
                <p style={{ textAlign: "center", color: "#888" }}>
                  No hay mensajes aún
                </p>
              )}
            </div>

            <form className="chat-input-area" onSubmit={handleEnviarMensaje}>
              <input
                type="text"
                placeholder="Escribe tu mensaje..."
                value={inputMensaje}
                onChange={(e) => setInputMensaje(e.target.value)}
              />
              <i className="fa-solid fa-paperclip"></i>
              <i className="fa-solid fa-camera"></i>
              <button type="submit">
                <i className="fa-solid fa-paper-plane"></i>
              </button>
            </form>
          </>
        ) : (
          <div className="empty-chat-window">
            <div className="empty-chat-content">
              <i className="fa-solid fa-comments"></i>
              <h2>Selecciona un chat para empezar</h2>
              <p>Elige una conversación de la lista o inicia una nueva</p>
              <div className="empty-chat-actions">
                <button className="btn-new-chat">
                  <i className="fa-solid fa-plus"></i> Nuevo Chat
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* BARRA LATERAL DERECHA - PERFIL DEL CONTACTO */}
      {selectedChat && (
        <aside className="chat-profile-sidebar">
          {cargandoPerfil ? (
            <div className="profile-loading">
              <p>Cargando perfil...</p>
            </div>
          ) : perfilContacto ? (
            <>
              <div className="profile-header-with-image">
                <img
                  src={
                    perfilContacto.imagen_perfil_url ||
                    `https://ui-avatars.com/api/?name=${encodeURIComponent(
                      perfilContacto.nombre
                    )}&background=random&color=fff&size=80`
                  }
                  alt={`Foto de perfil de ${perfilContacto.nombre}`}
                  className="profile-avatar"
                />
                <div className="profile-header-info">
                  <h3>{perfilContacto.nombre}</h3>
                  <p>@{perfilContacto.usuario}</p>
                  <span className="status-badge">En línea</span>
                </div>
                <button
                  className="btn-close-profile profile-header-close"
                  onClick={() => setPerfilContacto(null)}
                >
                  <i className="fa-solid fa-chevron-right"></i>
                </button>
              </div>

              <div className="profile-info"></div>

              <div className="profile-actions">
                <button
                  className="btn-profile-view"
                  onClick={() => navigate(`/PerfilPagina/${perfilContacto.id}`)}
                >
                  <i className="fa-solid fa-user"></i> Ver Perfil Completo
                </button>
                <button className="btn-profile-block">
                  <i className="fa-solid fa-ban"></i> Bloquear
                </button>
              </div>

              <div className="profile-stats">
                <div className="stat">
                  <span className="stat-number">
                    {perfilContacto.publicaciones_count || 0}
                  </span>
                  <span className="stat-label">Publicaciones</span>
                </div>
                <div className="stat">
                  <span className="stat-number">
                    {perfilContacto.seguidores_count || 0}
                  </span>
                  <span className="stat-label">Seguidores</span>
                </div>
                <div className="stat">
                  <span className="stat-number">
                    {perfilContacto.seguidos_count || 0}
                  </span>
                  <span className="stat-label">Seguidos</span>
                </div>
              </div>

              {perfilContacto.publicaciones && perfilContacto.publicaciones.length > 0 && (
                <div className="profile-recent-posts">
                  <h4>Publicaciones Recientes</h4>
                  <div className="recent-posts-grid">
                    {perfilContacto.publicaciones.slice(0, 3).map((post) => (
                      <div key={post.id} className="post-thumbnail">
                        {post.imagen_url ? (
                          <img src={post.imagen_url} alt="Publicación" />
                        ) : (
                          <div className="post-placeholder">
                            <i className="fa-solid fa-image"></i>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="profile-error">
              <p>No se pudo cargar el perfil</p>
            </div>
          )}
        </aside>
      )}
    </div>
  );
}

export default Chats;