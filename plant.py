import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Load plant data
plant_df = pd.read_csv("plant_data.csv")  # Ensure correct file path

# ✅ Initialize session state variables
if "plant_found" not in st.session_state:
    st.session_state.plant_found = False
if "plant_details" not in st.session_state:
    st.session_state.plant_details = None
if "selected_analysis" not in st.session_state:
    st.session_state.selected_analysis = None
if "user_plant_name_lower" not in st.session_state:
    st.session_state.user_plant_name_lower = None  # Initialize variable

# 🌿 **Modern UI**
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌱 Plant Health Analysis</h1>", unsafe_allow_html=True)
st.subheader("🔍 Enter Your Plant Name")
user_plant_name = st.text_input("Plant Name:")

# ✅ Check Plant
if st.button("Check Plant 🌿"):
    if user_plant_name:
        st.session_state.user_plant_name_lower = user_plant_name.strip().lower()
        plant_df["Plant Name Lower"] = plant_df["Plant Name"].str.lower()

        if st.session_state.user_plant_name_lower in plant_df["Plant Name Lower"].values:
            st.session_state.plant_found = True
            st.session_state.plant_details = plant_df[plant_df["Plant Name Lower"] == st.session_state.user_plant_name_lower].iloc[0]
            st.session_state.selected_analysis = None  # Reset analysis selection
            st.success(f"✅ {user_plant_name} found in the dataset.")
        else:
            st.session_state.plant_found = False
            st.session_state.plant_details = None
            st.error("❌ Plant not found in the dataset.")

# ✅ Show analysis options if plant is found
if st.session_state.plant_found:
    
    if st.session_state.selected_analysis is None:
        st.subheader("📊 Choose an Analysis Type")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🌼 Flowering & Fruiting Stages"):
                st.session_state.selected_analysis = "flowering"

        with col2:
            if st.button("📈 Growth Rate"):
                st.session_state.selected_analysis = "growth"

        with col3:
            if st.button("🌍 Environmental Factors"):
                st.session_state.selected_analysis = "environment"

