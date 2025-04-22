import streamlit as st
import pandas as pd
import plotly.express as px
import os

DATA_PATH = "data/products.csv"
if not os.path.exists(DATA_PATH):
    st.error("🚫 'products.csv' not found. Please add it under the 'data' folder.")
    st.stop()

# Load data
data = pd.read_csv(DATA_PATH)

# Sidebar
st.sidebar.title("📱 Smart Product Finder")

# Budget
budget = st.sidebar.slider("💰 Your Budget", 5000, 50000, 10000, step=1000)

# Preferences
st.sidebar.markdown("### 🎯 Your Preferences")
camera = st.sidebar.checkbox("📸 High-quality Camera")
performance = st.sidebar.checkbox("⚡ Good Performance")
battery = st.sidebar.checkbox("🔋 Long Battery")
display = st.sidebar.checkbox("🖥️ Good Display")

ram = st.sidebar.selectbox("💾 RAM", ["Any", "4GB", "6GB", "8GB", "12GB"])
storage = st.sidebar.selectbox("📂 Storage", ["Any", "64GB", "128GB", "256GB"])
brand = st.sidebar.selectbox("🏷️ Brand", ["Any"] + sorted(data['brand'].unique()))

# Search Bar
search_query = st.text_input("🔍 Search for a product")

# Filter logic
filtered_data = data[data['price'] <= budget]

if camera:
    filtered_data = filtered_data[filtered_data['features'].str.contains("camera", case=False, na=False)]
if performance:
    filtered_data = filtered_data[filtered_data['features'].str.contains("performance", case=False, na=False)]
if battery:
    filtered_data = filtered_data[filtered_data['features'].str.contains("battery", case=False, na=False)]
if display:
    filtered_data = filtered_data[filtered_data['features'].str.contains("display", case=False, na=False)]
if ram != "Any":
    filtered_data = filtered_data[filtered_data['ram'] == ram]
if storage != "Any":
    filtered_data = filtered_data[filtered_data['storage'] == storage]
if brand != "Any":
    filtered_data = filtered_data[filtered_data['brand'].str.lower() == brand.lower()]
if search_query:
    filtered_data = filtered_data[filtered_data['product_name'].str.contains(search_query, case=False)]

# Sort
filtered_data = filtered_data.sort_values(by=['rating', 'value_for_money'], ascending=False)

# Title
st.title("📊 Product Results Based on Your Preferences")

# Best Pick
if st.button("🧠 Recommend Best Pick"):
    if not filtered_data.empty:
        best = filtered_data.iloc[0]
        st.success(f"🔥 Best Pick: {best['product_name']} - ₹{best['price']}")
        st.write(best[['product_name', 'price', 'rating', 'value_for_money', 'features']])
    else:
        st.warning("No product found for recommendation.")

# Display Results
if not filtered_data.empty:
    def render_star(rating):
        full = int(rating)
        return "⭐" * full + "✩" * (5 - full)

    display_df = filtered_data.copy()
    display_df['Rating'] = display_df['rating'].apply(render_star)
    st.dataframe(display_df[['product_name', 'price', 'Rating', 'features']])
else:
    st.warning("😕 No results found. Adjust filters.")

# Compare Section
st.subheader("📱 Compare Phones (Full Specs)")
selected = st.multiselect("Select phones to compare", filtered_data['product_name'].unique())

if selected:
    compare = filtered_data[filtered_data['product_name'].isin(selected)]
    st.table(compare[['product_name', 'price', 'rating', 'ram', 'storage', 'processor', 'battery', 'features']])

# Price Distribution – moved to bottom
if not filtered_data.empty:
    st.subheader("📈 Price Distribution")
    fig = px.histogram(filtered_data, x='price', nbins=30, title='Price Range of Filtered Phones')
    st.plotly_chart(fig)
