function adaptiveLighten([r, g, b], maxFactor = 0.4) {
    const distance = (255 - r) + (255 - g) + (255 - b);
    const maxDistance = 255 * 3;
    const factor = (distance / maxDistance) * maxFactor;

    const newR = Math.round(r + (255 - r) * factor);
    const newG = Math.round(g + (255 - g) * factor);
    const newB = Math.round(b + (255 - b) * factor);

    return `rgb(${newR}, ${newG}, ${newB})`;
}

document.addEventListener("DOMContentLoaded", () => {
    const img = document.getElementById("playlist-cover");
    if (!img) return;

    const colorThief = new ColorThief();

    img.addEventListener("load", () => {
        const [r, g, b] = colorThief.getColor(img);

        const primaryColor = `rgb(${r}, ${g}, ${b})`;
        const secondaryColor = adaptiveLighten([r, g, b], 0.4);

        document.documentElement.style.setProperty("--primary-color", primaryColor);
        document.documentElement.style.setProperty("--secondary-color", secondaryColor);
    });
});