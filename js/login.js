document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const documento = document.getElementById('login-documento').value;
    const contrasena = document.getElementById('login-contrasena').value;

    fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            documento,
            contrasena
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('¡Inicio de sesión exitoso!');
            localStorage.setItem('usuario', JSON.stringify(data.usuario));
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
