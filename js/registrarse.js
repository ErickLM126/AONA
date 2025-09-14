document.getElementById('create-account-form').addEventListener('submit', function(event) {
    event.preventDefault(); // 👈 evita que recargue la página

    const nombre = document.getElementById('nombre').value;
    const contacto = document.getElementById('contacto').value;
    const documento = document.getElementById('documento').value;
    const contrasena = document.getElementById('contrasena').value;

    fetch('http://127.0.0.1:5000/registro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: nombre,
            contacto: contacto,
            documento: documento,
            contrasena: contrasena
        })
    })
    .then(response => response.json())
    .then(data => {
        const msg = document.getElementById('registerMessage');
        if (data.success) {
            msg.textContent = "✅ ¡Cuenta creada con éxito!";
            msg.style.color = "green";
            document.getElementById('create-account-form').reset();
        } else {
            msg.textContent = "❌ Error: " + (data.message || "Intenta de nuevo");
            msg.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('registerMessage').textContent = "⚠️ No se pudo conectar al servidor";
    });
});
