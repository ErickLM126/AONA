// Este es un ejemplo para simular los datos del usuario logeado.
const userData = {
    isLoggedIn: true, // Cambia a 'false' para simular que no hay sesión iniciada
    name: "Elver G",
    profileImageUrl: "https://via.placeholder.com/60/7A9C7A/FFFFFF?text=EG"
};

// Función para actualizar la UI según el estado de la sesión
function updateProfileUI() {
    const profileContainer = document.getElementById("user-profile-container");
    const userNameElement = document.getElementById("user-name");
    const profileImageElement = document.getElementById("profile-image");

    if (userData.isLoggedIn) {
        userNameElement.textContent = userData.name;
        profileImageElement.src = userData.profileImageUrl;
        profileContainer.classList.remove("profile-hidden");
    } else {
        profileContainer.classList.add("profile-hidden");
    }
}

function handleLogout() {
    userData.isLoggedIn = false;
    
    window.location.href = 'paginadeinicio.html';
}

document.addEventListener("DOMContentLoaded", () => {
    updateProfileUI();

    const logoutButton = document.getElementById("logout-button");
    if (logoutButton) {
        logoutButton.addEventListener("click", (event) => {
            event.preventDefault();
            handleLogout();
        });
    }
});
