navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });

    recorder.ondataavailable = e => {
        if (e.data.size > 0) {
            fetch("/mic", {
                method: "POST",
                headers: { "Content-Type": "application/octet-stream" },
                body: e.data
            });
        }
    };

    recorder.start(200);
});
