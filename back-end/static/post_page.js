document.addEventListener("DOMContentLoaded", () => {
    const desc = document.querySelector(".post-description");

    if (!desc) return;

    const primary = desc.dataset.primary;
    const secondary = desc.dataset.secondary;

    if (primary && secondary) {
        // Set CSS variables globally
        document.documentElement.style.setProperty("--primary-color", primary);
        document.documentElement.style.setProperty("--secondary-color", secondary);

        // Apply colors directly
        document.body.style.backgroundColor = secondary;      // whole page bg
        desc.style.color = secondary;                          // description text

        const songBox = desc.querySelector(".song-box");
        if (songBox) {
            songBox.style.backgroundColor = secondary;
            songBox.style.color = "#000"; // readable text
        }

        const header = document.querySelector(".header-box");
        if (header) {
            header.style.backgroundColor = primary;
            header.style.color = "#fff";
        }
    }
});
