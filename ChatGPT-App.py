# streamlit_app.py
# BI-style Streamlit dashboard for UCI Student Performance dataset (Math & Portuguese)
# Paste this file locally and run: streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="Student Performance BI Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Student Performance – BI Dashboard")
st.caption("UCI Student Performance Dataset (Math & Portuguese)")

# -----------------------------
# Data Loading
# -----------------------------
@st.cache_data

def load_data():
    # You can replace these URLs with local CSV paths if preferred
    math_url = "/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/student/student-mat.csv"
    port_url = "/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/student/student-por.csv"

    math_df = pd.read_csv(math_url, sep=";")
    port_df = pd.read_csv(port_url, sep=";")

    math_df["dataset"] = "Math"
    port_df["dataset"] = "Portuguese"

    df = pd.concat([math_df, port_df], ignore_index=True)
    return df, math_df, port_df


df, math_df, port_df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

selected_dataset = st.sidebar.multiselect(
    "Dataset",
    options=df["dataset"].unique(),
    default=df["dataset"].unique(),
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=df["sex"].unique(),
    default=df["sex"].unique(),
)

selected_school = st.sidebar.multiselect(
    "School",
    options=df["school"].unique(),
    default=df["school"].unique(),
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max())),
)

# Apply filters
filtered_df = df[
    (df["dataset"].isin(selected_dataset)) &
    (df["sex"].isin(selected_gender)) &
    (df["school"].isin(selected_school)) &
    (df["age"] >= age_range[0]) &
    (df["age"] <= age_range[1])
]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Students", f"{len(filtered_df):,}")

with col2:
    st.metric("Avg Final Grade (G3)", f"{filtered_df['G3'].mean():.2f}")

with col3:
    pass_rate = (filtered_df["G3"] >= 10).mean() * 100
    st.metric("Pass Rate (%)", f"{pass_rate:.1f}%")

with col4:
    st.metric("Avg Absences", f"{filtered_df['absences'].mean():.1f}")

# -----------------------------
# Charts Row 1
# -----------------------------
st.subheader("Performance Overview")

col1, col2 = st.columns(2)

with col1:
    fig_grade_dist = px.histogram(
        filtered_df,
        x="G3",
        nbins=20,
        color="dataset",
        title="Final Grade Distribution (G3)",
        opacity=0.7,
    )
    fig_grade_dist.update_layout(bargap=0.1)
    st.plotly_chart(fig_grade_dist, use_container_width=True)

with col2:
    avg_by_dataset = (
        filtered_df
        .groupby("dataset")["G3"]
        .mean()
        .reset_index()
    )

    fig_avg_dataset = px.bar(
        avg_by_dataset,
        x="dataset",
        y="G3",
        title="Average Final Grade by Dataset",
        text_auto=True,
    )
    st.plotly_chart(fig_avg_dataset, use_container_width=True)

# -----------------------------
# Charts Row 2
# -----------------------------
st.subheader("Demographics & Behavior")

col1, col2, col3 = st.columns(3)

with col1:
    fig_gender = px.box(
        filtered_df,
        x="sex",
        y="G3",
        color="sex",
        title="Final Grade by Gender",
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    fig_studytime = px.box(
        filtered_df,
        x="studytime",
        y="G3",
        title="Grades vs Study Time",
    )
    st.plotly_chart(fig_studytime, use_container_width=True)

with col3:
    fig_absences = px.scatter(
        filtered_df,
        x="absences",
        y="G3",
        color="dataset",
        title="Absences vs Final Grade",
        trendline="ols",
    )
    st.plotly_chart(fig_absences, use_container_width=True)

# -----------------------------
# Detailed Analysis Table
# -----------------------------
st.subheader("Detailed Student Data")

st.dataframe(
    filtered_df.sort_values("G3", ascending=False),
    use_container_width=True,
    height=400,
)

# -----------------------------
# Aggregated Table
# -----------------------------
st.subheader("Aggregated Metrics")

agg_table = (
    filtered_df
    .groupby(["dataset", "sex"], as_index=False)
    .agg(
        Students=("G3", "count"),
        Avg_G1=("G1", "mean"),
        Avg_G2=("G2", "mean"),
        Avg_G3=("G3", "mean"),
        Pass_Rate=("G3", lambda x: (x >= 10).mean() * 100),
    )
)

agg_table[["Avg_G1", "Avg_G2", "Avg_G3", "Pass_Rate"]] = agg_table[[
    "Avg_G1", "Avg_G2", "Avg_G3", "Pass_Rate"
]].round(2)

st.dataframe(agg_table, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit • Dataset: UCI Machine Learning Repository")
