import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import joblib

st.set_page_config(
    page_title="Sri Lanka Flood & Rainfall Risk GIS",
    page_icon="🌧️",
    layout="wide"
)

df = pd.read_csv("data/rainfall_flood_risk.csv")
df["date"] = pd.to_datetime(df["date"])

model = joblib.load("models/flood_risk_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: white;
}

button[data-baseweb="tab"] {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 20px !important;
    border: 1px solid #374151 !important;
    margin: 3px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #2563eb !important;
    color: white !important;
    border: 1px solid #60a5fa !important;
}

.kpi-card {
    background: #111827;
    padding: 22px;
    border-radius: 15px;
    min-height: 150px;
    border: 1px solid #1f2937;
    overflow-wrap: break-word;
}

.kpi-card h4 {
    color: #9ca3af;
}

.kpi-card h2 {
    font-size: 30px;
}

.stButton > button,
.stDownloadButton > button {
    background-color: #1f2937 !important;
    color: white !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
    font-weight: 600 !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #2563eb !important;
    border: 1px solid #2563eb !important;
}

div[data-testid="stAlert"] {
    background-color: #0f172a;
    color: white;
    border: 1px solid #1e40af;
}

@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 230px !important;
        min-width: 230px !important;
        max-width: 230px !important;
    }

    section[data-testid="stSidebar"] * {
        font-size: 13px !important;
    }

    .kpi-card {
        margin-bottom: 16px !important;
        padding: 18px !important;
        border-radius: 14px !important;
    }

    .kpi-card h2 {
        font-size: 26px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #111827, #1f2937);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #374151;
">
<h1 style='color:white; margin-bottom:5px;'>
    🌧️ Sri Lanka Flood & Rainfall Risk Intelligence System
</h1>

<p style='color:#cbd5e1; font-size:17px;'>
    AI-powered disaster intelligence dashboard for rainfall monitoring,
    flood-prone district analysis, emergency risk zones, and flood risk prediction across Sri Lanka.
</p>

<p style='color:#9ca3af; font-size:14px;'>
    Developed by Sanjula Bandara | Data Science Undergraduate
</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Sidebar
st.sidebar.markdown("## 🌧️ Flood Risk Filters")
st.sidebar.markdown("Use these filters to analyze disaster risk patterns.")
st.sidebar.markdown("---")

selected_risk = st.sidebar.pills(
    "Flood Risk Level",
    options=list(df["flood_risk"].unique()),
    default=list(df["flood_risk"].unique()),
    selection_mode="multi"
)

selected_drainage = st.sidebar.pills(
    "Drainage Condition",
    options=list(df["drainage_condition"].unique()),
    default=list(df["drainage_condition"].unique()),
    selection_mode="multi"
)

filtered_df = df[
    (df["flood_risk"].isin(selected_risk)) &
    (df["drainage_condition"].isin(selected_drainage))
]

if filtered_df.empty:
    st.warning("No records available for the selected filters.")
    st.stop()

# KPIs
total_districts = len(filtered_df)
high_risk_count = len(filtered_df[filtered_df["flood_risk"] == "High"])
avg_rainfall = round(filtered_df["monthly_rainfall_mm"].mean(), 2)
highest_risk_district = filtered_df.sort_values(
    "monthly_rainfall_mm",
    ascending=False
).iloc[0]["district"]

k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
        <h4>Total Districts</h4>
        <h2 style='color:white'>{total_districts}</h2>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card'>
        <h4>High Risk Districts</h4>
        <h2 style='color:#ef4444'>{high_risk_count}</h2>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card'>
        <h4>Average Rainfall</h4>
        <h2 style='color:#38bdf8'>{avg_rainfall} mm</h2>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card'>
        <h4>Highest Rainfall Zone</h4>
        <h2 style='color:#facc15'>{highest_risk_district}</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Map and rainfall chart
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("🗺️ Flood Risk GIS Map")

    m = folium.Map(
        location=[7.8731, 80.7718],
        zoom_start=7,
        tiles="CartoDB dark_matter"
    )

    risk_colors = {
        "High": "red",
        "Medium": "orange",
        "Low": "green"
    }

    for _, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=max(row["monthly_rainfall_mm"] / 35, 5),
            popup=f"""
            <b>{row['district']}</b><br>
            Rainfall: {row['monthly_rainfall_mm']} mm<br>
            River Level: {row['river_level_m']} m<br>
            Soil Saturation: {row['soil_saturation_percent']}%<br>
            Drainage: {row['drainage_condition']}<br>
            Flood Risk: {row['flood_risk']}
            """,
            tooltip=row["district"],
            color=risk_colors[row["flood_risk"]],
            fill=True,
            fill_opacity=0.75
        ).add_to(m)

    st_folium(m, use_container_width=True, height=500)

