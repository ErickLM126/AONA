function checkSession() {
    const user = getLoggedUser();
    console.log (user)
    if (!user) {
        window.location.href = "index.html";
    } else {
        if (window.location.pathname.endsWith("admin.html") && user.role !== "admin") {
            redirectByRole(user.role);
        }
        if (window.location.pathname.endsWith("user.html") && user.role !== "user") {
            redirectByRole(user.role);
        }
    }
}


        