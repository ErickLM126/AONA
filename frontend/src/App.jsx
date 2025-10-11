import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PaginaInicio from "./pages/paginadeinicio.jsx";
import Login from "./pages/login.jsx";
import Home from "./pages/home.jsx";
import Chats from "./pages/chats.jsx";
import Privacidad from "./pages/privacidad.jsx";
import Registro from "./pages/register.jsx";
import Terminos from "./pages/terminos.jsx";
import Tienda from "./pages/tienda.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PaginaInicio />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/chats" element={<Chats />} />
        <Route path="/privacidad" element={<Privacidad />} />
        <Route path="/register" element={<Registro />} />
        <Route path="/terminos" element={<Terminos />} />
        <Route path="/tienda" element={<Tienda />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
