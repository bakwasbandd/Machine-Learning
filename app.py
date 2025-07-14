import streamlit as st
from spotify_analysis import analyze_playlist
from utils import get_artist_roast, get_personality_roast, get_recommendations_raw, get_genre_roast
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
        padding-top: 0rem;   
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
        background-color: #000000;
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


# st.markdown("""
# <div style='text-align: center; margin-top: 30px; margin-bottom: 10px;'>
#     <label style='font-size:18px; color:'white'; font-weight:bold;'>
#         Insert your playlist here so Noodles can call it trash — <br>respectfully, of course!!! (ᵕ•_•)
#     </label>
# </div>
# """, unsafe_allow_html=True)

# playlist_url = st.text_input("", key="playlist_input")
# st.subheader("")

st.subheader("")
if 'show_input' not in st.session_state:
    st.session_state['show_input'] = False

if not st.session_state['show_input']:
    col1, col2, col3 = st.columns([5, 4, 5])  # for centering
    with col2:
        if st.button("😼🔗 Get Roasted by Noodles"):
            st.session_state['show_input'] = True

if st.session_state['show_input']:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 10px;'>
            <label style='font-size:18px; color:#ffeee6; font-weight:bold;'>
                Insert your playlist so Noodles can call it trash — respectfully, of course!!! (ᵕ•_•)
            </label>
        </div>
    """, unsafe_allow_html=True)
    playlist_url = st.text_input("", key="playlist_input")

    if playlist_url:
        with st.spinner("Analyzing your playlist..."):
            result = analyze_playlist(playlist_url, sp)

            if result:
                st.text("")
                st.title(f"🎵 Playlist: {result['playlist_name']}")
                st.subheader("🎤 Noodles thinks you're a bit obsessed ")
                st.pyplot(result["artist_chart"])
                # st.write(get_roast(result["top_artist"]))
                # st.markdown(f"""
                # <div style='
                #     background-color: #353839;
                #     border-radius: 15px;
                #     padding: 20px;
                #     margin: 20px auto;
                #     width: 80%;
                #     text-align: center;
                #     font-size: 18px;
                #     font-family: Comic Sans MS, cursive;
                #     color: #FFFFFF;
                #     box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                # '>
                #     {get_artist_roast(result["top_artist"])}
                # </div>
                # """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style='
                    background-color: #222;
                    border-left: 8px solid #ff9f43;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 25px auto;
                    width: 80%;
                    font-family: Comic Sans MS;
                    font-size: 17px;
                    color: #fff7e6;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                '>
                    😾 
                    {get_artist_roast(result["top_artist"])}
                </div>
                """, unsafe_allow_html=True)

                img = Image.open("pictures/noodlesSleeping(2).jpg")
                left, centre, right = st.columns([4, 2, 4])
                with centre:
                    st.image(img, width=200,
                             caption='The state i found noodles in after he listened to your playlist.')

                st.subheader(
                    "🎧 Noodles thinks you should pick a personality, ANY personality")
                st.pyplot(result["genre_chart"])

                st.markdown(f"""
                <div style='
                    background-color: #222;
                    border-left: 8px solid #ff9f43;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 25px auto;
                    width: 80%;
                    font-family: Comic Sans MS;
                    font-size: 17px;
                    color: #fff7e6;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                '>
                    😾 
                    {get_genre_roast(result["top_genre"])}
                </div>
                """, unsafe_allow_html=True)

                # st.markdown(f"""
                # <div style='
                #     background-color: #353839;
                #     border-radius: 15px;
                #     padding: 20px;
                #     margin: 20px auto;
                #     width: 80%;
                #     text-align: center;
                #     font-size: 18px;
                #     font-family: Comic Sans MS, cursive;
                #     color: #FFFFFF;
                #     box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                # '>
                #     {get_genre_roast(result["top_genre"])}
                # </div>
                # """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col2:
                    st.markdown(get_video_html("pictures/litrnoodles.mp4"),
                                unsafe_allow_html=True)

                st.subheader("🧠 Noodles rates your playlist a SOLID 2/10")

                st.markdown(f"""
                <div style='
                    background-color: #222;
                    border-left: 8px solid #ff9f43;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 25px auto;
                    width: 80%;
                    font-family: Comic Sans MS;
                    font-size: 17px;
                    color: #fff7e6;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                '>
                    😾 
                    {get_personality_roast(result["top_genres"])}
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col2:
                    st.markdown(get_video_html("pictures/carjudging.mp4"),
                                unsafe_allow_html=True)

                st.subheader("🎶 More Trash (Curated by Noodles)")
                # add a gif here!!!!!!!!!!!!!
                st.subheader("")
                col1, col2, col3 = st.columns([1, 2, 1])

                with col2:
                    st.markdown(get_video_html("pictures/loadingcar.mp4",
                                width=300), unsafe_allow_html=True)

                st.markdown("""
                <div style='text-align: center;'>
                    <div style='
                        background-color: #fff9c4;
                        border: 2px dashed #d4af37;
                        padding: 12px 16px;
                        margin-top: 12px;
                        border-radius: 10px;
                        color: #444444;
                        font-family: Comic Sans MS, bold;
                        text-align: center;
                        box-shadow: 3px 3px 5px rgba(0,0,0,0.2);
                        display: inline-block;
                    '>
                        🐾 Still working on this... 🐾 
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.subheader("")
                st.markdown(
                    "<div style='text-align:center; font-size:20px;'>ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ</div>", unsafe_allow_html=True)
                st.subheader("")
                # for recommendations
                # !!! not working !!!
                # try recommendations based off top 5 artists

            else:
                st.error("Something went wrong. Please check the playlist link.")

st.text("")
st.markdown(
    "<div style='text-align:center; font-size:20px;'>ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ ᓚᘏᗢ</div>", unsafe_allow_html=True)

st.subheader("")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown(get_video_html("pictures/jumpingcar.mp4"),
                unsafe_allow_html=True)

st.text("")

st.subheader("👩🏻‍💻 About this project ")
st.text("")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #b35929 0%, #cc7744 100%);
    color: #fffbe6;
    font-family: 'Comic Sans MS';
    font-size: 16px;
    padding: 25px;
    margin: 30px auto;
    border-radius: 20px;
    width: 80%;
    box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    text-align: center;
    border: 2px dashed #ffd699;
">
    <p style="font-size: 20px; font-weight: bold; margin-bottom: 15px;">hiiiii!!</p>
    turning literally everything about my rude orange cat, <b>Noodles</b>, is kind of my brand. <br><br>
    he’s nosy, dramatic, and wildly talented at sticking his face where it absolutely doesn’t belong — like right into my food 🍜😾<br><br>
    sooo of course, <b>Noodle Poodle</b> feels very entitled to give his totally unsolicited (and possibly judgmental) opinions on your playlist. <br>
    whether you wanted them or not… hehe 💁‍♀️🐾🎧
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
