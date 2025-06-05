function setupTouchLogging(id, zoneName) {
    const area = document.getElementById(id);

    area.addEventListener("touchstart", event => {
        event.touches.forEach(touch => {
            if (within(touch, area.getBoundingClientRect())) {
                event.preventDefault();
            }
        })
    }, { passive: false });

    area.addEventListener("touchmove", event => {
        const rect = area.getBoundingClientRect();
        
        for (let touch of event.touches) {
            if (within(touch, rect)) {
                event.preventDefault();
                const relativeX = (touch.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);
                const relativeY = (touch.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);

                sendUpdate(zoneName, relativeX, relativeY);
            }
        }
    }, { passive: false });

    area.addEventListener("touchend", event => {
        const rect = area.getBoundingClientRect();

        for (let touch of event.changedTouches) {
            if (within(touch, rect)) {
                event.preventDefault();
                sendUpdate(zoneName);
            }
        }
    }, { passive: false });

    function sendUpdate(zone, x = 0, y = 0) {
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

window.onload = () => {
    setupTouchLogging("left-touch", "left");
    setupTouchLogging("right-touch", "right");
};
