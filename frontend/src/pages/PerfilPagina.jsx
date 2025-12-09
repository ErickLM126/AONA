import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../services/styles/perfil.css';
import { 
  obtenerPerfil, 
  actualizarPerfil,
  seguirUsuario,
  dejarSeguir,
  verificarSeguimiento,
  obtenerSeguimientos,
  obtenerEstadisticas,
  editarPublicacion,
  eliminarPublicacion,
  fijarPublicacion,
  denunciarPublicacion 
} from '../services/perfilService';

function PerfilPagina() {
    const navigate = useNavigate();
    const { id } = useParams();
    
    const [datosPerfil, setDatosPerfil] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    const [usuarioActual, setUsuarioActual] = useState(null);
    const [perfilUsuarioId, setPerfilUsuarioId] = useState(null);
    const [modalAbierto, setModalAbierto] = useState(false);
    const [formData, setFormData] = useState({
        nombre: '',
        imagen: null,
        imagenPreview: null
    });
    const [guardando, setGuardando] = useState(false);
    const [puedeEditar, setPuedeEditar] = useState(false);
    const [siguiendo, setSiguiendo] = useState(false);
    const [cargandoSeguir, setCargandoSeguir] = useState(false);
    const [estadisticas, setEstadisticas] = useState({
      total_seguidores: 0,
      total_siguiendo: 0,
      total_publicaciones: 0,
      total_reacciones: 0
    });
    const [seguimientos, setSeguimientos] = useState({ siguiendo: [], seguidores: [] });
    const [modalEditarAbierto, setModalEditarAbierto] = useState(false);
    const [publicacionEditar, setPublicacionEditar] = useState(null);
    const [formEditarPublicacion, setFormEditarPublicacion] = useState({ titulo: '', contenido: '', imagen: null });
    const [modalDenunciaAbierto, setModalDenunciaAbierto] = useState(false);
    const [publicacionDenunciar, setPublicacionDenunciar] = useState(null);
    const [motivoDenuncia, setMotivoDenuncia] = useState('');

    useEffect(() => {
        const cargarPerfil = async () => {
            try {
                const usuarioJSON = localStorage.getItem("usuario");
                if (!usuarioJSON) {
                    setError("No hay usuario activo. Por favor inicia sesión.");
                    setCargando(false);
                    return;
                }
                
                const usuario = JSON.parse(usuarioJSON);
                setUsuarioActual(usuario);
                
                const idPerfil = id ? parseInt(id) : usuario.id;
                setPerfilUsuarioId(idPerfil);
                
                console.log("[PERFIL] Cargando perfil para ID:", idPerfil);
                const datos = await obtenerPerfil(idPerfil);
                
                if (datos.success) {
                    const generarAvatar = (nombre) => 
                        `https://ui-avatars.com/api/?name=${encodeURIComponent(nombre)}&background=38a169&color=fff&size=100`;
                    
                    const avatarUrl = datos.usuario.imagen_perfil_url 
                        ? `http://localhost:5000${datos.usuario.imagen_perfil_url}`
                        : generarAvatar(datos.usuario.nombre);
                    
                    const perfilProcesado = {
                        id: datos.usuario.id,
                        nombre: datos.usuario.nombre,
                        avatarUrl: avatarUrl,
                        coverImageUrl: 'https://images.unsplash.com/photo-1511379938547-c1f69b13d835?w=800&h=300&fit=crop',
                        
                        singles: (datos.productos && datos.productos.length > 0) ? 
                            datos.productos.map(p => ({
                                id: p.id,
                                titulo: p.titulo,
                                imageUrl: p.imagen_url || null
                            })) : [],
                        
                        publicaciones: (datos.publicaciones && datos.publicaciones.length > 0) ? 
                            datos.publicaciones.map(pub => ({
                                id: pub.id,
                                autor: datos.usuario.nombre,
                                fecha: new Date(pub.fecha_publicacion).toLocaleDateString('es-ES', { 
                                    year: 'numeric', 
                                    month: 'long', 
                                    day: 'numeric' 
                                }),
                                tituloContenido: pub.titulo || '',
                                postImageUrl: pub.imagen_url || null,  // Ya viene con URL completa del backend
                                postText: pub.contenido || ''
                            })) : [],
                        
                        comentarios: (datos.comentarios && datos.comentarios.length > 0) ? 
                            datos.comentarios.map(com => ({
                                id: com.id,
                                autor: com.autor,
                                autor_id: com.autor_id,
                                avatarUrl: `https://ui-avatars.com/api/?name=${encodeURIComponent(com.autor)}&background=random&color=fff&size=36`,
                                texto: com.comentario || ''
                            })) : []
                    };
                    
                    setDatosPerfil(perfilProcesado);
                    setFormData({
                        nombre: datos.usuario.nombre,
                        imagen: null,
                        imagenPreview: avatarUrl
                    });
                    setError(null);
                } else {
                    setError(datos.message || "Error al cargar el perfil");
                }
            } catch (error) {
                console.error("[PERFIL] Error al cargar:", error);
                setError("Error al cargar los datos del perfil");
            } finally {
                setCargando(false);
            }
        };
        
        cargarPerfil();
    }, [id]);

    useEffect(() => {
        const cargarDatosAdicionales = async () => {
            if (!usuarioActual || !perfilUsuarioId) return;
            
            try {
                const esPerfilPropio = perfilUsuarioId === usuarioActual.id;
                setPuedeEditar(esPerfilPropio);
        
                if (!esPerfilPropio) {
                  const verificacion = await verificarSeguimiento(usuarioActual.id, perfilUsuarioId);
                  console.log("[PERFIL] Verificación de seguimiento:", verificacion);
                  setSiguiendo(verificacion.siguiendo || false);
                }
        
                const stats = await obtenerEstadisticas(perfilUsuarioId);
                console.log("[PERFIL] Estadísticas:", stats);
                if (stats.success) {
                  setEstadisticas(stats.estadisticas || {
                    total_seguidores: 0,
                    total_siguiendo: 0,
                    total_publicaciones: 0,
                    total_reacciones: 0
                  });
                }
        
                const segs = await obtenerSeguimientos(perfilUsuarioId);
                if (segs.success) {
                  setSeguimientos({
                    siguiendo: segs.siguiendo || [],
                    seguidores: segs.seguidores || []
                  });
                }
              } catch (error) {
                console.error("[PERFIL] Error al cargar datos adicionales:", error);
              }
        };

        cargarDatosAdicionales();
    }, [usuarioActual, perfilUsuarioId]);

    const abrirModalEdicion = () => {
        setFormData({
            nombre: datosPerfil.nombre,
            imagen: null,
            imagenPreview: datosPerfil.avatarUrl
        });
        setModalAbierto(true);
    };

    const cerrarModal = () => {
        setModalAbierto(false);
        setFormData({
            nombre: '',
            imagen: null,
            imagenPreview: null
        });
    };

    const manejarCambioNombre = (e) => {
        setFormData({
            ...formData,
            nombre: e.target.value
        });
    };

    const manejarCambioImagen = (e) => {
        const archivo = e.target.files[0];
        if (archivo) {
            const reader = new FileReader();
            reader.onload = (evento) => {
                setFormData({
                    ...formData,
                    imagen: archivo,
                    imagenPreview: evento.target.result
                });
            };
            reader.readAsDataURL(archivo);
        }
    };

    const guardarCambios = async () => {
        if (!formData.nombre.trim()) {
            alert('El nombre no puede estar vacío');
            return;
        }

        try {
            setGuardando(true);
            const datosActualizar = {
                nombre: formData.nombre,
                imagen: formData.imagen
            };

            const resultado = await actualizarPerfil(usuarioActual.id, datosActualizar);

            if (resultado.success) {
                const usuarioActualizado = {
                    ...usuarioActual,
                    nombre: resultado.usuario.nombre
                };
                localStorage.setItem('usuario', JSON.stringify(usuarioActualizado));

                const generarAvatar = (nombre) => 
                    `https://ui-avatars.com/api/?name=${encodeURIComponent(nombre)}&background=38a169&color=fff&size=100`;
                
                const nuevaAvatarUrl = resultado.usuario.imagen_perfil_url 
                    ? `http://localhost:5000${resultado.usuario.imagen_perfil_url}`
                    : generarAvatar(resultado.usuario.nombre);

                const perfilActualizado = {
                    ...datosPerfil,
                    nombre: resultado.usuario.nombre,
                    avatarUrl: nuevaAvatarUrl
                };
                
                setDatosPerfil(perfilActualizado);
                setUsuarioActual(usuarioActualizado);

                cerrarModal();
                alert('Perfil actualizado correctamente');
            } else {
                alert(resultado.message || 'Error al actualizar el perfil');
            }
        } catch (error) {
            console.error('[PERFIL] Error al guardar:', error);
            alert('Error al guardar los cambios');
        } finally {
            setGuardando(false);
        }
    };

    const handleSeguir = async () => {
      try {
        setCargandoSeguir(true);
        
        if (siguiendo) {
          const resultado = await dejarSeguir(usuarioActual.id, perfilUsuarioId);
          console.log("[PERFIL] Dejar de seguir - Respuesta:", resultado);
          if (resultado.success) {
            setSiguiendo(false);
            const stats = await obtenerEstadisticas(perfilUsuarioId);
            if (stats.success) setEstadisticas(stats.estadisticas);
          } else {
            alert(resultado.message || "Error al dejar de seguir");
          }
        } else {
          const resultado = await seguirUsuario(usuarioActual.id, perfilUsuarioId);
          console.log("[PERFIL] Seguir - Respuesta:", resultado);
          if (resultado.success) {
            setSiguiendo(true);
            const stats = await obtenerEstadisticas(perfilUsuarioId);
            if (stats.success) setEstadisticas(stats.estadisticas);
          } else {
            alert(resultado.message || "Error al seguir");
          }
        }
      } catch (error) {
        console.error("[PERFIL] Error:", error);
        alert("Error al actualizar seguimiento");
      } finally {
        setCargandoSeguir(false);
      }
    };

    const ComentarioTarjeta = ({ comentario }) => (
        <div className="comment-card">
            <img 
                src={comentario.avatarUrl} 
                alt={comentario.autor} 
                className="comment-avatar" 
            />
            <div className="comment-content">
                <p>
                    <span className="comment-author">{comentario.autor}</span>
                    <span className="comment-text">{comentario.texto}</span>
                </p>
                <span className="comment-reply">responder reaccionar</span>
            </div>
        </div>
    );

    const abrirEditorPublicacion = (pub) => {
      setPublicacionEditar(pub);
      setFormEditarPublicacion({
        titulo: pub.tituloContenido,
        contenido: pub.postText,
        imagen: null
      });
      setModalEditarAbierto(true);
    };

    const guardarEdicionPublicacion = async () => {
      try {
        const resultado = await editarPublicacion(publicacionEditar.id, formEditarPublicacion);
        if (resultado.success) {
          alert('Publicación actualizada correctamente');
          setModalEditarAbierto(false);
          // Recargar perfil
          window.location.reload();
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error al actualizar la publicación');
      }
    };

    const handleEliminarPublicacion = async (idPub) => {
      if (window.confirm('¿Estás seguro de que quieres eliminar esta publicación?')) {
        try {
          const resultado = await eliminarPublicacion(idPub);
          if (resultado.success) {
            alert('Publicación eliminada');
            window.location.reload();
          }
        } catch (error) {
          alert('Error al eliminar');
        }
      }
    };

    const handleFijarPublicacion = async (idPub) => {
      try {
        const resultado = await fijarPublicacion(idPub);
        if (resultado.success) {
          alert('Publicación fijada correctamente');
          window.location.reload();
        }
      } catch (error) {
        alert('Error al fijar');
      }
    };

    const handleDenunciar = async () => {
      if (!motivoDenuncia.trim()) {
        alert('Debes indicar un motivo para la denuncia');
        return;
      }
      try {
        const resultado = await denunciarPublicacion(publicacionDenunciar.id, motivoDenuncia);
        if (resultado.success) {
          alert('Denuncia enviada correctamente');
          setModalDenunciaAbierto(false);
          setMotivoDenuncia('');
        }
      } catch (error) {
        alert('Error al denunciar');
      }
    };

    if (cargando) {
        return (
            <div className="profile-container">
                <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <p>Cargando perfil...</p>
                </div>
            </div>
        );
    }

    if (error && !datosPerfil) {
        return (
            <div className="profile-container">
                <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
                    <p style={{ color: 'red' }}>{error}</p>
                    <button onClick={() => navigate('/login')} style={{ marginTop: '10px', padding: '10px 20px' }}>
                        Ir a Login
                    </button>
                </div>
            </div>
        );
    }

    if (!datosPerfil) {
        return (
            <div className="profile-container">
                <p>No hay datos disponibles</p>
            </div>
        );
    }

    return (
        <>
            <div className="profile-container">
                
                <div className="main-content">
                    
                    <div className="search-bar">
                        <input 
                            type="text" 
                            placeholder="Búsqueda" 
                            className="search-input"
                        />
                        <span role="img" aria-label="cámara">📹</span>
                        <span role="img" aria-label="ajustes">⚙️</span>
                    </div>

                    {datosPerfil.singles.length > 0 && (
                        <>
                            <h2 className="section-title">Mis sencillos musicales</h2>
                            <div className="musical-singles">
                                {datosPerfil.singles.map(single => (
                                    <div key={single.id} className="single-item">
                                        {single.imageUrl ? (
                                            <img src={single.imageUrl} alt={single.titulo} />
                                        ) : (
                                            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                                <span>Sin imagen</span>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </>
                    )}

                    {datosPerfil.publicaciones.length > 0 ? (
                        <>
                            <h2 className="section-title">Publicaciones</h2>
                            {datosPerfil.publicaciones.map(post => (
                                <div key={post.id} className="publication-post">
                                    
                                    <div className="post-header">
                                        <img src={datosPerfil.avatarUrl} alt={post.autor} className="post-avatar" />
                                        <div className="post-info">
                                            <p className="post-author">{post.autor}</p>
                                            <p className="post-date">{post.fecha}</p>
                                        </div>
                                        <div className="post-menu-container">
                                          <div className="post-menu-trigger">⋯</div>
                                          <div className="post-menu-dropdown">
                                            {puedeEditar ? (
                                              // Opciones para el propietario
                                              <>
                                                <button 
                                                  className="menu-item edit"
                                                  onClick={() => abrirEditorPublicacion(post)}
                                                >
                                                  ✎ Editar
                                                </button>
                                                <button 
                                                  className="menu-item pin"
                                                  onClick={() => handleFijarPublicacion(post.id)}
                                                >
                                                  📌 Fijar
                                                </button>
                                                <button 
                                                  className="menu-item delete"
                                                  onClick={() => handleEliminarPublicacion(post.id)}
                                                >
                                                  🗑 Eliminar
                                                </button>
                                              </>
                                            ) : (
                                              // Opciones para otros usuarios
                                              <>
                                                <button 
                                                  className="menu-item pin"
                                                  onClick={() => handleFijarPublicacion(post.id)}
                                                >
                                                  📌 Fijar
                                                </button>
                                                <button 
                                                  className="menu-item report"
                                                  onClick={() => {
                                                    setPublicacionDenunciar(post);
                                                    setModalDenunciaAbierto(true);
                                                  }}
                                                >
                                                  🚩 Denunciar
                                                </button>
                                              </>
                                            )}
                                          </div>
                                        </div>
                                    </div>
                                    
                                    {post.tituloContenido && (
                                        <p className="post-content-title">{post.tituloContenido}</p>
                                    )}
                                    
                                    {post.postImageUrl && (
                                        <div className="post-image-container">
                                            <img src={post.postImageUrl} alt="Contenido de la Publicación" />
                                        </div>
                                    )}
                                </div>
                            ))}
                        </>
                    ) : (
                        <div className="empty-state">
                            <p>Sin publicaciones aún. ¡Comparte tu primer contenido!</p>
                        </div>
                    )}
                </div>

                <div className="sidebar">
                    
                    <div className="profile-header" style={{backgroundImage: `url(${datosPerfil.coverImageUrl})`}}>
                        <div className="profile-icon">🎸</div>
                        <img src={datosPerfil.avatarUrl} alt={datosPerfil.nombre} className="profile-avatar" />
                        <h3 className="profile-name">{datosPerfil.nombre}</h3>
                        
                        <div className="profile-stats">
                            <div className="stat-item">
                                <span className="stat-number">{estadisticas.total_publicaciones || 0}</span>
                                <span className="stat-label">Publicaciones</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-number">{estadisticas.total_seguidores || 0}</span>
                                <span className="stat-label">Seguidores</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-number">{estadisticas.total_siguiendo || 0}</span>
                                <span className="stat-label">Siguiendo</span>
                            </div>
                        </div>
                        
                        <div className="profile-buttons">
                            {puedeEditar ? (
                                <>
                                    <button className="profile-data-button" onClick={abrirModalEdicion}>
                                        Editar Perfil
                                    </button>
                                    <button className="profile-data-button">Datos</button>
                                </>
                            ) : (
                                <button 
                                    className={`profile-follow-button ${siguiendo ? 'following' : ''}`}
                                    onClick={handleSeguir}
                                    disabled={cargandoSeguir}
                                >
                                    {cargandoSeguir ? 'Cargando...' : (siguiendo ? 'Dejar de Seguir' : 'Seguir')}
                                </button>
                            )}
                        </div>
                    </div>
                    
                    <div className="comments-section">
                        <div className="comments-title">
                            <span>Comentarios</span>
                            <span>...</span>
                        </div>
                        
                        {datosPerfil.comentarios.length > 0 ? (
                            datosPerfil.comentarios.map(comentario => (
                                <ComentarioTarjeta key={comentario.id} comentario={comentario} />
                            ))
                        ) : (
                            <div className="empty-state">
                                <p>Sin comentarios aún</p>
                            </div>
                        )}

                        <div className="comment-input-area">
                            <button className="comment-button">Comentar</button>
                        </div>
                    </div>
                </div>
            </div>

            {modalAbierto && (
                <div className="modal-overlay" onClick={cerrarModal}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Editar Perfil</h2>
                            <button className="modal-close" onClick={cerrarModal}>✕</button>
                        </div>

                        <form onSubmit={(e) => { e.preventDefault(); guardarCambios(); }}>
                            <div className="image-preview-container">
                                <img src={formData.imagenPreview} alt="Preview" className="image-preview" />
                                <label htmlFor="imagen-input" className="image-upload-label">
                                    Cambiar Foto
                                </label>
                                <input 
                                    id="imagen-input"
                                    type="file" 
                                    accept="image/*" 
                                    className="image-upload-input"
                                    onChange={manejarCambioImagen}
                                />
                                {formData.imagen && (
                                    <span className="image-filename">{formData.imagen.name}</span>
                                )}
                            </div>

                            <div className="form-group">
                                <label className="form-label">Nombre</label>
                                <input 
                                    type="text"
                                    className="form-input"
                                    value={formData.nombre}
                                    onChange={manejarCambioNombre}
                                    placeholder="Ingresa tu nombre"
                                />
                            </div>

                            <div className="modal-buttons">
                                <button 
                                    type="button"
                                    className="modal-button modal-button-cancel"
                                    onClick={cerrarModal}
                                    disabled={guardando}
                                >
                                    Cancelar
                                </button>
                                <button 
                                    type="submit"
                                    className="modal-button modal-button-save"
                                    disabled={guardando}
                                >
                                    {guardando ? (
                                        <div className="modal-loading">
                                            <span>Guardando</span>
                                            <div className="spinner"></div>
                                        </div>
                                    ) : (
                                        'Guardar'
                                    )}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* MODAL EDITAR PUBLICACIÓN */}
            {modalEditarAbierto && (
              <div className="modal-overlay" onClick={() => setModalEditarAbierto(false)}>
                <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                  <div className="modal-header">
                    <h2 className="modal-title">Editar Publicación</h2>
                    <button className="modal-close" onClick={() => setModalEditarAbierto(false)}>✕</button>
                  </div>
                  <form onSubmit={(e) => { e.preventDefault(); guardarEdicionPublicacion(); }}>
                    <div className="form-group">
                      <label className="form-label">Título</label>
                      <input 
                        type="text"
                        className="form-input"
                        value={formEditarPublicacion.titulo}
                        onChange={(e) => setFormEditarPublicacion({...formEditarPublicacion, titulo: e.target.value})}
                        placeholder="Título de la publicación"
                      />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Contenido</label>
                      <textarea 
                        className="form-input"
                        rows="4"
                        value={formEditarPublicacion.contenido}
                        onChange={(e) => setFormEditarPublicacion({...formEditarPublicacion, contenido: e.target.value})}
                        placeholder="Contenido de la publicación"
                      />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Imagen (opcional)</label>
                      <input 
                        type="file"
                        accept="image/*"
                        className="form-input"
                        onChange={(e) => setFormEditarPublicacion({...formEditarPublicacion, imagen: e.target.files[0]})}
                      />
                    </div>
                    <div className="modal-buttons">
                      <button type="button" className="modal-button modal-button-cancel" onClick={() => setModalEditarAbierto(false)}>
                        Cancelar
                      </button>
                      <button type="submit" className="modal-button modal-button-save">
                        Guardar Cambios
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}

            {/* MODAL DENUNCIAR PUBLICACIÓN */}
            {modalDenunciaAbierto && (
              <div className="modal-overlay" onClick={() => setModalDenunciaAbierto(false)}>
                <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                  <div className="modal-header">
                    <h2 className="modal-title">Denunciar Publicación</h2>
                    <button className="modal-close" onClick={() => setModalDenunciaAbierto(false)}>✕</button>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Motivo de la denuncia:</label>
                    <select 
                      className="form-input"
                      value={motivoDenuncia}
                      onChange={(e) => setMotivoDenuncia(e.target.value)}
                    >
                      <option value="">Selecciona un motivo</option>
                      <option value="contenido_ofensivo">Contenido ofensivo</option>
                      <option value="spam">Spam</option>
                      <option value="contenido_sexual">Contenido sexual</option>
                      <option value="violencia">Violencia</option>
                      <option value="otro">Otro</option>
                    </select>
                  </div>
                  <div className="modal-buttons">
                    <button className="modal-button modal-button-cancel" onClick={() => setModalDenunciaAbierto(false)}>
                      Cancelar
                    </button>
                    <button className="modal-button modal-button-save" onClick={handleDenunciar}>
                      Enviar Denuncia
                    </button>
                  </div>
                </div>
              </div>
            )}
        </>
    );
}

export default PerfilPagina;