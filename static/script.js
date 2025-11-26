document.addEventListener('DOMContentLoaded', () => {
    const chatDisplay = document.getElementById('chat-display');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Écoute l'événement de clic sur le bouton d'envoi
    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    // Écoute l'événement de la touche 'Entrée' dans le champ de saisie
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Fonction principale pour envoyer le message
    function sendMessage() {
        const message = userInput.value.trim();

        if (message === '') {
            return; // Ne rien envoyer si le champ est vide
        }

        // 1. Afficher le message de l'utilisateur
        appendMessage(message, 'user');
        
        // 2. Nettoyer le champ de saisie
        userInput.value = '';

        // 3. Envoyer le message au serveur Flask (route /chat)
        fetch('/chat', { // <-- ATTENTION : C'EST ICI QUE C'EST '/chat'
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            // 4. Afficher la réponse du Bot
            const botResponse = data.response || "Désolé, je n'ai pas pu obtenir de réponse.";
            appendMessage(botResponse, 'bot');
        })
        .catch(error => {
            console.error('Erreur de communication avec le serveur:', error);
            appendMessage("🤖 Une erreur est survenue lors de la connexion.", 'bot');
        });
    }

    // Fonction utilitaire pour ajouter une bulle de message à l'écran
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        
        // Ajouter la classe spécifique pour le style CSS
        if (sender === 'user') {
            messageDiv.classList.add('user-message');
        } else {
            messageDiv.classList.add('bot-message');
            // Ajouter l'emoji du Bot
            text = '🤖 ' + text;
        }

        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
        chatDisplay.appendChild(messageDiv);
        
        // Faire défiler l'affichage vers le bas pour voir le dernier message
        chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }
});