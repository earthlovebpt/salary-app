import streamlit as st
from predict_page import show_predict_page
from insights_page import show_insights_page


page = st.sidebar.selectbox("Predict or Insights", ("Predict", "Insights"))

if page == "Predict":
    show_predict_page()
elif page == "Insights":
    show_insights_page()
