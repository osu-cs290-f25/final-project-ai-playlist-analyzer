

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