function getUsers() {
    return JSON.parse(localStorage.getItem("users")) || [];
}
function addUser(user) {
    const users = getUsers();
    users.push(user);
    localStorage.setItem("users", JSON.stringify(users));
}
function findUser(username, password) {
    return getUsers().find(u => u.username === username && u.password === password);
}
function usernameExists(username) {
    return getUsers().some(u => u.username === username);
}
function setLoggedUser(user) {
    localStorage.setItem("loggedUser", JSON.stringify(user));
}
function getLoggedUser() {
    return JSON.parse(localStorage.getItem("loggedUser"));
}
function logout() {
    localStorage.removeItem("loggedUser");
    window.location.href = "index.html";
}
function redirectByRole(role) {
    if (role === "admin") {
        window.location.href = "admin.html";
    } else {
        window.location.href = "user.html";
    }
}



async function loginUsuario(user, password) {
    try {
        const loginData = {
            correo_usuario: user,
            clave_usuario: password
        };

        const response = await fetch("http://localhost:3001/api/usuario/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(loginData)
        });

        if (!response.ok) {
            throw new Error("Error en la solicitud: " + response.status);
        }

        const data = await response.json();
        return (data.datos)

        

    } catch (error) {
        console.error("Error:", error);
        return null
      
    }


}