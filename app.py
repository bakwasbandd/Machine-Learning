import streamlit as st
from spotify_analysis import analyze_playlist
from utils import get_roast, get_personality_roast, get_recommendations_raw
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import streamlit as st

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id="0c5335a96ef648f2870da0546328347a",
    client_secret="10f86e0d76634e69a8e5ef8a127fc41e",
    redirect_uri="http://127.0.0.1:8080",
    scope="playlist-read-private user-top-read"
))


st.markdown(
    """
    <style>
    /* Main background area */
    .stApp {
        background-color: #252525;
    }

    /* Optional: Scrollbar for light themes */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #252525;
    }
    ::-webkit-scrollbar-thumb {
        background: #C9C9C9;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("""
    <h1 style='text-align: center; font-family:Comic Sans MS; color:#b35929;'>
        ₍^. .^₎⟆<br>Noodles Hates It
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='text-align: center; font-family:Comic Sans MS; color:#ffeee6;'>
        Does Noodles Think Your Playlist is Trash?<br>Yes he does ...( -_•)╦̵̵̿╤─
    </h3>
""", unsafe_allow_html=True)


img = Image.open("pictures/noodles1.png")

# to keep the picture in centre 
left, centre, right = st.columns([4, 2, 4])

with centre:
    st.image(img, width=150)

playlist_url = st.text_input(
    "Insert your playlist here so Noodles can call it trash — respectfully, of course!!! (ᵕ•_•)")

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
