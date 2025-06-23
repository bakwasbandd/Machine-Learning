import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id="0c5335a96ef648f2870da0546328347a",
#     client_secret="10f86e0d76634e69a8e5ef8a127fc41e",
#     redirect_uri="http://127.0.0.1:8080",
#     scope="user-top-read"
# ))


def get_roast(name):
    return random.choice([
        f"Noodles thinks you've got an unhealthy obsession with {name}. Seek help.",
        f"{name}? Again? Noodles just walked out of the room.",
        f"Even Noodles knows other artists exist besides {name}."
    ])


def get_personality_roast(genres):
    if "emo" in genres:
        return "Noodles says you're one sad song away from a poetry blog."
    elif "pop" in genres:
        return "You like the musical equivalent of white bread. - Noodles"
    elif "rap" in genres:
        return "Tough on the outside, but Noodles knows you're soft inside."
    elif "rock" in genres:
        return "You probably still use wired headphones. Vintage. - Noodles"
    else:
        return "You're mysterious... or just confused. - Noodles"


def fetch_artist_genres(artist_id, sp):
    try:
        artist = sp.artist(artist_id)
        return artist.get('genres', [])
    except:
        return []


def get_recommendations_raw(seed_genres, sp):
    try:
        valid_genres = sp.recommendation_genre_seeds()['genres']
    except Exception as e:
        print("Error fetching genre seeds:", e)
        return []

    filtered_genres = [g for g in seed_genres if g in valid_genres]
    if not filtered_genres:
        return []

    recs = sp.recommendations(seed_genres=filtered_genres[:2], limit=5)
    return [{
        "name": t["name"],
        "artist": t["artists"][0]["name"],
        "url": t["external_urls"]["spotify"]
    } for t in recs["tracks"]]
