document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("playlistForm");
  const list = document.getElementById("playlistList");

  form.addEventListener("submit", async (e) => {
    
    const playlistUrl = document.getElementById("playlistUrl").value;

    try {
      const response = await fetch("/add_playlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: playlistUrl })
      });


    } catch {
      if (!response.ok) throw new Error("Failed to save playlist");
    }
  });
});