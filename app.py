import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hotel Recommender", layout="wide")

st.markdown("""
<style>
.main-title {
    font-size:40px;
    font-weight:700;
    margin-bottom:10px;
    color:white;
}

.card {
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-weight:600;
    font-size:18px;
    cursor:pointer;
    transition:0.3s;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
}

.card:hover {
    transform:scale(1.05);
    box-shadow:0px 6px 18px rgba(0,0,0,0.25);
}

.green { background-color:#28a745; color:white; }
.blue { background-color:#007bff; color:white; }
.yellow { background-color:#ffc107; color:black; }
.red { background-color:#dc3545; color:white; }

.hotel-card {
    background:#ffffff;
    padding:18px;
    border-radius:12px;
    margin-bottom:12px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.12);
    color:#222;   /* IMPORTANT */
}

.hotel-card h4 {
    color:#111;
    margin-bottom:8px;
}

.hotel-card p {
    color:#333;
    margin:4px 0;
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)


# LOAD DATA
merged = pd.read_csv(r"C:\Users\ASUS\Downloads\final_hotels.csv")

# SENTIMENT LOGIC
def sentiment_from_rating(rating):
    if rating >= 8:
        return "Highly Recommended"
    elif rating >= 7:
        return "Recommended"
    elif rating >= 6:
        return "Average"
    else:
        return "Not Recommended"

merged["sentiment"] = merged["hotel_rating"].apply(sentiment_from_rating)

# UI TITLE
st.markdown('<div class="main-title">🏨 NLP Hotel Recommendation System</div>', unsafe_allow_html=True)
st.write("Search a famous tourist place and explore hotels by recommendation level.")

user_input = st.text_input("Enter Famous Location (Example: Taj Mahal)")

if user_input:
    results = merged[
        merged["famous_place"].str.contains(user_input, case=False)
    ]

    # REMOVE REPEATED HOTELS
    results = results.drop_duplicates(subset=["hotel_name"])

    if results.empty:
        st.warning("No hotels found near this location.")

    else:
        st.subheader("Choose Recommendation Level")

        col1, col2, col3, col4 = st.columns(4)

        selected_sentiment = None

        with col1:
            if st.button("🟢 Highly Recommended"):
                selected_sentiment = "Highly Recommended"

        with col2:
            if st.button("🔵 Recommended"):
                selected_sentiment = "Recommended"

        with col3:
            if st.button("🟡 Average"):
                selected_sentiment = "Average"

        with col4:
            if st.button("🔴 Not Recommended"):
                selected_sentiment = "Not Recommended"

        if selected_sentiment:

            filtered = results[
                results["sentiment"] == selected_sentiment
            ].sort_values(by="hotel_rating", ascending=False)

            st.subheader(f"{selected_sentiment} Hotels")

            for _, row in filtered.iterrows():
                st.markdown(f"""
                <div class="hotel-card">
                    <h4>{row['hotel_name']}</h4>
                    <p><b>📍Location:</b> {row['city']}</p>
                    <p><b>🧭Near:</b> {row['famous_place']}</p>
                    <p><b>⭐ Rating:</b> {row['hotel_rating']} 
                    &nbsp; | &nbsp; <b>🗳 Reviews:</b> {row['total_reviews']}</p>
                    <p><b>💬 Condition:</b> {row['Condition']}</p>
                    <p><b>🌱 Description:</b> {row['description']}</p>
                </div>
                """, unsafe_allow_html=True)



