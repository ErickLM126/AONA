const userData = {
    isLoggedIn: true,
    name: "Elver G",
    profileImageUrl: "https://via.placeholder.com/60/7A9C7A/FFFFFF?text=EG"
};

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