with right_col:
    st.subheader("📊 Rainfall by District")

    fig_rain = px.bar(
        filtered_df.sort_values("monthly_rainfall_mm", ascending=True),
        x="monthly_rainfall_mm",
        y="district",
        orientation="h",
        text="monthly_rainfall_mm",
        title="Monthly Rainfall Distribution"
    )

    fig_rain.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#374151"),
        yaxis=dict(gridcolor="#374151")
    )

    st.plotly_chart(fig_rain, use_container_width=True)

# Flood risk distribution
st.subheader("🚨 Flood Risk Distribution")

risk_chart = filtered_df["flood_risk"].value_counts().reset_index()
risk_chart.columns = ["flood_risk", "count"]

fig_pie = px.pie(
    risk_chart,
    names="flood_risk",
    values="count",
    hole=0.45,
    title="Flood Risk Level Distribution"
)

fig_pie.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b1220",
    plot_bgcolor="#0b1220",
    font=dict(color="white"),
    legend=dict(
        font=dict(color="white"),
        bgcolor="rgba(0,0,0,0)"
    )
)

fig_pie.update_traces(
    textfont_color="white",
    marker=dict(line=dict(color="#0b1220", width=2))
)

st.plotly_chart(fig_pie, use_container_width=True)

# District flood risk intelligence
st.subheader("🚨 District Flood Risk Intelligence")

risk_table = (
    filtered_df.groupby("district")
    .agg(
        avg_rainfall=("monthly_rainfall_mm", "mean"),
        avg_river_level=("river_level_m", "mean"),
        avg_soil_saturation=("soil_saturation_percent", "mean"),
        flood_history=("flood_history_count", "sum")
    )
    .reset_index()
)

risk_table["risk_score"] = (
    risk_table["avg_rainfall"] * 0.3 +
    risk_table["avg_river_level"] * 20 +
    risk_table["avg_soil_saturation"] * 0.5 +
    risk_table["flood_history"] * 2
)

risk_table = risk_table.sort_values("risk_score", ascending=False)

fig_risk = px.bar(
    risk_table,
    x="district",
    y="risk_score",
    color="risk_score",
    text=risk_table["risk_score"].round(2),
    title="District Flood Risk Score"
)

fig_risk.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b1220",
    plot_bgcolor="#0b1220",
    font=dict(color="white"),
    xaxis=dict(gridcolor="#374151"),
    yaxis=dict(gridcolor="#374151")
)

st.plotly_chart(fig_risk, use_container_width=True)

# Emergency priority table
st.subheader("🚑 Emergency Flood Priority Zones")

priority_table = risk_table[
    [
        "district",
        "avg_rainfall",
        "avg_river_level",
        "avg_soil_saturation",
        "risk_score"
    ]
].round(2).reset_index(drop=True)

def risk_color(value):
    if value >= 190:
        return "background-color:#7f1d1d;color:white;font-weight:bold;"
    elif value >= 160:
        return "background-color:#b91c1c;color:white;font-weight:bold;"
    elif value >= 130:
        return "background-color:#dc2626;color:white;font-weight:bold;"
    else:
        return "background-color:#1f2937;color:white;font-weight:bold;"

