document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("playlistForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const playlistUrl = document.getElementById("playlistUrl").value;

    try {
      const response = await fetch("/add_playlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: playlistUrl })
      });

      if (!response.ok) {
        throw new Error("Failed to save playlist");
      }

      const result = await response.json();
      console.log("Playlist saved:", result);

      // optional: refresh page
      // location.reload();

    } catch (err) {
      console.error("Error saving playlist:", err);
    }
  });
});
