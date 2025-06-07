function playSound(key) {
    fetch('/play/' + key).then(r => r.text());
}

function displayMessage(message) {
    const textDiv = document.createElement("div");
    textDiv.innerText = message;
    textDiv.style.position = "fixed";
    textDiv.style.top = "50%";
    textDiv.style.left = "50%";
    textDiv.style.transform = "translate(-50%, -50%)";
    textDiv.style.color = "white";
    textDiv.style.background = "rgba(0, 0, 0, 0.6)";
    textDiv.style.padding = "20px 30px";
    textDiv.style.borderRadius = "10px";
    textDiv.style.fontSize = "1.2em";
    textDiv.style.zIndex = "9999";
    textDiv.style.textAlign = "center";

    document.body.appendChild(textDiv);
    setTimeout(() => textDiv.remove(), 5000);

    fetch("/debug", {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: message
    });
}