if st.session_state.selected_analysis == "growth":
    st.write("## 📈 Growth Rate")
     # Separate button and logic for Growth Rate scatter plot
    if st.button("Growth Rate"):
        st.subheader("Sunlight Hours vs Growth Rate")

        # # Create scatter plot
        # growth_mapping = {"Slow": 1, "Medium": 2, "Fast": 3}
        # plant_df["Growth Rate Num"] = plant_df["Growth Rate"].map(growth_mapping)

        # fig, ax = plt.subplots(figsize=(8, 5))
        # sns.scatterplot(x=plant_df["Sunlight Hours"], y=plant_df["Growth Rate Num"], hue=plant_df["Plant Name"], palette="viridis", s=100, ax=ax)
        
        # ax.set_xlabel("Sunlight Hours")
        # ax.set_ylabel("Growth Rate (1=Slow, 2=Medium, 3=Fast)")
        # ax.set_title("Sunlight Hours vs Growth Rate")
        # ax.legend(title="Plant Name", bbox_to_anchor=(1.05, 1), loc="upper left")

        # # Show plot
        # st.pyplot(fig)
        growth_mapping = {"Slow": 1, "Medium": 2, "Fast": 3}
        plant_df["Growth Rate Num"] = plant_df["Growth Rate"].map(lambda x: growth_mapping.get(x, None))
        plant_df = plant_df.dropna(subset=["Growth Rate Num", "Sunlight Hours"])

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x=plant_df["Sunlight Hours"], y=plant_df["Growth Rate Num"], 
                    hue=plant_df["Plant Name"], palette="viridis", s=150, alpha=0.8, ax=ax)

        ax.set_xlabel("Sunlight Hours")
        ax.set_ylabel("Growth Rate (1=Slow, 2=Medium, 3=Fast)")
        ax.set_title("Sunlight Hours vs Growth Rate")
        ax.legend(title="Plant Name", bbox_to_anchor=(1.05, 1), loc="upper left", ncol=2)
        fig.tight_layout()

        st.pyplot(fig)
    st.subheader("📊 Enter Your Plant Growth Conditions")

    # Step 2: User inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        sunlight_hours = st.number_input("☀ Sunlight Hours", min_value=0, max_value=24, step=1, key="sunlight")

    with col2:
        soil_type = st.selectbox("🌱 Soil Type", ["Sandy", "Clay", "Loamy", "Silty", "Peaty"], key="soil")

    with col3:
        plant_height = st.number_input("📏 Height (cm)", min_value=0, max_value=500, step=1, key="height")

    # Step 3: Compare with Ideal Conditions
    if st.button("📊 Analyze Growth Conditions"):
        st.subheader("📊 Your Growth Condition vs. Ideal Conditions")

        plant_details = st.session_state.plant_details
        
        try:
            # Extract ideal conditions
            ideal_sunlight = int(plant_details["Sunlight Hours"])
            ideal_soil = plant_details["Soil Type"]
            ideal_height = int(plant_details["Height (cm)"]) if pd.notna(plant_details["Height (cm)"]) else 0

            # Convert categorical values to numeric for comparison
            soil_mapping = {"Sandy": 1, "Clay": 2, "Loamy": 3, "Silty": 4, "Peaty": 5}

            user_soil_numeric = soil_mapping.get(soil_type, 0)
            ideal_soil_numeric = soil_mapping.get(ideal_soil, 0)

            # Prepare data for graph
            categories = ["Sunlight (Hours)", "Soil Type", "Height (cm)"]
            user_values = [sunlight_hours, user_soil_numeric, plant_height]
            ideal_values = [ideal_sunlight, ideal_soil_numeric, ideal_height]

            # Plot comparison graph
            fig, ax = plt.subplots()
            bar_width = 0.3
            index = range(len(categories))

            ax.bar(index, user_values, bar_width, label="Your Input", color="blue")
            ax.bar([i + bar_width for i in index], ideal_values, bar_width, label="Ideal Conditions", color="green")

            ax.set_xlabel("Growth Factors")
            ax.set_ylabel("Values (Numeric Scale)")
            ax.set_title("Comparison: Your Input vs. Ideal Conditions")
            ax.set_xticks([i + bar_width / 2 for i in index])
            ax.set_xticklabels(categories)
            ax.legend()

            st.pyplot(fig)
            
            # Step 4: Determine growth rate
            deviation = abs(sunlight_hours - ideal_sunlight) + abs(user_soil_numeric - ideal_soil_numeric) + abs(plant_height - ideal_height)

            if deviation == 0:
                growth_rate = "Fast"
            elif deviation <= 10:
                growth_rate = "Moderate"
            else:
                growth_rate = "Slow"

            st.subheader(f"🌱 Growth Rate: **{growth_rate}**")

            # Step 5: Recommendations
            st.subheader("🌿 Recommendations")

            # Sunlight
            if sunlight_hours < ideal_sunlight:
                st.write(f"🔆 **Increase Sunlight:** Your plant needs at least **{ideal_sunlight} hours/day**.")
            elif sunlight_hours > ideal_sunlight:
                st.write(f"☀ **Too Much Sunlight:** Reduce to **{ideal_sunlight} hours/day** for best growth.")
            else:
                st.write("✅ **Sunlight Level is Perfect!**")

            # Soil
            if user_soil_numeric != ideal_soil_numeric:
                st.write(f"🌱 **Change Soil Type:** Your plant prefers **{ideal_soil} soil**.")

            # Height
            if plant_height < ideal_height:
                st.write(f"📏 **Increase Plant Height:** Your plant should ideally be **{ideal_height} cm**.")
            elif plant_height > ideal_height:
                st.write(f"📏 **Your plant is taller than usual!** Normal height: **{ideal_height} cm**.")
            else:
                st.write("✅ **Your plant's height is perfect!**")

        except KeyError as e:
            st.error(f"❌ Missing data in the dataset: {e}")

