import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import re

# Title of the app
st.title("📱 Flipkart Mobile Sales")

# Load cleaned CSV
df = pd.read_csv("C:/Users/bhumi/OneDrive/Desktop/professional/internship/mobile/mobile_cleaned.csv")


# Normalize Product Name by removing color keywords for consistent Model Name
def clean_model_name(name):
    color_words = [
        'black', 'blue', 'white', 'green', 'red', 'purple', 'grey', 'silver',
        'gold', 'pink', 'yellow', 'coral', 'midnight', 'deep', 'starlight',
        'titanium', 'graphite', 'bronze', 'orange', 'cyan'
    ]
    name_lower = name.lower()
    for color in color_words:
        pattern = rf"\\b{color}\\b"
        name_lower = re.sub(pattern, '', name_lower)
    name_lower = re.sub(r'\(\s*,', '(', name_lower)
    name_lower = re.sub(r',\s*\)', ')', name_lower)
    name_lower = re.sub(r'\(\s*\)', '', name_lower)
    name_lower = re.sub(r'\s+', ' ', name_lower).strip()
    return name_lower.title()

df['Model Name'] = df['Product Name'].apply(clean_model_name)

# Extract brand from normalized model name
df['Brand'] = df['Model Name'].apply(lambda x: x.split()[0])

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select Chart", [
    "Top 10 Mobile Brands",
    "Star Rating Pie Chart",
    "Price Comparison (Bar Chart)"
])

# Chart 1 - Bar Chart: Top 10 Brands
if options == "Top 10 Mobile Brands":
    st.subheader("📊 Top 10 Mobile Brands")
    brand_counts = df['Brand'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(brand_counts.index, brand_counts.values, color='skyblue')
    ax.set_title('Top 10 Mobile Brands')
    ax.set_xlabel('Brand')
    ax.set_ylabel('Number of Products')
    ax.set_xticks(range(len(brand_counts.index)))
    ax.set_xticklabels(brand_counts.index, rotation=45)
    st.pyplot(fig)

# Chart 2 - Pie Chart: Star Ratings
# Chart 2 - Pie Chart: Star Ratings
elif options == "Star Rating Pie Chart":
    st.subheader("⭐ Star Rating Distribution (Top 5)")

    stars = df['Stars'].value_counts().head(5)
    
    # Define fixed colors for the slices
    pie_colors = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0', '#f44336']  # Green, Blue, Orange, Purple, Red

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        stars,
        labels=stars.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=pie_colors,
        textprops={'color': 'black'}
    )
    ax.set_title("Top 5 Star Ratings")

    # Add a legend below the chart with custom color meaning
    legend_labels = [
        f"{stars.index[0]} Stars - Excellent (Green)",
        f"{stars.index[1]} Stars - Good (Blue)",
        f"{stars.index[2]} Stars - Average (Orange)",
        f"{stars.index[3]} Stars - Below Avg (Purple)",
        f"{stars.index[4]} Stars - Poor (Red)"
    ]
    ax.legend(wedges, legend_labels, title="Rating Legend", loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=2)

    st.pyplot(fig)



# Chart 3 - Grouped Bar Chart: Price Comparison
elif options == "Price Comparison (Bar Chart)":
    st.subheader("📊 Price Comparison by Brand")

    top_brands = df['Brand'].value_counts().head(15).index.tolist()
    selected_brand = st.selectbox("Choose a Brand", top_brands)

    brand_df = df[df['Brand'] == selected_brand].head(15)

    if not brand_df.empty:
        labels = brand_df['Model Name']
        actual = brand_df['Actual price']
        discount = brand_df['Discount price']

        x = range(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(x, actual, width=width, label='Actual Price', color='gray')
        ax.bar([i + width for i in x], discount, width=width, label='Discount Price', color='green')

        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title(f"Actual vs Discount Price – {selected_brand}")
        ax.set_xlabel("Mobile")
        ax.set_ylabel("Price (₹)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning(f"No data available for brand: {selected_brand}")



