// ===============================
// Browser Speech Setup
// ===============================
let speechUnlocked = false;

/**
 * Unlock speech synthesis on first user interaction
 * (required by modern browsers)
 */
function unlockSpeech() {
    if (speechUnlocked) return;

    const utterance = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(utterance);
    speechUnlocked = true;
}

/**
 * Speak text using browser TTS
 */
function speakText(text) {
    if (!("speechSynthesis" in window)) {
        console.warn("Speech synthesis not supported");
        return;
    }

    window.speechSynthesis.cancel(); // stop previous speech

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;     // speed (0.5 – 2)
    utterance.pitch = 1;   // tone (0 – 2)
    utterance.volume = 1;  // volume (0 – 1)

    window.speechSynthesis.speak(utterance);
}

// ===============================
// Chat Message Handler
// ===============================
function sendMessage(event) {
    event.preventDefault();

    unlockSpeech(); // 🔓 unlock browser voice

    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // User message
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.innerText = message;
    chatBox.appendChild(userDiv);

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to Flask backend
    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `question=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        // Bot message
        const botDiv = document.createElement("div");
        botDiv.className = "bot-message";
        botDiv.innerText = data.response;
        chatBox.appendChild(botDiv);

        chatBox.scrollTop = chatBox.scrollHeight;

        // 🔊 Speak bot response
        speakText(data.response);
    })
    .catch(error => {
        console.error("Chatbot error:", error);
    });
}
