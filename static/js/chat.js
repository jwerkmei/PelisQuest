function onLoad() {
    let messageInput = document.getElementById('message')
    let submitButton = document.getElementById('send-message')
    let form = document.getElementById('message-form')

    // Escuchar cambios en el input de texto para habilitar/deshabilitar el botón de enviar
    messageInput.addEventListener('input', (event) => {
        if (event.target.value.length > 0) {
            submitButton.classList.remove('disabled')
        } else {
            submitButton.classList.add('disabled')
        }
    })

    function addMessageToChat(message) {
        let messageHTML = ''

        if (message.author === 'assistant') {
            messageHTML = `
                <div class="d-flex flex-row justify-content-start mb-4">
                    <img src="/static/pixelart_logo.png" alt="avatar 1" style="width: 45px; height: 45px;">
                    <div class="p-3 ms-3 message-assistant" style="border-radius: 15px; background-color: rgba(57, 192, 237,.2); font-size: 16px;">
                        <p class="mb-0">${message.content}</p>
                    </div>
                </div>
            `;
        } else {
            messageHTML = `
                <div class="d-flex flex-row justify-content-end mb-4">
                    <div class="p-3 me-3 border bg-body-tertiary" style="border-radius: 15px;">
                        <p class="mb-0">${message.content}</p>
                    </div>
                </div>
            `
        }

        document.getElementById('messages').insertAdjacentHTML('beforeend', messageHTML)

        // Scroll suave hacia el último mensaje
        const lastMessage = document.getElementById('messages').lastElementChild;
        lastMessage.scrollIntoView({ behavior: 'smooth' });
    }

    // Función para manejar la lógica de envío de mensajes
    async function sendMessage(formData) {
        submitButton.classList.add('disabled')
        messageInput.classList.add('disabled')
        submitButton.value = 'Enviando...'

        addMessageToChat({
            content: formData.get('message'),
            author: 'user',
        })
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
               'Accept': 'application/json',
            },
            body: formData,
        })

        const message = await response.json()
        addMessageToChat(message)
        messageInput.value = ''
        messageInput.classList.remove('disabled')
        submitButton.value = 'Enviar'
    }

    // Manejar la lógica de enviar el formulario cuando se usa el input de texto
    document.addEventListener('submit', (event) => {
        event.preventDefault()

        const form = event.target
        const formData = new FormData(form)

        sendMessage(formData)
    })

    // Escuchar clics en los botones de recomendación rápida (los botones "Recomiéndame una...")
    document.querySelectorAll('.btn-shortcut').forEach(button => {
        button.setAttribute('type', 'button') // Cambiar el tipo de botón a "button"

        button.addEventListener('click', (event) => {
            event.preventDefault()

            // Poner el valor del botón en el campo de texto
            messageInput.value = event.target.value

            // Crear un FormData con el formulario completo
            const formData = new FormData(form)

            // Enviar el mensaje al servidor usando sendMessage
            sendMessage(formData)
        })
    })
}

document.addEventListener('DOMContentLoaded', onLoad)