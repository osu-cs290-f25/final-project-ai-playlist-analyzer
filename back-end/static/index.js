document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("playlistForm");
  const list = document.getElementById("playlistList");

  // Helper function to validate Spotify playlist URLs
  function isSpotifyPlaylistUrl(url) {
    const webPattern = /^https:\/\/open\.spotify\.com\/playlist\/[A-Za-z0-9]+/;
    const uriPattern = /^spotify:playlist:[A-Za-z0-9]+$/;
    return webPattern.test(url) || uriPattern.test(url);
  }


  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // prevent default form submission

    const playlistUrl = document.getElementById("playlistUrl").value.trim();

    // Validate before sending
    if (!isSpotifyPlaylistUrl(playlistUrl)) {
      alert("Please enter a valid Spotify playlist URL.");
      return;
    }

    try {
      const response = await fetch("/add_playlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: playlistUrl })
      });

      if (!response.ok) {
        throw new Error("Failed to save playlist");
      }
      else {
        document.getElementById("playlistUrl").value = "";
        alert("Playlist Saved")
      }
      

    } catch (err) {
      console.error(err);
      alert("There was an error saving the playlist.");
    }
  });
});