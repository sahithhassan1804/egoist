import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CineSphere",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM DARK UI
# =========================================================

st.markdown("""
<style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.18), transparent 28%),
            radial-gradient(circle at 90% 20%, rgba(219, 39, 119, 0.14), transparent 28%),
            linear-gradient(135deg, #080a10 0%, #0d0f18 50%, #090a10 100%);
        color: #f5f5f7;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }


    /* ---------- HERO ---------- */

    .hero {
        padding: 55px 35px;
        margin-bottom: 45px;

        background:
            linear-gradient(
                135deg,
                rgba(76, 29, 149, 0.70),
                rgba(157, 23, 77, 0.65)
            );

        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 28px;

        text-align: center;

        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .hero-icon {
        font-size: 48px;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #ddd6fe;
        letter-spacing: 0.3px;
    }


    /* ---------- SECTION HEADERS ---------- */

    .section-title {
        font-size: 30px;
        font-weight: 750;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #aeb4c7;
        font-size: 15px;
        margin-bottom: 20px;
    }


    /* ---------- SELECTBOX LABELS ---------- */

    label {
        color: #f5f5f7 !important;
        font-weight: 600 !important;
    }


    /* ---------- SELECTBOX ---------- */

    div[data-baseweb="select"] > div {
        background-color: #171923 !important;
        border: 1px solid #35394b !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        min-height: 50px !important;
    }

    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }

    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }


    /* ---------- BUTTON ---------- */

    div.stButton > button {
        width: 100%;

        height: 58px;

        border: none;
        border-radius: 16px;

        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #a855f7,
                #db2777
            );

        color: #ffffff;

        font-size: 17px;
        font-weight: 700;

        box-shadow:
            0 10px 30px rgba(168, 85, 247, 0.25);

        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 15px 40px rgba(219, 39, 119, 0.35);

        border: none;
        color: #ffffff;
    }


    /* ---------- DIVIDER ---------- */

    .divider {
        height: 1px;
        background: #292d3b;
        margin: 45px 0 30px 0;
    }


    /* ---------- RECOMMENDATION HEADER ---------- */

    .recommendation-header {
        padding: 18px 22px;

        background:
            linear-gradient(
                90deg,
                rgba(124, 58, 237, 0.20),
                rgba(219, 39, 119, 0.15)
            );

        border-left: 4px solid #a855f7;
        border-radius: 12px;

        margin-bottom: 22px;
    }

    .recommendation-header-title {
        font-size: 22px;
        font-weight: 750;
        color: #ffffff;
    }

    .recommendation-header-subtitle {
        font-size: 13px;
        color: #aeb4c7;
        margin-top: 5px;
    }


    /* ---------- MOVIE CARDS ---------- */

    .movie-card {
        background:
            linear-gradient(
                145deg,
                #181b25,
                #12141c
            );

        border: 1px solid #292d3b;
        border-radius: 18px;

        padding: 22px;

        margin-bottom: 18px;

        min-height: 210px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.20);

        transition:
            transform 0.25s ease,
            border 0.25s ease,
            box-shadow 0.25s ease;
    }

    .movie-card:hover {
        transform: translateY(-4px);

        border: 1px solid #8b5cf6;

        box-shadow:
            0 15px 40px rgba(124, 58, 237, 0.20);
    }


    /* ---------- MOVIE RANK ---------- */

    .movie-rank {
        display: inline-block;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #db2777
            );

        color: white;

        padding: 5px 11px;

        border-radius: 20px;

        font-size: 12px;
        font-weight: 700;

        margin-bottom: 12px;
    }


    /* ---------- MOVIE TITLE ---------- */

    .movie-title {
        font-size: 21px;
        font-weight: 750;

        color: #ffffff;

        margin-bottom: 9px;

        line-height: 1.3;
    }


    /* ---------- GENRE ---------- */

    .movie-genre {
        color: #b9c0d4;

        font-size: 13px;

        margin-bottom: 18px;
    }


    /* ---------- STATS ---------- */

    .movie-stats {
        display: flex;
        flex-wrap: wrap;

        gap: 9px;
    }

    .stat {
        background: #202330;

        border: 1px solid #303548;

        border-radius: 9px;

        padding: 7px 10px;

        font-size: 12px;

        color: #dce1ee;
    }

    .score {
        background: rgba(168, 85, 247, 0.14);

        border: 1px solid rgba(168, 85, 247, 0.35);

        color: #c4b5fd;
    }


    /* ---------- INFO BOX ---------- */

    .info-box {
        padding: 18px 20px;

        background: rgba(124, 58, 237, 0.08);

        border: 1px solid rgba(124, 58, 237, 0.20);

        border-radius: 14px;

        color: #c8cde0;

        font-size: 13px;

        margin-top: 20px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        margin-top: 55px;

        padding: 30px 20px;

        text-align: center;

        background: #151720;

        border: 1px solid #292d3b;

        border-radius: 18px;

        color: #f5f5f7;
    }

    .footer-title {
        font-size: 20px;

        margin-bottom: 16px;

        color: #ffffff;
    }

    .footer-powered {
        font-size: 14px;

        color: #aeb4c7;

        margin-bottom: 10px;
    }

    .footer-tech {
        display: flex;

        justify-content: center;

        align-items: center;

        gap: 10px;

        flex-wrap: wrap;

        font-size: 14px;

        color: #cdd2e3;
    }

    .footer-tech span {
        color: #c4b5fd;

        font-weight: 600;
    }

    .footer-copy {
        margin-top: 16px;

        font-size: 12px;

        color: #737b92;
    }


    /* ---------- REMOVE STREAMLIT BRANDING ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_movie_data():

    data = pd.read_csv("movies_processed.csv")

    data.columns = data.columns.str.strip()

    return data


# =========================================================
# LOAD ML MODELS
# =========================================================

@st.cache_resource
def load_models():

    with open("hybrid_recommendations.pkl", "rb") as f:
        hybrid_recommendations = pickle.load(f)

    return hybrid_recommendations


# =========================================================
# LOAD EVERYTHING
# =========================================================

try:

    movie_data = load_movie_data()
    hybrid_recommendations = load_models()

except Exception as e:

    st.error("⚠️ Unable to load the movie data or model files.")

    st.code(str(e))

    st.stop()


# =========================================================
# CLEAN DATA
# =========================================================

movie_data["Title"] = movie_data["Title"].astype(str)

movie_data["Genres"] = movie_data["Genres"].fillna("").astype(str)

movie_data["Average_Rating"] = pd.to_numeric(
    movie_data["Average_Rating"],
    errors="coerce"
).fillna(0)

movie_data["Rating_Count"] = pd.to_numeric(
    movie_data["Rating_Count"],
    errors="coerce"
).fillna(0)


# =========================================================
# HELPER: GET GENRES
# =========================================================

def extract_genres(value):

    value = str(value).strip()

    if not value:
        return []

    # Dataset may contain either:
    # Animation Children's Comedy
    # OR
    # Animation|Children's|Comedy

    if "|" in value:

        parts = value.split("|")

    else:

        # MovieLens genres are single-token genre names,
        # except combinations such as Film-Noir.
        parts = value.split()

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


# Create genre list for every movie

movie_data["_Genre_List"] = movie_data["Genres"].apply(
    extract_genres
)


# =========================================================
# GET UNIQUE GENRES
# =========================================================

all_genres = set()

for genres in movie_data["_Genre_List"]:

    for genre in genres:

        all_genres.add(genre)


genre_options = sorted(all_genres)


# =========================================================
# HERO SECTION
# =========================================================
st.html("""
<div class="hero">

    <div class="hero-icon">
        🎞️
    </div>

    <div class="hero-title">
        CineSphere
    </div>

    <div class="hero-subtitle">
        Explore movies. Discover your next favorite.
    </div>

</div>
""")


# =========================================================
# SELECTION SECTION
# =========================================================

st.markdown(
    '<div class="section-title">🎭 Choose Your Movie</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Start with a genre and choose a movie you already like. '
    'Our hybrid recommendation system will find similar movies for you.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# GENRE SELECTOR
# =========================================================

selected_genre = st.selectbox(
    "🎭 Select a Genre",
    genre_options,
    index=0,
    key="genre_selector"
)


# =========================================================
# FILTER MOVIES BY GENRE
# =========================================================

genre_movies = movie_data[
    movie_data["_Genre_List"].apply(
        lambda genres: selected_genre in genres
    )
].copy()


genre_movies = genre_movies.sort_values(
    by="Title"
)


# =========================================================
# MOVIE SELECTOR
# =========================================================

movie_options = genre_movies["Title"].tolist()


if len(movie_options) == 0:

    st.warning(
        "No movies were found for this genre."
    )

    st.stop()


selected_movie = st.selectbox(
    "🎬 Select a Movie",
    movie_options,
    index=0,
    key="movie_selector"
)


# =========================================================
# SELECTED MOVIE INFORMATION
# =========================================================

selected_row = movie_data[
    movie_data["Title"] == selected_movie
].iloc[0]


selected_rating = selected_row["Average_Rating"]

selected_votes = int(
    selected_row["Rating_Count"]
)

selected_genres = selected_row["Genres"]


st.html(f"""
<div class="info-box">

    <b>Selected Movie:</b> {selected_movie}
    &nbsp;&nbsp; • &nbsp;&nbsp;

    <b>Genres:</b> {selected_genres}
    &nbsp;&nbsp; • &nbsp;&nbsp;

    <b>Rating:</b> ⭐ {selected_rating:.2f}
    &nbsp;&nbsp; • &nbsp;&nbsp;

    <b>Ratings:</b> {selected_votes:,}

</div>
""")


# =========================================================
# RECOMMENDATION FUNCTION
# =========================================================

def get_hybrid_recommendations(
    movie_title,
    selected_genre,
    number_of_recommendations=10
):

    # Find the selected movie
    movie_matches = movie_data[
        movie_data["Title"] == movie_title
    ]

    if movie_matches.empty:
        return pd.DataFrame()

    selected_movie_id = int(movie_matches.iloc[0]["MovieID"])

    # Get the precomputed top-100 hybrid recommendations.
    # These were generated using 50% content + 50% collaborative filtering.
    stored_recommendations = hybrid_recommendations.get(
        selected_movie_id,
        []
    )

    if not stored_recommendations:
        return pd.DataFrame()

    results = pd.DataFrame(stored_recommendations)

    if results.empty:
        return pd.DataFrame()

    # Add rating and genre information from the processed movie dataset.
    movie_info = movie_data[
        [
            "MovieID",
            "Title",
            "Genres",
            "Average_Rating",
            "Rating_Count",
            "_Genre_List"
        ]
    ].copy()

    results = results.merge(
        movie_info,
        on="MovieID",
        how="left",
        suffixes=("", "_data")
    )

    # Filter recommendations to the selected genre.
    results = results[
        results["_Genre_List"].apply(
            lambda genres: selected_genre in genres
        )
    ].copy()

    # Do not recommend the movie the user selected.
    results = results[
        results["Title"] != movie_title
    ]

    # Highest precomputed hybrid score first.
    results = results.sort_values(
        by="Hybrid_Score",
        ascending=False
    )

    return results.head(number_of_recommendations)


# =========================================================
# RECOMMEND BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

recommend_clicked = st.button(
    "🎯  Find Similar Movies",
    key="recommend_button"
)


# =========================================================
# SHOW RECOMMENDATIONS
# =========================================================

if recommend_clicked:

    with st.spinner(
        "🔎 Finding movies you may enjoy..."
    ):

        recommendations = get_hybrid_recommendations(
            selected_movie,
            selected_genre,
            10
        )


    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


    if recommendations.empty:

        st.warning(
            "No recommendations were found for this movie."
        )

    else:
        st.html(f"""
<div class="recommendation-header">

    <div class="recommendation-header-title">
        🍿 Movies similar to {selected_movie}
    </div>

    <div class="recommendation-header-subtitle">
        Genre: {selected_genre}
        &nbsp; • &nbsp;
        Hybrid recommendation using
        content + collaborative filtering
    </div>

</div>
""")

      
        # -----------------------------------------
        # DISPLAY MOVIE CARDS
        # -----------------------------------------

        for rank, (_, movie) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            title = movie["Title"]

            genres = movie["Genres"]

            rating = movie["Average_Rating"]

            rating_count = int(
                movie["Rating_Count"]
            )

            hybrid = movie["Hybrid_Score"]

            st.html(f"""
<div class="movie-card">

    <div class="movie-rank">
        #{rank}
    </div>

    <div class="movie-title">
        🎬 {title}
    </div>

    <div class="movie-genre">
        {genres}
    </div>

    <div class="movie-stats">

        <div class="stat">
            ⭐ Rating: {rating:.2f}
        </div>

        <div class="stat">
            👥 Ratings: {rating_count:,}
        </div>

        <div class="stat score">
            🧠 Match Score: {hybrid:.3f}
        </div>

    </div>

</div>
""")


            

        # -----------------------------------------
        # MODEL INFORMATION
        # -----------------------------------------

        st.html("""
<div class="info-box">

    <b>🧠 How the recommendations work:</b>

    The system combines two machine-learning
    approaches. <b>Content-based filtering</b>
    compares movie titles and genres using
    TF-IDF and cosine similarity, while
    <b>collaborative filtering</b> uses
    user-rating patterns.

    <br><br>

    <b>Hybrid Score = 50% Content Similarity
    + 50% Collaborative Similarity</b>

</div>
""")


# =========================================================
# FOOTER
# =========================================================
st.html("""
<div class="footer">

    <div class="footer-title">
        🎞️ <b>CineSphere</b>
    </div>

    <div class="footer-powered">
        Powered by Machine Learning
    </div>

    <div class="footer-tech">

        <span>TF-IDF</span>

        <span>•</span>

        <span>Cosine Similarity</span>

        <span>•</span>

        <span>Collaborative Filtering</span>

        <span>•</span>

        <span>Hybrid Recommendation</span>

    </div>

    <div class="footer-copy">
        Movie Recommendation System
    </div>

</div>
""")