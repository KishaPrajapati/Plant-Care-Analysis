import streamlit as st
import pandas as pd
import os
from PIL import Image

# Load plant dataset
df = pd.read_csv("plant_data.csv")

# Folder containing plant images
IMAGE_FOLDER = "plant_images"

def fetch_image(plant_name):
    """Fetch plant image from local storage."""
    img_filename = f"{plant_name.lower().replace(' ', '_')}.jpg"
    img_path = os.path.join(IMAGE_FOLDER, img_filename)
    
    # Check if the image file exists before returning
    if os.path.exists(img_path) and os.path.getsize(img_path) > 0:
        return img_path
    return None  # Return None if image is missing

# Streamlit UI
# st.title("Plant Care Analysis")
st.markdown("<h1 style='text-align: center; color: darkgreen;'>🌱 Plant Care Analysis </h1>", unsafe_allow_html=True)
st.sidebar.header("🔍 Search & Filter Plants")

search_query = st.sidebar.text_input("Enter plant name")

# Filters
st.sidebar.markdown("<hr style='border: dashed 1px #A9A9A9;'>", unsafe_allow_html=True)
soil_filter = st.sidebar.multiselect("🌎 Select Soil Type", df["Soil Type"].unique())
water_filter = st.sidebar.multiselect("💧 Select Watering Needs", df["Watering"].unique())
st.sidebar.markdown("<hr style='border: dashed 1px #A9A9A9;'>", unsafe_allow_html=True)

def filter_plants(df):
    if search_query:
        df = df[df['Plant Name'].str.contains(search_query, case=False, na=False)]
    if soil_filter:
        df = df[df['Soil Type'].isin(soil_filter)]
    if water_filter:
        df = df[df['Watering'].isin(water_filter)]
    return df

# Sidebar button to open plant.py
st.sidebar.header(" How's Your Plant?")
if st.sidebar.button("Check Your Plant 🌱"):
    os.system("streamlit run plant.py")

st.sidebar.markdown("<hr style='border: dashed 1px #A9A9A9;'>", unsafe_allow_html=True)
# Check if a plant is selected
if "selected_plant" not in st.session_state:
    st.session_state["selected_plant"] = None

# If a plant is selected, show only that plant
if st.session_state["selected_plant"]:
    selected_plant = st.session_state["selected_plant"]
    plant_details = df[df['Plant Name'] == selected_plant].iloc[0]
    
    # Display the selected plant image
    # st.subheader(f"Details for {selected_plant}")
    st.markdown(f"<h2 style='text-align: center; color: ;'>🌿 {selected_plant} - Plant Details 🌿</h2>", unsafe_allow_html=True)
    st.markdown("---")
    img_path = fetch_image(selected_plant)
    if img_path:
        st.image(img_path, caption=selected_plant, use_container_width=True)
    else:
        st.write("Image not available")

    # Display plant details
    st.markdown(f"""
    <div style="background-color: #f0f7f4; padding: 10px; border-radius: 10px;">
    <p><strong>🟢 Soil Type:</strong> <span style="color: #008000;">{plant_details['Soil Type']}</span></p>
    <p><strong>💦 Watering Needs:</strong> <span style="color: #1E90FF;">{plant_details['Watering']}</span></p>
    <p><strong>🌡 Temperature Range:</strong> <span style="color: #FF4500;">{plant_details['Temperature']}</span></p>
    <p><strong>☀ Sunlight Hours:</strong> <span style="color: #FFD700;">{plant_details['Sunlight Hours']}</span> hours/day</p>
    <p><strong>📈 Growth Rate:</strong> <span style="color: #8B0000;">{plant_details['Growth Rate']}</span></p>
    <p><strong>🌿 Height of the Plant (in cm):</strong> <span style="color: #4B0082;">{plant_details['Height (cm)']}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Favorite button
    if st.button("Save to Favorites"):
        if "favorites" not in st.session_state:
            st.session_state["favorites"] = []
        if selected_plant not in st.session_state["favorites"]:
            st.session_state["favorites"].append(selected_plant)
            st.success(f"{selected_plant} added to favorites!")

    # Button to go back to full plant list
    if st.button("Back to Plant List"):
        st.session_state["selected_plant"] = None
        st.rerun()  # Updated from st.experimental_rerun()

# If no plant is selected, show the full plant list
else:
    filtered_df = filter_plants(df)
    st.subheader("Plant List")
    cols = st.columns(3)

    for i, row in filtered_df.iterrows():
        with cols[i % 3]:
            plant_name = row["Plant Name"]
            img_path = fetch_image(plant_name)

            if img_path:
                try:
                    img = Image.open(img_path)
                    st.image(img, caption=plant_name, use_container_width=True)
                except Exception:
                    st.write("Error loading image")
            else:
                st.write("Image not available")

            # Ensure unique keys for buttons
            if st.button(f"View Details {plant_name}", key=f"btn_{plant_name}"):
                st.session_state["selected_plant"] = plant_name
                st.rerun()  # Updated from st.experimental_rerun()

# Display Favorite Plants in Sidebar
st.sidebar.subheader("🌟 Favorite Plants")
if "favorites" in st.session_state and st.session_state["favorites"]:
    for fav in st.session_state["favorites"]:
       st.sidebar.markdown(f"✅ {fav}")
else:
    st.sidebar.write("No favorite plants added yet.")
