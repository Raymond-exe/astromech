function setupTouchLogging(id, zoneName) {
    const area = document.getElementById(id);
    area.addEventListener("touchmove", function (e) {
        const rect = area.getBoundingClientRect();
        
        for (let touch of e.touches) {
            if (
                touch.clientX >= rect.left &&
                touch.clientX <= rect.right &&
                touch.clientY >= rect.top &&
                touch.clientY <= rect.bottom
            ) {
                e.preventDefault();
                const relativeX = touch.clientX - (rect.left + rect.width / 2);
                const relativeY = touch.clientY - (rect.top + rect.height / 2);

                fetch("/touch", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        zone: zoneName,
                        x: relativeX,
                        y: relativeY
                    })
                });
            }
        }
    }, { passive: false });
}

window.onload = () => {
    setupTouchLogging("left-touch", "left");
    setupTouchLogging("right-touch", "right");
};
