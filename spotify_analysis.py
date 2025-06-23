import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from utils import fetch_artist_genres, get_recommendations_raw

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id="0c5335a96ef648f2870da0546328347a",
#     client_secret="10f86e0d76634e69a8e5ef8a127fc41e",
#     redirect_uri="http://127.0.0.1:8080",
#     scope="playlist-read-private"
# ))


def get_playlist_tracks(playlist_url, sp):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    tracks = sp.playlist_tracks(playlist_id)
    data = []

    for item in tracks['items']:
        track = item['track']
        if track:
            data.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'artist_id': track['artists'][0]['id']
            })
    return pd.DataFrame(data)


# def plot_bar_chart(data, title, xlabel):
#     fig, ax = plt.subplots()
#     data.plot(kind='bar', ax=ax)
#     ax.set_title(title)
#     ax.set_xlabel(xlabel)
#     ax.set_ylabel('Count')
#     buf = BytesIO()
#     plt.tight_layout()
#     fig.savefig(buf, format="png")
#     buf.seek(0)
#     return buf

def plot_bar_chart(data, title, xlabel):
    fig, ax = plt.subplots()
    data.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Count')
    plt.tight_layout()
    return fig


def analyze_playlist(playlist_url, sp):
    df = get_playlist_tracks(playlist_url, sp)
    if df.empty:
        return None

    artist_counts = df['artist'].value_counts()
    top_artist = artist_counts.idxmax()

    genre_list = []
    for artist_id in df['artist_id'].dropna().unique():
        genre_list += fetch_artist_genres(artist_id, sp)
    genre_series = pd.Series(genre_list)
    genre_counts = genre_series.value_counts()
    top_genre = genre_counts.idxmax()
    top_genres = genre_counts.head(5).index.tolist()

    result = {
        "top_artist": top_artist,
        "top_genre": top_genre,
        "top_genres": top_genres,
        "artist_chart": plot_bar_chart(artist_counts.head(10), "Top Artists", "Artist"),
        "genre_chart": plot_bar_chart(genre_counts.head(10), "Top Genres", "Genre"),
        "recommendations": get_recommendations_raw(top_genres[:2], sp)
    }

    return result
