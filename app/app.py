import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery
from google.oauth2 import service_account

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Media Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# CLEAN CSS
# -------------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
}

.kpi-card {
    padding: 8px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: 600;
}

.kpi-card h3 {
    margin: 4px 0px 0px 0px;
    font-size: 18px;
}

.kpi1 { background: #2563EB; }
.kpi2 { background: #059669; }
.kpi3 { background: #D97706; }
.kpi4 { background: #DC2626; }

.chart-card {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}

.card1 { background-color: #0F172A; }
.card2 { background-color: #111827; }
.card3 { background-color: #1F2937; }
.card4 { background-color: #0B3B5A; }
.card5 { background-color: #064E3B; }
.card6 { background-color: #3F1D2E; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# BIGQUERY CONNECTION
# -------------------------------------------------------
credentials = service_account.Credentials.from_service_account_file(
    "config/gcp_credentials.json"
)

client = bigquery.Client(
    credentials=credentials,
    project="mediaanalysis-488617"
)

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
def load_data():
    youtube = client.query("""
        SELECT *
        FROM media_warehouse.fact_youtube
    """).to_dataframe()

    news = client.query("""
        SELECT *
        FROM media_warehouse.stg_news
    """).to_dataframe()

    return youtube, news


youtube_df, news_df = load_data()

youtube_df["published_at"] = pd.to_datetime(
    youtube_df["published_at"]
).dt.tz_localize(None)

youtube_df["year"] = youtube_df["published_at"].dt.year

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------
st.sidebar.header("Filters")

top_n = st.sidebar.slider("Top N Records", 3, 15, 5)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(youtube_df["year"].dropna().unique())
)

selected_channel = st.sidebar.selectbox(
    "Channel",
    ["All"] + sorted(youtube_df["channel_title"].unique())
)

# -------------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------------
filtered_df = youtube_df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["year"] == selected_year
    ]

if selected_channel != "All":
    filtered_df = filtered_df[
        filtered_df["channel_title"] == selected_channel
    ]

# -------------------------------------------------------
# HEADER + KPI
# -------------------------------------------------------
title_col, k1, k2, k3, k4 = st.columns([2,1,1,1,1])

with title_col:
    st.markdown("## 📊 Media Content Analysis Dashboard")

with k1:
    st.markdown(f'<div class="kpi-card kpi1">Categories<br><h3>{news_df["category"].nunique()}</h3></div>', unsafe_allow_html=True)

with k2:
    st.markdown(f'<div class="kpi-card kpi2">Channels<br><h3>{filtered_df["channel_title"].nunique()}</h3></div>', unsafe_allow_html=True)

with k3:
    st.markdown(f'<div class="kpi-card kpi3">Videos<br><h3>{filtered_df["video_id"].nunique()}</h3></div>', unsafe_allow_html=True)

with k4:
    st.markdown(f'<div class="kpi-card kpi4">Views<br><h3>{int(filtered_df["view_count"].sum()):,}</h3></div>', unsafe_allow_html=True)

# -------------------------------------------------------
# DATA PREP
# -------------------------------------------------------
top_categories = news_df["category"].value_counts().head(top_n).reset_index()
top_categories.columns = ["category", "count"]

top_channels = (
    filtered_df.groupby("channel_title")["view_count"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
)

top_videos = (
    filtered_df
    .sort_values(by="view_count", ascending=False)
    .head(top_n)
)

filtered_df["month"] = filtered_df["published_at"].dt.to_period("M").astype(str)

engagement = (
    filtered_df.groupby("month")["engagement_score"]
    .mean()
    .reset_index()
)

# Helper to remove animation
def static_layout(fig, height=250):
    fig.update_layout(
        transition_duration=0,
        height=height,
        font_color="white"
    )
    return fig

# -------------------------------------------------------
# ROW 1
# -------------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="chart-card card1">', unsafe_allow_html=True)
    st.subheader("Top Categories")
    fig1 = px.bar(top_categories, x="count", y="category",
                  orientation="h",
                  color_discrete_sequence=["#3B82F6"])
    fig1.update_layout(plot_bgcolor="#0F172A", paper_bgcolor="#0F172A")
    static_layout(fig1)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card card2">', unsafe_allow_html=True)
    st.subheader("Top Channels")
    fig2 = px.bar(top_channels, x="view_count", y="channel_title",
                  orientation="h",
                  color_discrete_sequence=["#10B981"])
    fig2.update_layout(plot_bgcolor="#111827", paper_bgcolor="#111827")
    static_layout(fig2)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="chart-card card3">', unsafe_allow_html=True)
    st.subheader("Top Videos")

    fig3 = px.bar(
        top_videos,
        x="view_count",
        y="video_title",
        orientation="h",
        color_discrete_sequence=["#F59E0B"],
        hover_data={
            "channel_title": True,
            "view_count": True
        }
    )

    fig3.update_layout(
        plot_bgcolor="#1F2937",
        paper_bgcolor="#1F2937"
    )

    static_layout(fig3)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# ROW 2
# -------------------------------------------------------
c4, c5, c6 = st.columns(3)

with c4:
    st.markdown('<div class="chart-card card4">', unsafe_allow_html=True)
    st.subheader("Category Share")
    fig4 = px.pie(top_categories, names="category", values="count",
                  color_discrete_sequence=px.colors.sequential.Blues)
    fig4.update_layout(height=280,
                       plot_bgcolor="#0B3B5A",
                       paper_bgcolor="#0B3B5A",
                       transition_duration=0,
                       font_color="white")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c5:
    st.markdown('<div class="chart-card card5">', unsafe_allow_html=True)
    st.subheader("Channel Share")
    fig5 = px.pie(top_channels, names="channel_title", values="view_count",
                  color_discrete_sequence=px.colors.sequential.Greens)
    fig5.update_layout(height=280,
                       plot_bgcolor="#064E3B",
                       paper_bgcolor="#064E3B",
                       transition_duration=0,
                       font_color="white")
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="chart-card card6">', unsafe_allow_html=True)
    st.subheader("Engagement Trend")
    fig6 = px.line(engagement, x="month", y="engagement_score",
                   color_discrete_sequence=["#EF4444"])
    fig6.update_layout(plot_bgcolor="#3F1D2E",
                       paper_bgcolor="#3F1D2E",
                       transition_duration=0)
    static_layout(fig6)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
