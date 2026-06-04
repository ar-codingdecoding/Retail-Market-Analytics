import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import os
st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide"
)

st.title("🛍️ Store Intelligence Dashboard")

API_URL = os.getenv("API_URL", "https://store-intelligence-api-qkiu.onrender.com")
refresh = st.sidebar.checkbox(
    "Auto Refresh",
    value=True
)
store = st.selectbox(
    "Select Store",
    [
        "STORE_1",
        "STORE_2"
    ]
)

if store == "STORE_1":

    camera = st.selectbox(
        "Select Camera",
        [
            "ALL_STORE1",
            "CAM1",
            "CAM2",
            "CAM3",
            "CAM5"
        ]
    )

else:

    camera = st.selectbox(
        "Select Camera",
        [
            "ALL_STORE2",
            "STORE2_CAM1",
            "STORE2_CAM2",
            "STORE2_CAM6"
        ]
    )
st.info(
    f"Viewing analytics for {store}"
)
# ------------------------
# API Calls
# ------------------------

metrics = requests.get(
    f"{API_URL}/stores/{camera}/metrics"
).json()

heatmap = requests.get(
    f"{API_URL}/stores/{camera}/heatmap"
).json()

funnel = requests.get(
    f"{API_URL}/stores/{camera}/funnel"
).json()

anomalies = requests.get(
    f"{API_URL}/stores/{camera}/anomalies"
).json()

# ------------------------
# KPI Cards
# ------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Events",
        metrics.get(
            "total_events",
            0
        )
    )

with c2:

    st.metric(
        "Zone Entries",
        metrics.get(
            "zone_enter_events",
            0
        )
    )

with c3:

    st.metric(
        "Zone Dwell",
        metrics.get(
            "zone_dwell_events",
            0
        )
    )

with c4:

    st.metric(
        "Unique Visitors",
        heatmap.get(
            "unique_visitors",
            0
        )
    )

st.divider()
st.subheader(
    "Event Distribution"
)

event_data = pd.DataFrame(
    {
        "Event": [
            "Entries",
            "Engaged"
        ],
        "Count": [
            funnel.get(
                "entered",
                0
            ),
            funnel.get(
                "engaged",
                0
            )
        ]
    }
)

fig_events = px.pie(
    event_data,
    names="Event",
    values="Count",
    title="Customer Activity"
)

st.plotly_chart(
    fig_events,
    use_container_width=True
)

# ------------------------
# Heatmap
# ------------------------

st.subheader(
    "Zone Popularity"
)

zones = heatmap.get(
    "zones",
    {}
)

if len(zones) > 0:

    heat_df = pd.DataFrame(
        [
            {
                "Zone": zone,
                "Visits": data["visits"],
                "Score": data["score"]
            }
            for zone, data in zones.items()
        ]
    )

    fig1 = px.bar(
        heat_df,
        x="Zone",
        y="Visits",
        color="Score",
        title="Most Visited Zones"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )
# ------------------------
# Store Layout Heatmap
# ------------------------

    st.subheader(
        "Store Layout Heatmap"
    )

    layout_data = []

    for zone_name, data in zones.items():

        layout_data.append(
            {
                "Zone": zone_name,
                "Intensity": data["score"]
            }
        )

    layout_df = pd.DataFrame(
        layout_data
    )

    fig_layout = px.treemap(
        layout_df,
        path=["Zone"],
        values="Intensity",
        color="Intensity",
        title="Store Traffic Heatmap"
    )

    st.plotly_chart(
        fig_layout,
        use_container_width=True
    )    
    

else:

    st.info(
        "No heatmap data available."
    )

# ------------------------
# Funnel
# ------------------------

st.subheader(
    "Customer Funnel"
)

funnel_df = pd.DataFrame({

    "Stage": [
        "Entered",
        "Engaged"
    ],

    "Count": [

        funnel.get(
            "entered",
            0
        ),

        funnel.get(
            "engaged",
            0
        )
    ]
})

fig2 = px.funnel(
    funnel_df,
    x="Count",
    y="Stage"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.success(
    f"Conversion Rate = {funnel.get('conversion_rate',0)}%"
)

st.divider()

# ------------------------
# Confidence
# ------------------------
st.divider()

st.subheader(
    "Store Summary"
)

st.write(
    f"Store: {store}"
)

st.write(
    f"Camera: {camera}"
)

st.write(
    f"Unique Visitors: {heatmap.get('unique_visitors',0)}"
)

st.write(
    f"Conversion Rate: {funnel.get('conversion_rate',0)}%"
)
st.subheader(
    "Data Quality"
)

st.write(
    "Unique Visitors:",
    heatmap.get(
        "unique_visitors",
        0
    )
)

st.write(
    "Data Confidence:",
    heatmap.get(
        "data_confidence",
        False
    )
)

st.divider()

# ------------------------
# Anomalies
# ------------------------

st.subheader(
    "Anomalies"
)

if len(
    anomalies.get(
        "anomalies",
        []
    )
) == 0:

    st.success(
        "No active anomalies."
    )

else:

    st.error(
        anomalies
    )
if refresh:

    time.sleep(5)

    st.rerun()
