window.addEventListener('load', () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });

        recorder.ondataavailable = event => {
            if (event.data.size > 0) {
                fetch("/audio-in", {
                    method: "POST",
                    headers: { "Content-Type": "application/octet-stream" },
                    body: event.data
                });
            }
        };

        recorder.start(200);
    }).catch(err => console.error(err));
});
