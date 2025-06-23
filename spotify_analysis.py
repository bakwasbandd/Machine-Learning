import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from utils import fetch_artist_genres, get_recommendations_raw


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


# for top artists, PIECHART
def plot_pie_chart(data, title):
    fig, ax = plt.subplots()  # top get a blank canvas
    fig.patch.set_facecolor("#7B97CC")  # Light cream background
    ax.pie(
        data.values,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#E89EB8', '#ADEBB3', '#9D9DCC', '#89CFF0', '#DEA193'],
        explode=[0.1] + [0] * (len(data) - 1),  # Explodes the first slice
        shadow=True
    )

    ax.set_ylabel('')
    ax.set_title(title, fontsize=15, fontweight='bold',fontname='Arial Rounded MT Bold')
    ax.axis("equal")  # for a perfect circle
    plt.tight_layout()
    return fig


def plot_bar_chart(data, title, ylabel):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#F1D7D7")
    ax.set_facecolor("#F1D7D7")  # plot background
    bar_colors = ["#8B485F", "#496D4D", "#7C7CB6",
                  "#579FC0", "#AA6151", "#A8486D", "#5F7450"]
    barChart = ax.barh(data.index, data.values, color=bar_colors[:len(
        data)], edgecolor='black', linewidth=1)
    ax.set_title(title, fontsize=20, fontweight='bold',
                 fontname='Arial Rounded MT Bold')
    ax.set_ylabel(ylabel, fontsize=15, fontweight='bold')
    ax.set_xlabel("Count", fontsize=15, fontweight='bold')

    # ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

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
        "artist_chart": plot_pie_chart(artist_counts.head(5), "Your Top Artists"),
        "genre_chart": plot_bar_chart(genre_counts.head(7), "Top Genres", "Genre"),
        "recommendations": get_recommendations_raw(top_genres[:2], sp)
    }

    return result
