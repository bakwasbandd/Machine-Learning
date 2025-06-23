import streamlit as st
from spotify_analysis import analyze_playlist
from utils import get_roast, get_personality_roast, get_recommendations_raw
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id="0c5335a96ef648f2870da0546328347a",
    client_secret="10f86e0d76634e69a8e5ef8a127fc41e",
    redirect_uri="http://127.0.0.1:8080",
    scope="playlist-read-private user-top-read"
))

st.title("₍^. .^₎⟆ Noodles Hates It")
st.subheader("Does Noodles Think Your Playlist is Trash? Yes he does ...😼")
playlist_url = st.text_input("Paste your Spotify Playlist Link:")

if playlist_url:
    with st.spinner("Analyzing your playlist..."):
        result = analyze_playlist(playlist_url, sp)

        if result:
            st.subheader("🎤 Artist Frequency")
            st.pyplot(result["artist_chart"])
            st.write(get_roast(result["top_artist"]))

            st.subheader("🎧 Genre Distribution")
            st.pyplot(result["genre_chart"])
            st.write(get_roast(result["top_genre"]))

            st.subheader("🧠 Playlist Personality (According to Noodles)")
            st.write(get_personality_roast(result["top_genres"]))

            st.subheader("🎶 Recommended Songs You Might Like")
            for track in result["recommendations"]:
                st.markdown(
                    f"- [{track['name']}]({track['url']}) by {track['artist']}")
        else:
            st.error("Something went wrong. Please check the playlist link.")
