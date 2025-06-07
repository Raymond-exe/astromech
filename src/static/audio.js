window.addEventListener('load', () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        let options = { mimeType: 'audio/webm;codecs=opus' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            console.warn("mimeType not supported, falling back to default");
            options = {};
        }

        const recorder = new MediaRecorder(stream, options);

        recorder.ondataavailable = event => {
            if (event.data.size > 0) {
                fetch("/mic", {
                    method: "POST",
                    headers: { "Content-Type": "application/octet-stream" },
                    body: event.data
                });
            }
        };

        recorder.start(200);
    }).catch(err => console.error(err));
});
