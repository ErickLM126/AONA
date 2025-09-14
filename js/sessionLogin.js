function checkSession() {
    const user = getLoggedUser();
    console.log (user)
    if (user) {
      redirectByRole(user.role);
    } 
}
checkSession()

        