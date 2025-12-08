import os
from dotenv import load_dotenv
import spotipy
import joblib
import requests
import time
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import json
from io import BytesIO
from colorthief import ColorThief


# color finder
def adaptive_lighten(rgb, max_factor=0.4):
    r, g, b = rgb
    distance = (255 - r) + (255 - g) + (255 - b)
    max_distance = 255 * 3
    factor = (distance / max_distance) * max_factor

    new_r = round(r + (255 - r) * factor)
    new_g = round(g + (255 - g) * factor)
    new_b = round(b + (255 - b) * factor)

    return f"rgb({new_r}, {new_g}, {new_b})"

# how we save the playlist
def save_playlist_to_json(playlist_data, filename="playlist_url.json"):
    # If file exists, load it; otherwise start fresh
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {"playlists": []}

    # Append new playlist info
    existing_data["playlists"].append(playlist_data)

    # Save back to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4)

    print(f"✅ Playlist saved to {filename}")


# how we analyze the playlist
def analyze_playlist(playlist_url):

    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), ".." , "..", "secret.env"))
    client_id = os.getenv("SPOTIPY_CLIENT_ID") 
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET") 
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")



    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



    # auth_manager = SpotifyOAuth( client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="playlist-read-private playlist-read-collaborative" )
    #  print (redirect_uri)
    # sp = Spotify(auth_manager=auth_manager)

    model = joblib.load("model/mood_model.pkl") 
    le = joblib.load("model/label_encoder.pkl")

    features = ['valence', 'energy', 'danceability', 'acousticness', 'loudness', 'speechiness']

    # this finds the playlist and allows us to group the songs by themselves
    # playlist_link = "https://open.spotify.com/playlist/7vWVX36xMHGwi1f9L9OX61" # this is roxane playlist
    # another playlist: "https://open.spotify.com/playlist/22vzWz8jg0xrIqBoE59ULO"
    playlist_link = playlist_url # this is my throwback's playlist
    playlist_id = playlist_link.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id) 
    tracks = results['items']

    playlist = sp.playlist(playlist_id)

    image_url = playlist['images'][0]['url']
    print("image of playlist:", image_url)


    # download the playlist cover image
    response = requests.get(image_url)
    img_bytes = BytesIO(response.content)

    # extract dominant color
    color_thief = ColorThief(img_bytes)
    r, g, b = color_thief.get_color(quality=1)

    primary_color = f"rgb({r}, {g}, {b})"
    secondary_color = adaptive_lighten((r, g, b), 0.25)
    # starts saving the data:
    playlist_data = {
        "url": playlist_url,
        "playlist-name": playlist['name'],
        "image-url": image_url,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "songs": []
    }


    # After you've built the client and fetched tracks:
    for item in tracks : # [:1]:
        track = item['track']
        track_name = track['name']
        artist = track['artists'][0]['name']
        print(f"song: {track_name}, artist: {artist}")
        try:
            url = "https://track-analysis.p.rapidapi.com/pktx/analysis"
            params = {
                "song": track_name,
                "artist": artist # optional field but recommended for accuracy
            }

            headers = {
                "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
                "X-RapidAPI-Host": "track-analysis.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=params)

            data = response.json()
            # print("Response JSON:", data)
            
            
            # features = ['valence', 'energy', 'danceability', 'acousticness', 'loudness', 'speechiness']
            # make all the data get prepped into 0-1 range, and order it in the same order for the ai to analysis
            def preprocess_features(data):
                raw_loudness = data.get("loudness", "-60 dB")
                loudness_val = float(raw_loudness.replace(" dB", ""))

                return {
                    "valence": data.get("happiness", 0)/100.0,
                    "energy": data.get("energy", 0)/100.0,
                    "danceability": data.get("danceability", 0)/100.0,
                    "acousticness": data.get("acousticness", 0)/100.0,
                    "loudness": (loudness_val / 60.0) + 1,  # normalize dB
                    "speechiness": data.get("speechiness", 0)/100.0
                    # "tempo": data.get("tempo", 0) / 200.0,               # not needed, not tested with
                }
            X_song = pd.DataFrame([preprocess_features(data)])
            
            if (X_song.values == 0).all():
                mood = "Unknown"
            else :
                pred = model.predict(X_song)
                mood = le.inverse_transform(pred)[0]
            
            
            time.sleep(0.1) # for now we remove the sleep

        except Exception as e:
            print(f"⚠️ Failed to fetch features for {track_name}: {e}")
            mood = "Unknown"

        # saves the song after it finds the mood
        playlist_data["songs"].append({
            "title": track_name,
            "artist": artist,
            "mood": mood
        })

    # Save to JSON file
    save_playlist_to_json(playlist_data)

    # make the chart here in the futureS


# for testing purposes
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run.py <playlist_url>")
        sys.exit(1)

    playlist_url = sys.argv[1]
    analyze_playlist(playlist_url)
