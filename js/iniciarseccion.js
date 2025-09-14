document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const usuario = document.getElementById('login-usuario').value;
    const contrasena = document.getElementById('login-contrasena').value;

    // Aquí envías los datos al endpoint de inicio de sesión en tu servidor.
    // **Asegúrate de cambiar esta URL por la de tu backend.**
    fetch('http://tu-servidor.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            usuario,
            contrasena
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('¡Inicio de sesión exitoso!');
            // Si el inicio de sesión es exitoso, el servidor puede devolver un token.
            // Puedes guardarlo en localStorage para mantener la sesión.
            localStorage.setItem('authToken', data.token);
            // Y luego redirigir al usuario a la página principal.
            window.location.href = 'pagina-principal.html'; 
        } else {
            alert('Error al iniciar sesión: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al conectar con el servidor.');
    });
});