import streamlit as st
from features.dashboard import render_dashboard
from state.session_state import init_session_state

st.set_page_config(page_title="GeoGuard IA", page_icon="🌎", layout="wide")
init_session_state()
render_dashboard()
