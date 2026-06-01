import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide"
)

st.title("🛍️ Store Intelligence Dashboard")

BASE_URL = "http://127.0.0.1:8000"

# ------------------------
# API Calls
# ------------------------

metrics = requests.get(f"{BASE_URL}/metrics").json()
heatmap = requests.get(f"{BASE_URL}/heatmap").json()
funnel = requests.get(f"{BASE_URL}/funnel").json()

# ------------------------
# KPI Cards
# ------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Events",
        metrics["total_events"]
    )

with c2:
    st.metric(
        "Zone Entries",
        metrics["zone_enter_events"]
    )

with c3:
    st.metric(
        "Zone Dwell Events",
        metrics["zone_dwell_events"]
    )

st.divider()

# ------------------------
# Heatmap Chart
# ------------------------

st.subheader("Zone Popularity")

heat_df = pd.DataFrame(
    list(heatmap.items()),
    columns=["Zone", "Visits"]
)

fig1 = px.bar(
    heat_df,
    x="Zone",
    y="Visits",
    title="Most Visited Zones"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ------------------------
# Funnel Chart
# ------------------------

st.subheader("Customer Funnel")

funnel_df = pd.DataFrame({
    "Stage": ["Entered", "Engaged"],
    "Count": [
        funnel["entered"],
        funnel["engaged"]
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
    f"Conversion Rate = {funnel['conversion_rate']}%"
)