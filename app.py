import streamlit as st
from spotify_analysis import analyze_playlist
from utils import get_roast, get_personality_roast, get_recommendations_raw
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import streamlit as st
import base64  # for videos!!

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id="0c5335a96ef648f2870da0546328347a",
    client_secret="10f86e0d76634e69a8e5ef8a127fc41e",
    redirect_uri="http://127.0.0.1:8080",
    scope="playlist-read-private user-top-read"
))

st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;  /* Reduce from default (~6.5rem) */
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.corner-paw {
    position: fixed;
    font-size: 30px;
    z-index: 99;
}
.top-left { top: 5px; left: 10px; }
.top-right { top: 5px; right: 10px; }
.bottom-left { bottom: 5px; left: 10px; }
.bottom-right { bottom: 5px; right: 10px; }
</style>

<div class="corner-paw top-left">🐾</div>
<div class="corner-paw top-right">🐾</div>
<div class="corner-paw bottom-left">🐾</div>
<div class="corner-paw bottom-right">🐾</div>
""", unsafe_allow_html=True)


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


# st.subheader(" ")


def get_video_html(path, width=200):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return f'''
    <video width="{width}" autoplay muted loop playsinline style="border-radius: 10px;">
        <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
    </video>
    '''


img = Image.open("pictures/noodles1.png")

# to keep the picture in centre
left, centre, right = st.columns([4, 2, 4])

with centre:
    st.image(img, width=150)


st.markdown("""
<div style='text-align: center; margin-top: 30px; margin-bottom: 10px;'>
    <label style='font-size:18px; color:'white'; font-weight:bold;'>
        Insert your playlist here so Noodles can call it trash — <br>respectfully, of course!!! (ᵕ•_•)
    </label>
</div>
""", unsafe_allow_html=True)

playlist_url = st.text_input("", key="playlist_input")


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

st.subheader("")  #to add space!!

st.subheader("👩🏻‍💻 About this project ")
st.markdown("""
<div style="border: 2px dashed #ffeee6;
            border-radius: 12px;
            padding: 20px;
            margin: 30px auto;
            width: 80%;
            color: #ffeee6;
            font-family: Comic Sans MS;
            text-align: center;">
    hiiii!!! turning everything into a tribute to my rude orange cat, Noodles, is kind of my thing. <br><br>
    he’s nosy, dramatic, and exceptionally gifted at shoving his face where it doesn’t belong — like straight into my food. 🍲<br><br>
    sooo naturally, Noodle Poodle feels <b>very</b> entitled to share his completely unsolicited opinions about your playlist.<br>
    whether you asked or not hehe
</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(get_video_html("pictures/dancingcar.mp4"),
                unsafe_allow_html=True)

with col2:
    st.markdown(get_video_html("pictures/dancingmonke.mp4"),
                unsafe_allow_html=True)

with col3:
    st.markdown(get_video_html("pictures/dancingcar.mp4"),
                unsafe_allow_html=True)

st.text("")

st.markdown("""
<div style="text-align: center;">
    <a href="https://github.com/bakwasbandd" target="_blank" style="text-decoration: none; margin-right: 15px;">
        <button style="padding:10px 20px; font-size:16px; border:none; background-color:#b35929; color:white; border-radius:5px;">💻 GitHub</button>
    </a>
    <a href="https://www.linkedin.com/in/muntaha-adnan/" target="_blank" style="text-decoration: none;">
        <button style="padding:10px 20px; font-size:16px; border:none; background-color:#b35929; color:white; border-radius:5px;">🔗 LinkedIn</button>
    </a>
</div>
""", unsafe_allow_html=True)
