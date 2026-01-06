import pickle
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🎬 Neon IMDB-style Recommender", layout="wide")
st.title("🎬 Neon AI-Powered Movie Dashboard")
st.markdown("Content-Based Filtering & Neon Effects")

# ------------------ SESSION STATE ------------------
if "results" not in st.session_state:
    st.session_state.results = []

# ------------------ LOAD DATA ------------------
@st.cache_resource
def load_data():
    movies = pickle.load(open("movie_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()

# ------------------ NIGHT/DAY MODE TOGGLE ------------------
st.sidebar.header("🌗 Appearance")
mode = st.sidebar.radio("Select Theme", ["Day Mode", "Neon Night Mode"])
night_mode = mode == "Neon Night Mode"

# ------------------ STYLING ------------------
if night_mode:
    bg_gradient = "linear-gradient(135deg, #0f0c29, #302b63, #24243e)"
    card_gradient = "linear-gradient(135deg, #ff6ec7, #ff00f7)"
    text_color = "#fff"
    badge_text_color = "#fff"
    shadow_color = "#ff00f7"
else:
    bg_gradient = "linear-gradient(135deg, #89f7fe, #66a6ff)"
    card_gradient = "linear-gradient(135deg, #ff9a9e, #fad0c4)"
    text_color = "#000"
    badge_text_color = "#fff"
    shadow_color = "#888"

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {bg_gradient};
            color: {text_color};
        }}
        .card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 10px 20px {shadow_color};
            transition: all 0.3s ease-in-out;
        }}
        .card img {{
            border-radius: 12px;
            transition: transform 0.3s ease-in-out;
        }}
        .card img:hover {{
            transform: scale(1.05);
        }}
        .stars {{
            color: gold;
            text-shadow: 0 0 5px gold;
        }}
        @media screen and (max-width: 800px) {{
            .scroll-container {{
                display: flex;
                overflow-x: auto;
                padding-bottom: 10px;
            }}
            .scroll-container::-webkit-scrollbar {{
                height: 8px;
            }}
            .scroll-container::-webkit-scrollbar-thumb {{
                background: #888;
                border-radius: 4px;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ FETCH YOUTUBE TRAILER ------------------
def fetch_youtube_trailer(tmdb_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={api_key}"
        data = requests.get(url, timeout=5).json()
        for video in data.get("results", []):
            if video["site"].lower() == "youtube" and video["type"].lower() == "trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
    except:
        pass
    return None

# ------------------ FETCH MOVIE DATA ------------------
@st.cache_data(show_spinner=False)
def fetch_movie_data(title):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(url, timeout=5).json()
        results = response.get("results")
        if results:
            movie = results[0]
            poster_path = movie.get("poster_path")
            poster_url = (
                f"https://image.tmdb.org/t/p/w500{poster_path}"
                if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
            )
            rating = movie.get("vote_average", 0)
            release_date = movie.get("release_date")
            release = release_date[:4] if release_date and release_date.strip() else "N/A"
            tmdb_id = movie.get("id")
            tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}" if tmdb_id else "#"
            trailer_url = fetch_youtube_trailer(tmdb_id) if tmdb_id else None
            return poster_url, rating, release, tmdb_link, trailer_url
        return "https://via.placeholder.com/500x750?text=No+Image", 0, "N/A", "#", None
    except:
        return "https://via.placeholder.com/500x750?text=No+Image", 0, "N/A", "#", None

# ------------------ RECOMMENDATION FUNCTION ------------------
def recommend(movie, selected_genre=None):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendations = []
    for idx, score in distances[1:30]:
        row = movies.iloc[idx]
        if selected_genre and selected_genre.lower() not in row["tags"].lower():
            continue
        recommendations.append({"title": row.title, "tags": row.tags, "score": round(score, 3)})
        if len(recommendations) == 10:
            break
    return recommendations

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filters")
genres = ["All", "Action", "Comedy", "Drama", "Romance", "Thriller", "Horror", "Sci-Fi"]
selected_genre = st.sidebar.selectbox("Select Genre", genres)
if selected_genre == "All":
    selected_genre = None

# ------------------ SEARCH BOX ------------------
movie_list = sorted(movies["title"].values)
selected_movie = st.selectbox("Search or select a movie", movie_list)

# ------------------ SHOW RECOMMENDATIONS BUTTON ------------------
if st.button("🚀 Show Recommendations"):
    with st.spinner("Fetching movies..."):
        recs = recommend(selected_movie, selected_genre)
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda x: (x, fetch_movie_data(x["title"])), recs))
        st.session_state.results = results

# ------------------ DISPLAY RESULTS ------------------
if st.session_state.results:
    st.subheader("🎯 Recommended Movies")
    results = st.session_state.results
    chunk_size = 5
    genre_colors = {
        "Action": "#ff073a",
        "Comedy": "#ff8c00",
        "Drama": "#ffde03",
        "Romance": "#ff1493",
        "Thriller": "#8a2be2",
        "Horror": "#ff4500",
        "Sci-Fi": "#00ffff",
    }

    for i in range(0, len(results), chunk_size):
        row = results[i:i+chunk_size]
        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        cols = st.columns(len(row))
        for col, (rec, movie_data) in zip(cols, row):
            poster_url, rating, release, tmdb_link, trailer_url = movie_data
            with col:
                tags_html = ""
                for tag in rec["tags"].split(","):
                    tag_clean = tag.strip()
                    color = genre_colors.get(tag_clean, "#adb5bd")
                    tags_html += f'<span style="background-color:{color}; color:{badge_text_color}; padding:3px 8px; margin:2px; border-radius:6px; font-size:13px; font-weight:bold;">{tag_clean}</span> '
                st.markdown(
                    f"""
                    <div class="card" style="text-align:center; margin-bottom:25px; padding:12px; border-radius:15px;
                        box-shadow: 0 0 15px {shadow_color}; background: {card_gradient}; color:{text_color};">
                        <a href="{tmdb_link}" target="_blank" style="text-decoration:none; color:{text_color};">
                            <img src="{poster_url}" width="180px" style="border-radius:12px; margin-bottom:10px;">
                            <h4>{rec['title']} ({release})</h4>
                        </a>
                        <div>{tags_html}</div>
                        <p style="margin:3px;"><span class="stars">{"★"*int(round(rating/2))}{"☆"*(5-int(round(rating/2)))}</span></p>
                        <p style="color:lime; font-weight:bold;">Similarity Score: {rec['score']}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                if trailer_url:
                    st.markdown(f'<a href="{trailer_url}" target="_blank" style="color:#00ffff; font-weight:bold;">🎥 Watch Trailer on YouTube</a>', unsafe_allow_html=True)
                    st.video(trailer_url, start_time=0)
        st.markdown('</div>', unsafe_allow_html=True)