# ✅ **Flowering & Fruiting Stages Analysis**
if st.session_state.selected_analysis == "flowering":
    st.write("## 🌼 Flowering & Fruiting Stages Analysis")
    flowering_df = pd.read_csv("plant_flowering_fruiting.csv")  # Ensure correct file path

    # ✅ Convert plant names to lowercase for matching
    flowering_df["Plant Name Lower"] = flowering_df["Plant Name"].str.lower()

    if not st.session_state.user_plant_name_lower:
        st.error("❌ No plant name provided. Please enter a valid plant name.")
    else:
        # ✅ Find the plant details
        plant_data = flowering_df[flowering_df["Plant Name Lower"] == st.session_state.user_plant_name_lower]

        if plant_data.empty:
            st.error("❌ No flowering/fruition data found for this plant.")
        else:
            # ✅ Determine flowering/fruition type
            flowering = plant_data.iloc[0]["Flowering"]
            fruiting = plant_data.iloc[0]["Fruiting"]

            if flowering == "Yes" and fruiting == "Yes":
                flowering_type = "Flowering & Fruiting"
            elif flowering == "Yes":
                flowering_type = "Flowering Only"
            elif fruiting == "Yes":
                flowering_type = "Fruiting Only"
            else:
                flowering_type = "Neither Flowering nor Fruiting"

            st.subheader(f"🌱 **This plant is categorized as:** {flowering_type}")

            # ✅ Extract flowering & fruiting months
            flowering_months = plant_data.iloc[0]["Flowering Months"]
            fruiting_months = plant_data.iloc[0]["Fruiting Months"]

            # ✅ Display Flowering and Fruiting Seasons
            st.write(f"**🌼 Flowering Season:** {plant_data.iloc[0]['Flowering Season']}")
            if fruiting == "Yes":
                st.write(f"**🍎 Fruiting Season:** {plant_data.iloc[0]['Fruiting Season']}")

            # ✅ Display Soil Nutrient Recommendations
            st.write(f"**🌱 Soil Nutrient Requirements:** {plant_data.iloc[0]['Soil Nutrient']}")

            # ✅ Display Leaf Color Analysis
            leaf_color = plant_data.iloc[0]["Leaf Color"]
            st.write(f"**🍃 Leaf Color:** {leaf_color}")
            if leaf_color == "Yellow":
                st.warning("⚠️ Yellow leaves may indicate nutrient deficiency (e.g., nitrogen, iron). Consider adding fertilizers.")
            elif leaf_color == "Brown":
                st.warning("⚠️ Brown leaves may indicate overwatering or root rot. Check soil drainage.")
            elif leaf_color == "Dark Green":
                st.success("✅ Dark green leaves indicate healthy growth. Maintain current care routine.")
            elif leaf_color == "Light Green":
                st.warning("⚠️ Light green leaves may indicate insufficient sunlight or nutrients.")

            # ✅ Plot Flowering & Fruiting Trends
            st.subheader("📊 Flowering & Fruiting Trends Over the Year")

            # Define months order
            months_order = ["January", "February", "March", "April", "May", "June", 
                            "July", "August", "September", "October", "November", "December"]

            # Count occurrences of flowering and fruiting months
            flowering_counts = {month: 0 for month in months_order}
            fruiting_counts = {month: 0 for month in months_order}

            if flowering == "Yes":
                for month in flowering_months.split("-"):
                    flowering_counts[month.strip()] += 1

            if fruiting == "Yes":
                for month in fruiting_months.split("-"):
                    fruiting_counts[month.strip()] += 1

            # Convert to DataFrame for plotting
            flowering_counts_df = pd.DataFrame({"Month": months_order, "Flowering": [flowering_counts[month] for month in months_order]})
            fruiting_counts_df = pd.DataFrame({"Month": months_order, "Fruiting": [fruiting_counts[month] for month in months_order]})

            # Plot the graph
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(flowering_counts_df["Month"], flowering_counts_df["Flowering"], color="green", label="Flowering")
            ax.bar(fruiting_counts_df["Month"], fruiting_counts_df["Fruiting"], color="orange", alpha=0.7, label="Fruiting")
            ax.set_xlabel("Months of the Year")
            ax.set_ylabel("Number of Occurrences")
            ax.set_title(f"🌼 {st.session_state.user_plant_name_lower.capitalize()} - Flowering & Fruiting Trends")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # ✅ Analyze Best Season for Flowering/Fruiting
            st.subheader("🌿 Best Season for Flowering & Fruiting")

            # Define seasons and their corresponding months
            seasons = {
                "Winter": ["December", "January", "February"],
                "Spring": ["March", "April", "May"],
                "Summer": ["June", "July", "August"],
                "Fall": ["September", "October", "November"]
            }

            # Calculate total occurrences for each season
            flowering_season_counts = {season: 0 for season in seasons}
            fruiting_season_counts = {season: 0 for season in seasons}

            for season, months in seasons.items():
                for month in months:
                    flowering_season_counts[season] += flowering_counts[month]
                    fruiting_season_counts[season] += fruiting_counts[month]

            # Determine the best season for flowering and fruiting
            best_flowering_season = max(flowering_season_counts, key=flowering_season_counts.get)
            best_fruiting_season = max(fruiting_season_counts, key=fruiting_season_counts.get)

            # Display results
            if flowering == "Yes":
                st.success(f"✅ **Best Season for Flowering:** {best_flowering_season}")
            if fruiting == "Yes":
                st.success(f"✅ **Best Season for Fruiting:** {best_fruiting_season}")

           # ✅ Plot Height Trends Based on Season
            st.subheader("📏 Flowering/Fruiting Height vs. Season")

            # Extract height data
            height_data = plant_data.iloc[0]["Height Based on Season (cm)"]
            height_dict = {}

            # Split the height data into season-height pairs
            for season_height in height_data.split("|"):
                # Extract the height range and season
                height_range, season = season_height.strip().split(" (")
                season = season.replace(")", "").strip()  # Remove the closing parenthesis
                height_min, height_max = map(int, height_range.split("-"))  # Extract min and max height
                height_dict[season] = (height_min, height_max)  # Store in dictionary

            # Prepare data for plotting
            seasons_list = list(height_dict.keys())
            height_min = [height_dict[season][0] for season in seasons_list]
            height_max = [height_dict[season][1] for season in seasons_list]

            # Plot the graph
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(seasons_list, height_max, color="blue", alpha=0.6, label="Max Height")
            ax.bar(seasons_list, height_min, color="green", alpha=0.6, label="Min Height")
            ax.set_xlabel("Season")
            ax.set_ylabel("Height (cm)")
            ax.set_title(f"📏 {st.session_state.user_plant_name_lower.capitalize()} - Height Trends by Season")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)
            # ✅ Chat Box for User Input
            st.subheader("💬 Plant Condition Check")
            user_issue = st.text_input("Describe any flowering or fruiting issues:", key="user_issue")

            # Ensure the variable is not empty before processing
            if user_issue:
                user_issue_lower = user_issue.lower()

                # Define common problem indicators
                issue_keywords = ["not grow", "dying", "yellow", "wilt", "dry", "falling", "poor flowering"]

                # Check if any issue keywords are in user input
                if any(keyword in user_issue_lower for keyword in issue_keywords):
                    st.error("⚠️ Your plant may have a growth issue. Consider checking soil nutrients, watering, and sunlight!")
                    if st.session_state.user_issue:
                        st.subheader("🍃 Select Leaf Color")
                        leaf_color = st.selectbox("🍃 Select Leaf Color", ["Yellow", "Brown", "Drooping", "Dark Green", "Purplish"], key="leaf_color")
                        
                        # Analysis based on leaf color
                        leaf_issues = {
                            "Yellow": {"cause": "Poor Nutrient Absorption (Nitrogen, Iron, Magnesium Deficiency)",
                                    "effect": "Weak growth, delayed flowering, reduced fruit production",
                                    "solution": "Add balanced fertilizers and ensure proper soil pH",
                                    "color": "yellow"},
                            "Brown": {"cause": "Overwatering/Underwatering", 
                                    "effect": "Root rot or dehydration causing stress",
                                    "solution": "Adjust watering and check drainage",
                                    "color": "brown"},
                            "Drooping": {"cause": "Root Issues (Overwatering, Poor Aeration, Fungal Infections)",
                                    "effect": "Weak stem support, reducing flowering",
                                    "solution": "Improve soil drainage and avoid waterlogging",
                                    "color": "gray"},
                            "Dark Green": {"cause": "Excess Nitrogen",
                                    "effect": "Promotes leafy growth but inhibits flowering",
                                    "solution": "Reduce nitrogen and increase phosphorus & potassium",
                                    "color": "green"},
                            "Purplish": {"cause": "Phosphorus Deficiency",
                                    "effect": "Weak root development, poor fruit set",
                                    "solution": "Use phosphorus-rich fertilizers like bone meal",
                                    "color": "purple"}
                        }
                        
                        if leaf_color in leaf_issues:
                            issue = leaf_issues[leaf_color]
                            st.write(f"### 🌿 **Issue Analysis: {leaf_color} Leaves**")
                            st.write(f"**Cause:** {issue['cause']}")
                            st.write(f"**Effect:** {issue['effect']}")
                            st.write(f"**Solution:** {issue['solution']}")
                else:
                    st.success("✅ Your plant appears to be growing well!")  
