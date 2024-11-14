const startBtn = document.getElementById('start-btn');
const statusMsgElem = document.getElementById('status-msg');
const langSelect = document.getElementById('src-lang');
const chatContainer = document.getElementById('chat');
const progressBar = document.getElementById('progress-bar');
const progress = document.getElementById('progress');

let mediaRecorder;
let audioChunks = [];

startBtn.addEventListener('click', async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Your browser does not support audio recording');
        return;
    }

    audioChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.webm');
        formData.append('src_lang', langSelect.value === 'hi' ? 'hi-IN' : 'en-US');

        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.textContent = 'Recording completed. Processing...';
        chatContainer.appendChild(userMessage);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const response = await axios.post('/translate', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            const { english_text, translated_text, audio_path } = response.data;

            addMessage('user', english_text);
            addMessage('bot', translated_text);

            const audioElem = document.createElement('audio');
            audioElem.src = `/download_audio/${audio_path.split('/').pop()}?t=${new Date().getTime()}`;  // Append a timestamp to prevent caching issues
            audioElem.controls = true;
            chatContainer.appendChild(audioElem);

            audioElem.addEventListener('play', () => {
                progress.style.width = '0';
                const duration = audioElem.duration;
                const interval = setInterval(() => {
                    if (audioElem.currentTime >= duration) {
                        clearInterval(interval);
                        progress.style.width = '100%';
                        return;
                    }
                    const progressPercent = (audioElem.currentTime / duration) * 100;
                    progress.style.width = `${progressPercent}%`;
                }, 100);
            });

            chatContainer.scrollTop = chatContainer.scrollHeight;

        } catch (error) {
            console.error('Error translating audio:', error);
            alert('Error translating audio');
        } finally {
            statusMsgElem.textContent = 'Recording completed.';
            stream.getTracks().forEach(track => track.stop());
        }
    };

    mediaRecorder.start();
    statusMsgElem.textContent = 'Recording...';
    startBtn.disabled = true;

    updateProgressBar(true, 5000);

    setTimeout(() => {
        mediaRecorder.stop();
        startBtn.disabled = false;
    }, 5000);  // Record for 5 seconds
});

function addMessage(sender, text) {
    const messageElem = document.createElement('div');
    messageElem.className = `message ${sender}`;
    messageElem.textContent = text;
    chatContainer.appendChild(messageElem);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateProgressBar(start, duration) {
    if (start) {
        let elapsed = 0;
        const interval = setInterval(() => {
            if (elapsed >= duration) {
                clearInterval(interval);
                progress.style.width = '100%';
                return;
            }
            elapsed += 100;
            const progressPercent = (elapsed / duration) * 100;
            progress.style.width = `${progressPercent}%`;
        }, 100);
    } else {
        progress.style.width = '0';
    }
}