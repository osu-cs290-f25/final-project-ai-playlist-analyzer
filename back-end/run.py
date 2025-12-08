from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import os
from starlette.exceptions import HTTPException as StarletteHTTPException
from model.predict_playlist import analyze_playlist
import matplotlib.pyplot as plt
from chart import generate_mood_chart



# Run with:
from pydantic import BaseModel
import json

# how to run the code
# python -m uvicorn run:app --reload --host 0.0.0.0 --port 7222
# Then visit: http://flip2.engr.oregonstate.edu:7222



app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# JSON file for storing playlists
DATA_FILE = "playlist_url.json"

# Load existing data if file exists, otherwise initialize
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        playlist_data = json.load(f)
else:
    playlist_data = {"playlists": []}

# Pydantic model for request body
class Playlist(BaseModel):
    url: str

@app.get("/playlist")
async def get_playlist():
    with open("playlist.json") as f:
        return json.load(f)
 
# this makes the os look from the stat
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# this loads the default home page (index.html)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, search: str = None):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    playlists = data["playlists"]
    if search:
        playlists = [
            p for p in playlists
            if search.lower() in p['playlist-name'].lower() or
                any(search.lower() in song['mood'].lower() for song in p    ['songs'])
        ]
    return templates.TemplateResponse(
        "index.jinja",
        {"request": request, "playlists": playlists, "search_query": search}
    )





 # this loads the singular post page
@app.get("/playlist/{playlist_id}", response_class=HTMLResponse)
async def playlist_detail(request: Request, playlist_id: int):
    with open('playlist_url.json', 'r') as f:
        data = json.load(f)
    playlist = data['playlists'][playlist_id - 1]

    # Count moods
    mood_counts = {}
    for song in playlist.get("songs", []):
        mood = song.get("mood", "Unknown")
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    total_songs = len(playlist.get("songs", []))
    percentages = {
        mood: (count / total_songs) * 100
        for mood, count in mood_counts.items()
    } if total_songs > 0 else {}

    # Call helper function
    chart_path = generate_mood_chart(playlist_id, playlist, percentages)

    # Attach chart path to playlist dict
    playlist["chart"] = chart_path

    return templates.TemplateResponse(
        "post_page.jinja",
        {"request": request, "playlist": playlist}
    )


@app.post("/add_playlist")
def add_playlist(playlist: Playlist):
    if not playlist.url:
        raise HTTPException(status_code=400, detail="Need a request body with `url`")

    analyze_playlist(playlist.url)
    

    return {"message": "Received a playlist!"}


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.jinja",
            {"request": request},
            status_code=404
        )
    # fallback: let FastAPI handle other errors normally
    return HTMLResponse(str(exc.detail), status_code=exc.status_code)