# ✅ **Show Environmental Factors Analysis only if selected**
if st.session_state.selected_analysis == "environment":
    st.write("## 🌡️ Environmental Impact Analysis")

    # ✅ Load environmental data
    env_data = pd.read_csv("environment_data.csv")  # Ensure correct file path

    # Fix column names
    env_data.columns = env_data.columns.str.strip().str.lower()

    # Ensure user_plant_name_lower exists
    if not st.session_state.user_plant_name_lower:
        st.error("❌ No plant name provided. Please enter a valid plant name.")
    else:
        # Filter data for the selected plant
        plant_env_data = env_data[env_data["plant name"].str.lower() == st.session_state.user_plant_name_lower]

        if plant_env_data.empty:
            st.error("❌ No environmental data found for this plant.")
        else:
            # ✅ Convert numeric columns to float (fixing TypeError)
            numeric_cols = ["temperature (°c)", "humidity (%)", "aqi"]
            for col in numeric_cols:
                plant_env_data[col] = pd.to_numeric(plant_env_data[col], errors='coerce')  # Convert to numeric, set errors as NaN

            # ✅ Group data by season for analysis
            season_grouped = plant_env_data.groupby("season")[numeric_cols].mean()  # Now only numeric columns

            # ✅ 🌡️ Pie Chart: Temperature Distribution by Season
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(season_grouped["temperature (°c)"], labels=season_grouped.index, autopct='%1.1f%%', colors=['red', 'orange', 'yellow', 'pink'])
            ax.set_title("🌡️ Temperature Distribution by Season")
            st.pyplot(fig)

            # ✅ 💧 Bar Chart: Humidity Levels by Season
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(season_grouped.index, season_grouped["humidity (%)"], color=['blue', 'cyan', 'navy', 'skyblue'])
            ax.set_xlabel("Season")
            ax.set_ylabel("Humidity (%)")
            ax.set_title("💧 Humidity Levels by Season")
            st.pyplot(fig)

            # ✅ 🌫️ Line Chart: AQI Trends Across Seasons
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(season_grouped.index, season_grouped["aqi"], marker='o', color='green', linestyle='-', linewidth=2)
            ax.set_xlabel("Season")
            ax.set_ylabel("Air Quality Index (AQI)")
            ax.set_title("🌫️ AQI Trends Across Seasons")
            st.pyplot(fig)

            # ✅ **Determine Best Season for the Plant with Weighted Scoring**
            st.subheader("🌿 Best Season for Your Plant")

            # 1️⃣ Define Ideal Ranges (These values can be adjusted per plant type)
            ideal_temp_range = (18, 30)  # Ideal temperature range (can be adjusted)
            ideal_humidity_range = (40, 70)  # Ideal humidity range
            ideal_aqi_threshold = 50  # Lower AQI is better

            # 2️⃣ **Scoring Function**: Higher score means better season
            def score_season(temp, humidity, aqi):
                temp_score = max(0, 100 - abs((temp - sum(ideal_temp_range) / 2) * 5))  # Closer to ideal range = higher score
                humidity_score = max(0, 100 - abs((humidity - sum(ideal_humidity_range) / 2) * 3))  # Closer = better
                aqi_score = max(0, 100 - (aqi - ideal_aqi_threshold) * 2)  # Lower AQI is better
                return temp_score + humidity_score + aqi_score  # Total score

            # 3️⃣ Calculate Scores for Each Season
            season_scores = {
                season: score_season(row["temperature (°c)"], row["humidity (%)"], row["aqi"])
                for season, row in season_grouped.iterrows()
            }

            # 4️⃣ Find Best Season Based on Highest Score
            best_season = max(season_scores, key=season_scores.get)

            # ✅ Display best season result
            st.success(f"✅ Based on environmental factors, **{st.session_state.user_plant_name_lower.capitalize()}** is best suited for **{best_season.capitalize()}** season!")

            # ✅ Show detailed scoring breakdown
            st.write("### 📊 **Scoring Breakdown:**")
            for season, score in season_scores.items():
                st.write(f"- **{season.capitalize()}** → Score: **{score:.1f}**")

# 🔄 **Reset Button**
if st.button("🔄 Start Over"):
    st.session_state.plant_found = False
    st.session_state.plant_details = None
    st.session_state.selected_analysis = None
    st.session_state.user_plant_name_lower = None
    st.rerun()
