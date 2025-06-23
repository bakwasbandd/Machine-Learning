import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cohere  # for AI generated roasts

co = cohere.Client("zOuAgdyAsRK5DWmQHpJzeFzGqA0KP5kIZDZLBtGN")


def get_roast(name):

    response = co.chat(
        model='command-r',
        message=f"Write one sharp, 2-3 lines max roast from Noodles (no cheesy references, and ALWAYS include Noodle's name in the roast) directed at the USER for their top artist/genre, {name}, who dominates their playlist with the most songs. Keep it clever and no cringe, bonus points if you tailor it specifically to that artist/genre. Do not include any follow-up commentary or ANY text after the roast"

    )
    return (response.text.strip())
    # f"Noodles thinks you've got an unhealthy obsession with {name}. Seek help.",
    # f"{name}? Again? Noodles just walked out of the room.",
    # f"Even Noodles knows other artists exist besides {name}."

def get_personality_roast(genres):
    response = co.chat(
        model='command-r',
        message=f"Write one sharp, 2-3 lines max roast from Noodles (no cheesy references, and ALWAYS include Noodle's name in the roast) directed at the USER for the PERSONALITY of their PLAYLIST, which is dominated by the {genres} genre. Keep it clever and no cringe, making sure to poke fun at the vibe or personality of the playlist based on that genre. No generic commentary, and do not include any follow-up text after the roast."
    )
    return response.text.strip()



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
