import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/login";
import Home from "./pages/home";
import Chats from "./pages/chats";
import PaginaInicio from "./pages/paginadeinicio";
import Privacidad from "./pages/privacidad";
import Registro from "./pages/register";
import Terminos from "./pages/terminos";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/login" element={<Login />} />
        <Route path="/terminos" element={<Terminos />} />
        <Route path="/privacidad" element={<Privacidad />} />
        <Route path="/inicio" element={<PaginaInicio />} />
        <Route path="/chats" element={<Chats />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
