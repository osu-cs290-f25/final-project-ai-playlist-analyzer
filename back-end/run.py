from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import os

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
DATA_FILE = "./playlist_url.json"

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
async def home(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request})

@app.post("/add_playlist")
def add_playlist(playlist: Playlist):
    if not playlist.url:
        raise HTTPException(status_code=400, detail="Need a request body with `url`")

    new_playlist = {"url": playlist.url}
    playlist_data.setdefault("playlists", []).append(new_playlist)

    # Save back to JSON file
    with open(DATA_FILE, "w") as f:
        json.dump(playlist_data, f, indent=2)

    return {"message": "Received a playlist!", "playlist": new_playlist}



# extra stuff
@app.get("/playlist")
async def get_playlist():
    with open("playlist.json") as f:
        return json.load(f)

class PlaylistData(BaseModel):
    songs: list[str]
    moods: list[str]
    coverPhoto: str

@app.post("/save")
async def save_playlist(data: PlaylistData):
    with open("playlist.json", "w") as f:
        json.dump(data.dict(), f, indent=4)
    return {"status": "saved"}

