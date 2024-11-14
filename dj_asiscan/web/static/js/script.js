// myapp/static/js/script.js
document.addEventListener("DOMContentLoaded", function() {
    const cameraSocket = new WebSocket('ws://' + window.location.host + '/ws/camera/');

    cameraSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const imageSrc = "data:image/png;base64," + data.image;
        document.getElementById('cameraImage').src = imageSrc;
    };

    const buttons = document.querySelectorAll('.btn');
    let inactivityTimeout;

    function sendValueToServer(movimiento) {
        fetch('cam/display/enviar_valor_servos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: 'movimiento=' + movimiento
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }

    function resetInactivityTimeout() {
        clearTimeout(inactivityTimeout);
        inactivityTimeout = setTimeout(() => {
            sendValueToServer(0); // Enviar '0' después de 1 segundo de inactividad
        }, 1000);
    }

    buttons.forEach(button => {
        button.addEventListener('mousedown', function() {
            sendValueToServer(this.value);
            resetInactivityTimeout();
        });

        button.addEventListener('mouseup', resetInactivityTimeout);
    });

    resetInactivityTimeout(); // Inicia el temporizador de inactividad
});
