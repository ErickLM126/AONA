import React from "react";
import "../services/styles/chats.css";

function Chats() {
  return (
    <div className="chat-container">
      <aside className="chat-list-sidebar">
        <div className="chat-header">
          <h3>Chats</h3>
          <i className="fa-solid fa-gear"></i>
        </div>

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
            </div>
          </div>

          <div className="chat-item active">
            <img
              src="https://via.placeholder.com/50"
              alt="Foto de perfil de Oscar Davis"
            />
            <div className="chat-info">
              <h5>Oscar Davis</h5>
            </div>
          </div>
        </div>
      </aside>

      <main className="chat-window">
        <div className="chat-window-header">
          <img src="https://via.placeholder.com/50" alt="Foto de perfil" />
          <div className="chat-info">
            <h5>Oscar Davis</h5>
            <span>Activo hace 1m</span>
          </div>
          <div className="chat-actions">
            <i className="fa-solid fa-video"></i>
            <i className="fa-solid fa-phone"></i>
            <i className="fa-solid fa-ellipsis-v"></i>
          </div>
        </div>

        <div className="chat-messages">
          <div className="message received">
            <p>
              ¡Hola! Me podrías ayudar a crear un post para mi nueva
              adquisición?
            </p>
          </div>
          <div className="message sent">
            <p>Claro, ¿tienes alguna idea en mente?</p>
          </div>
          <div className="message received">
            <p>Sí, estoy pensando en un post de un auto clásico.</p>
          </div>
        </div>

        <div className="chat-input-area">
          <input type="text" placeholder="Escribe tu mensaje..." />
          <i className="fa-solid fa-paperclip"></i>
          <i className="fa-solid fa-camera"></i>
          <button>
            <i className="fa-solid fa-paper-plane"></i>
          </button>
        </div>
      </main>
    </div>
  );
}

export default Chats;