styled_table = (
    priority_table.style
    .hide(axis="index")
    .map(risk_color, subset=["risk_score"])
    .set_table_styles([
        {
            "selector": "thead th",
            "props": [
                ("background-color", "#1f2937"),
                ("color", "white"),
                ("border", "1px solid #374151"),
                ("font-size", "14px"),
                ("text-align", "center"),
                ("padding", "10px")
            ]
        },
        {
            "selector": "tbody td",
            "props": [
                ("background-color", "#111827"),
                ("color", "white"),
                ("border", "1px solid #374151"),
                ("font-size", "14px"),
                ("padding", "10px")
            ]
        }
    ])
)

st.markdown(styled_table.to_html(), unsafe_allow_html=True)

# Rainfall trend
st.subheader("📈 Rainfall Trend Analysis")

trend_chart = filtered_df.sort_values("date")

fig_trend = px.line(
    trend_chart,
    x="date",
    y="monthly_rainfall_mm",
    color="district",
    markers=True,
    title="Rainfall Monitoring Trend"
)

fig_trend.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b1220",
    plot_bgcolor="#0b1220",
    font=dict(color="white"),
    xaxis=dict(gridcolor="#374151"),
    yaxis=dict(gridcolor="#374151")
)

st.plotly_chart(fig_trend, use_container_width=True)

# Smart insight
st.subheader("🧠 AI Smart Disaster Insight")

highest_risk = risk_table.iloc[0]

st.success(
    f"""
    🚨 {highest_risk['district']} is currently identified as the highest flood-risk district.

    • Average Rainfall: {highest_risk['avg_rainfall']:.2f} mm  
    • Average River Level: {highest_risk['avg_river_level']:.2f} m  
    • Average Soil Saturation: {highest_risk['avg_soil_saturation']:.2f}%  
    • Calculated Flood Risk Score: {highest_risk['risk_score']:.2f}

    Recommendation:
    Prioritize flood monitoring, drainage inspection, early warning communication,
    and emergency preparedness in this district.
    """
)

# Download
st.subheader("⬇️ Download Processed Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Flood Risk Dataset",
    data=csv,
    file_name="processed_sri_lanka_flood_risk.csv",
    mime="text/csv"
)

st.markdown("---")

# AI Prediction section
st.subheader("🌊 AI Flood Risk Prediction System")

st.markdown(
    "Predict flood risk using Machine Learning and environmental risk factors."
)

col1, col2 = st.columns(2)

with col1:
    pred_district = st.selectbox(
        "District",
        df["district"].unique()
    )

    pred_rainfall = st.slider(
        "Monthly Rainfall (mm)",
        50,
        400,
        220
    )

    pred_river = st.slider(
        "River Level (m)",
        1.0,
        5.0,
        3.0
    )

with col2:
    pred_soil = st.slider(
        "Soil Saturation (%)",
        20,
        100,
        70
    )

    pred_population = st.slider(
        "Population Density",
        100,
        4000,
        1000
    )

    pred_history = st.slider(
        "Flood History Count",
        0,
        15,
        5
    )

    pred_drainage = st.selectbox(
        "Drainage Condition",
        df["drainage_condition"].unique()
    )

if st.button("Predict Flood Risk"):
    input_data = pd.DataFrame({
        "district": [
            label_encoders["district"].transform([pred_district])[0]
        ],
        "monthly_rainfall_mm": [pred_rainfall],
        "river_level_m": [pred_river],
        "soil_saturation_percent": [pred_soil],
        "population_density": [pred_population],
        "flood_history_count": [pred_history],
        "drainage_condition": [
            label_encoders["drainage_condition"].transform([pred_drainage])[0]
        ]
    })

    prediction = model.predict(input_data)[0]

    risk_label = label_encoders["flood_risk"].inverse_transform(
        [prediction]
    )[0]

    if risk_label == "High":
        st.error(f"🚨 Predicted Flood Risk: {risk_label}")
    elif risk_label == "Medium":
        st.warning(f"⚠️ Predicted Flood Risk: {risk_label}")
    else:
        st.success(f"✅ Predicted Flood Risk: {risk_label}")

st.markdown("---")

st.markdown("""
<div style='text-align:center;color:gray'>
Developed by Sanjula Bandara | Sri Lanka 2026
</div>
""", unsafe_allow_html=True)