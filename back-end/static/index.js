
// required to save the json
fetch("/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
})
    .then(response => response.json())
    .then(result => {
        console.log("Server response:", result)
    })
    .catch(error => console.error("Error:", error));

// using the data in the 
async function loadPlaylist() {
    const response = await fetch("/playlist");
    const playlist = await response.json();

    // Update the image src with the coverPhoto URL
    document.getElementById("cover").src = playlist.coverPhoto;

    // Show songs/moods too
    document.getElementById("results").innerText =
        `Songs: ${playlist.songs.join(", ")}\nMoods: ${playlist.moods.join(", ")}`;
}





// someone elses stuff
document.createElement("html")


var button = document.createElement

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("playlistForm");
  const list = document.getElementById("playlistList");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = document.getElementById("playlistUrl").value;

    // Send to FastAPI backend
    const response = await fetch("/people/add_playlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const result = await response.json();
    alert(result.message);

    // Add to list dynamically
    const li = document.createElement("li");
    li.textContent = `${url} - ${caption}`;
    list.appendChild(li);

    form.reset();
  });
});