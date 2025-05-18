import streamlit as st
st.set_page_config(layout="wide")

import importlib.util
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

@st.cache_data
def load_all_data(path):
    from data_handler import load_all_data as real_loader
    return real_loader(path)

# Inject custom CSS
try:
    with open("style.css") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found.")

# Header
st.markdown("""
<div class='custom-header'>
  <div class='header-left'>
    <div class='brand-name'>WorkSight AI</div>
    <div class='brand-tagline'>Intelligent HR Analytics & Predictions</div>
  </div>
  <div class='header-right'>
    <a href="https://yourhelp.site" target="_blank">Help</a>
  </div>
</div>
""", unsafe_allow_html=True)

# Load data
data_folder = "data"
with st.spinner("Loading data..."):
    data = load_all_data(data_folder)
df_emp = data['employee']

# Load reports
report_folder = "reports"
report_files = [f.replace(".py", "") for f in os.listdir(report_folder) if f.endswith(".py")]

# Report selector
st.sidebar.markdown("### 📊 Select Report")
selected_report = st.sidebar.selectbox("Report", report_files, key="report_selector")

# Filters
st.sidebar.markdown("### 🧭 Filters")

def get_filter_values(column):
    return sorted(df_emp[column].dropna().unique())

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        company = st.multiselect("Company", get_filter_values("company"), placeholder="Select...")
        business_unit = st.multiselect("Business Unit", get_filter_values("business_unit"), placeholder="Select...")
        area = st.multiselect("Area", get_filter_values("area"), placeholder="Select...")
        department = st.multiselect("Department", get_filter_values("department"), placeholder="Select...")
    with col2:
        employment_type = st.multiselect("Employment Type", get_filter_values("employment_type"), placeholder="Select...")
        zone = st.multiselect("Zone", get_filter_values("zone"), placeholder="Select...")
        function = st.multiselect("Function", get_filter_values("function"), placeholder="Select...")
        band = st.multiselect("Band", get_filter_values("band"), placeholder="Select...")

# Apply filters
def apply_filters(df):
    if company: df = df[df['company'].isin(company)]
    if employment_type: df = df[df['employment_type'].isin(employment_type)]
    if business_unit: df = df[df['business_unit'].isin(business_unit)]
    if zone: df = df[df['zone'].isin(zone)]
    if area: df = df[df['area'].isin(area)]
    if function: df = df[df['function'].isin(function)]
    if department: df = df[df['department'].isin(department)]
    if band: df = df[df['band'].isin(band)]
    return df

data['employee'] = apply_filters(df_emp)

# Load and render report
try:
    report_path = os.path.join(report_folder, f"{selected_report}.py")
    spec = importlib.util.spec_from_file_location("report_module", report_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.render(data)
except Exception as e:
    st.error(f"Failed to load report: {e}")

# Footer with predictions
st.markdown("""
<div class='custom-footer'>
    <div class='footer-content'>
        Powered by WorkSight AI • Last updated: {}</div>
</div>
""".format(datetime.now().strftime("%d %b %Y %H:%M")), unsafe_allow_html=True)