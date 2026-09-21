import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Restaurant Recommendation System",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():

    data = pd.read_csv("restaurants_processed.csv")

    # Remove extra spaces from column names
    data.columns = data.columns.str.strip()

    return data


restaurant_df = load_data()

# -----------------------------
# TITLE
# -----------------------------

st.title("🍽️ Restaurant Recommendation System")

st.write(
    "Find restaurants based on your city, cuisine, budget, and rating preferences."
)

st.divider()

# -----------------------------
# USER INPUTS
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    city = st.selectbox(
        "📍 Select City",
        sorted(restaurant_df["City"].dropna().unique())
    )

    cuisine_options = sorted(
        set(
            cuisine.strip()
            for cuisines in restaurant_df["Cuisine"].dropna()
            for cuisine in cuisines.split(",")
        )
    )

    cuisine = st.selectbox(
        "🍽️ Select Cuisine",
        cuisine_options
    )

with col2:

    budget = st.number_input(
        "💰 Target Budget (₹)",
        min_value=50,
        max_value=5000,
        value=300,
        step=50
    )

    min_rating = st.slider(
        "⭐ Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=3.5,
        step=0.1
    )

# -----------------------------
# RECOMMENDATION FUNCTION
# -----------------------------

def recommend_restaurants(
    city,
    cuisine,
    budget,
    min_rating,
    num_recommendations=5
):

    results = restaurant_df.copy()

    # -----------------------------
    # CITY
    # -----------------------------

    results = results[
        results["City"].str.lower() == city.lower()
    ]

    if results.empty:
        return pd.DataFrame()

    # -----------------------------
    # CUISINE MATCH
    # -----------------------------

    results["Cuisine Score"] = results["Cuisine"].str.lower().apply(
        lambda x: 1.0 if cuisine.lower() in x else 0.0
    )

    # -----------------------------
    # RATING
    # -----------------------------

    results["Rating Score"] = (
        results["Overall Rating"] / 5
    )

    # -----------------------------
    # BUDGET
    # -----------------------------

    results["Budget Score"] = 1 - (
        abs(results["Average Price"] - budget) / budget
    )

    results["Budget Score"] = results["Budget Score"].clip(0, 1)

    # -----------------------------
    # POPULARITY
    # -----------------------------

    total_votes = (
        results["Dining Votes"] +
        results["Delivery Votes"]
    )

    max_votes = total_votes.max()

    if max_votes > 0:

        results["Popularity Score"] = (
            total_votes / max_votes
        )

    else:

        results["Popularity Score"] = 0

    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    results["Final Score"] = (
        0.35 * results["Cuisine Score"] +
        0.30 * results["Rating Score"] +
        0.20 * results["Budget Score"] +
        0.15 * results["Popularity Score"]
    )

    # -----------------------------
    # MINIMUM RATING
    # -----------------------------

    filtered = results[
        results["Overall Rating"] >= min_rating
    ]

    if not filtered.empty:
        results = filtered

    # -----------------------------
    # SORT
    # -----------------------------

    results = results.sort_values(
        by="Final Score",
        ascending=False
    )

    return results.head(num_recommendations)


# -----------------------------
# RECOMMEND BUTTON
# -----------------------------

if st.button(
    "🔍 Find Recommended Restaurants",
    type="primary"
):

    recommendations = recommend_restaurants(
        city,
        cuisine,
        budget,
        min_rating
    )

    st.divider()

    st.subheader("🏆 Recommended Restaurants")

    if recommendations.empty:

        st.warning(
            "No restaurants found for the selected city."
        )

    else:

        for _, restaurant in recommendations.iterrows():

            st.markdown(
                f"""
                ### 🍽️ {restaurant['Restaurant Name']}

                **📍 City:** {restaurant['City']}  
                
                **🍴 Cuisine:** {restaurant['Cuisine']}  
                
                **⭐ Rating:** {restaurant['Overall Rating']:.2f}  
                
                **💰 Average Price:** ₹{restaurant['Average Price']:.2f}  
                
                **📊 Recommendation Score:** {restaurant['Final Score']:.3f}
                """
            )

            st.divider()