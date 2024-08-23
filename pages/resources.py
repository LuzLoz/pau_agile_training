import streamlit as st
from common import check_login, add_user, render_main_page, render_header

def render_resources_page():
    render_header()
    st.markdown("<h1 style='text-align: center;'>Resources Page</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>This is the REsources page content.</p>", unsafe_allow_html=True)

    # main page
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #246cab;
    }
    .stButton>button:hover {
        background-color: #539cdc;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if "page" in st.query_params:
        if st.query_params["page"] == "assessment":
            from pages.assessment import render_assessment_page
            render_assessment_page()
        elif st.query_params["page"] == "resources":
            render_resources_page()
        elif st.query_params["page"] == "results":
            from results import render_results_page
            render_results_page()
    else:
        render_main_page()