import React from 'react';
import '../services/styles/tienda.css';
import { useProductos } from '../hooks/useProductos';

export default function Catalogo() {
  const { productos, cargando, error } = useProductos();

  const handleClick = (producto) => {
    alert(`Has seleccionado: ${producto.nombre}`);
  };

  return (
    <div className="catalogo-container">
      <header className="catalogo-header">
        <button className="btn-login">Inicio</button>
        <input type="text" placeholder="Búsqueda" className="input-busqueda" />
        <div className="promo">¡Por tu primera compra el envío es <span>GRATIS!</span>!</div>
        <div className="icono-carrito">🛒</div>
      </header>

      <div className="contenido">
        <aside className="columna-izquierda">
          <div className="oferta">
            <h3>¡Por tu primera compra lleva gratis uno de estos productos!</h3>
            <img src="https://picsum.photos/seed/regalo1/100/100" alt="Promo 1" />
            <img src="https://picsum.photos/seed/regalo2/100/100" alt="Promo 2" />
            <img src="https://picsum.photos/seed/regalo3/100/100" alt="Promo 3" />
            <img src="https://picsum.photos/seed/regalo4/100/100" alt="Promo 4" />
          </div>
          <div className="categorias">
            <h3>Categorías</h3>
            <ul>
              <li>Instrumentos +</li>
              <li>Guitarra +</li>
              <li>Bombo +</li>
              <li>Batería +</li>
              <li>Piano +</li>
              <li>Pedaleras +</li>
              <li>Trompeta +</li>
              <li>Instrumentos de cuerda +</li>
              <li>Instrumentos de viento +</li>
            </ul>
          </div>
        </aside>

        <main className="productos-grid">
          {cargando && <p>Cargando productos...</p>}
          {error && <p>Error al cargar productos.</p>}
          {productos.map((p) => (
            <div key={p.id} className="producto" onClick={() => handleClick(p)}>
              <img src={p.imagen} alt={p.nombre} />
              <h4>{p.nombre}</h4>
              <p className="precio">${p.precio}</p>
              <p className="descripcion">{p.descripcion}</p>
              <p className="stock">Stock: {p.stock}</p>
            </div>
          ))}
        </main>
      </div>
    </div>
  );
}