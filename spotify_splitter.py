import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
CHUNK_SIZE = 200             # max tracks per playlist, you probably don't need to change this.
NEW_PLAYLIST_PREFIX = "Split Playlist Part" # name of the playlists that get created.

# CONFIG — CHANGE THESE!
SPOTIFY_USERNAME = "ketchup" # refer to step 3.1 of the readme for more info
SPOTIFY_CLIENT_ID = "mayonnaise" # refer to step 3.2 of the readme for more info
SPOTIFY_CLIENT_SECRET = "garlicSauce" # refer to step 3.3 of the readme for more info
CSV_FILE = "playlist.csv"   # path to your Exportify CSV, this only works if the script and file are in the same location!

# DON'T CHANGE ANYTHING PAST THIS POINT!
REDIRECT_URI = "http://127.0.0.1:8888/callback"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private",
    open_browser=True
))

# Read Exportify CSV
tracks = []
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    print("CSV columns:", reader.fieldnames)
    for row in reader:
        uri = row.get("\ufeffTrack URI")
        if uri and uri.startswith("spotify:track:"):
            tracks.append(uri)

print(f"Found {len(tracks)} tracks in CSV.")

# Split into chunks and create playlists
for i in range(0, len(tracks), CHUNK_SIZE):
    chunk = tracks[i:i + CHUNK_SIZE]
    playlist_name = f"{NEW_PLAYLIST_PREFIX} {i // CHUNK_SIZE + 1}"
    playlist = sp.user_playlist_create(SPOTIFY_USERNAME, playlist_name, public=False)
    for j in range(0, len(chunk), 100):
        batch = chunk[j:j+100]
        print(f"Adding {len(batch)} tracks to {playlist_name}...")
        for track_uri in batch:
            print(f"  Adding track {track_uri} to {playlist_name}")
        sp.playlist_add_items(playlist["id"], batch)
    print(f"Created {playlist_name} with {len(chunk)} songs.")

print("All done! 🎉")
