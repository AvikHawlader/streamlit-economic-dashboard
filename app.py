import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Economic Resilience Pathways Mapping India's Transition to a $5 Trillion Economy Dashboard", layout="wide")
st.title("\U0001F30F Economic Resilience Pathways Mapping India's Transition to a $5 Trillion Economy Dashboard")
st.markdown("""
This dashboard summarizes insights from official statistics (MoSPI datasets) to track sectoral performance, regional development, and policy priorities as India moves toward a $5 Trillion economy.
""")

# Load Data
@st.cache_data
def load_data():
    sector_gdp = pd.read_csv("Merged_Sectoral_Dataset.csv")
    top_sectors = pd.read_csv("Top6_Sectors_GDP_Contribution.csv")
    regional_index = pd.read_csv("Regional_Development_Index.csv")
    policy_table = pd.read_csv("Policy_Summary_Table.csv")
    return sector_gdp, top_sectors, regional_index, policy_table

sector_gdp, top_sectors, regional_index, policy_table = load_data()

# --- Sectoral Performance Visual ---
st.subheader("\U0001F4C8 Sectoral Performance Trends")
sector_options = top_sectors["Sector"].unique()
selected_sectors = st.multiselect("Select sectors to view GDP contribution trends:", sector_options, default=sector_options[:3])

if selected_sectors:
    filtered = top_sectors[top_sectors["Sector"].isin(selected_sectors)]
    fig_sector = px.line(filtered, x="Year", y="GDP_Contribution", color="Sector",
                         title="GDP Contribution of Selected Sectors", markers=True)
    st.plotly_chart(fig_sector, use_container_width=True)

# --- Regional Development Index ---
st.subheader("\U0001F4CA Regional Development Index (2023)")
top_states = regional_index.groupby("State")["Regional_Dev_Index"].mean().sort_values(ascending=False).head(10)
bottom_states = regional_index.groupby("State")["Regional_Dev_Index"].mean().sort_values().head(10)

col1, col2 = st.columns(2)
with col1:
    fig_top = px.bar(top_states, x=top_states.index, y=top_states.values,
                     title="Top 10 States by Development Index", labels={"x": "State", "y": "Index"}, color=top_states.values)
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    fig_bottom = px.bar(bottom_states, x=bottom_states.index, y=bottom_states.values,
                        title="Bottom 10 States by Development Index", labels={"x": "State", "y": "Index"}, color=bottom_states.values)
    st.plotly_chart(fig_bottom, use_container_width=True)

# --- Policy Summary Table ---
st.subheader("\U0001F4DD Policy Zone Classification")
st.dataframe(policy_table.style.format({"HCES_Consumption": "{:.0f}", "CPI_Stability": "{:.2f}", "Regional_Dev_Index": "{:.3f}"}))

st.markdown("---")
st.markdown("""
### Project Creator
**Name:** Avik Hawlader  
**Institute:** Indian Institute of Science Education and Research Bhopal  
**Email:** avik21@iiserb.ac.in
**Submission:** *Innovate with GoIStats Hackathon 2025*""")