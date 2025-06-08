function setupTouchLogging(id, zoneName) {
    const area = document.getElementById(id);

    area.addEventListener("touchstart", event => {
        const touch = event.touches[0];
        if (within(touch, area.getBoundingClientRect())) {
            event.preventDefault();
            const rect = area.getBoundingClientRect();
            const relativeX = (touch.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);
            const relativeY = (touch.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);
            sendUpdate(zoneName, relativeX, relativeY);
        }
    }, { passive: false });

    area.addEventListener("touchmove", event => {
        event.preventDefault();
        const rect = area.getBoundingClientRect();
        const touch = event.touches[0];
        const relativeX = (touch.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);
        const relativeY = (touch.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);
        sendUpdate(zoneName, relativeX, relativeY);
    }, { passive: false });

    area.addEventListener("touchend", event => {
        event.preventDefault();
        sendUpdate(zoneName);
    }, { passive: false });

    document.addEventListener("contextmenu", event => {
        event.preventDefault()
        event.stopPropagation()
        return false;
    });

    function sendUpdate(zone, x = 0, y = 0) {
        x = x > 1 ? 1 : (x < -1 ? -1 : x); // limit x & y to [-1, 1]
        y = y > 1 ? 1 : (y < -1 ? -1 : y);
        fetch("/touch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ zone, x, y })
        });
    }

    function within(touch, rect) {
        return (between(touch.clientX, rect.left, rect.right) &&
        between(touch.clientY, rect.top, rect.bottom));
    }

    function between(value, min, max) {
        return (value >= min && value <= max);
    }
}

window.addEventListener('load', () => {
    setupTouchLogging("left-touch", "left");
    setupTouchLogging("right-touch", "right");
});

function playSound(key) {
    fetch('/play/' + key).then(r => r.text());
}
