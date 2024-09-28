import streamlit as st
from common import check_login, add_user, render_header, render_main_page
import time
import base64
import pandas as pd
import sqlite3
import plotly.express as px

def header_page():
    header_col1, header_col2 = st.columns([1, 1])
    with header_col1:
            # logo
            with open("images/logo.png", "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
            st.markdown(f"""
                <style>
                .logo-image {{
                    width: 100px;
                    height: 100px;
                    cursor: pointer;
                }}
                </style>
                <img src="data:image/png;base64,{encoded_image}" class="logo-image" onclick="window.location.href='/'" />
                """, unsafe_allow_html=True)
        # page header's message
    with header_col2:
        st.markdown(f"<h3 style='text-align: center; color: #539cdc;'>{st.session_state.username}, welcome to Results</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Here you see the results of your effort in training and assessments</h4>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            .stButton>button {
                background-color: #246cab;
                font-size: 16px;
                color: white;
            }
            .stButton>button:hover {
                background-color: #539cdc;
                color: white;
            }
            .button-container {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }
            </style>
            """, unsafe_allow_html=True)

def render_results_page():
    header_page()
    # st.markdown("<h3 style='text-align: center;'>Results Page</h1>", unsafe_allow_html=True)
    # st.markdown("<p style='text-align: center;'>This is the Results page content.</p>", unsafe_allow_html=True)

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
    
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()

    # Execute the query to fetch data
    query = f'SELECT percentace_level, date, assesment_type FROM Evaluations e WHERE e."user" = ?'
    cursor.execute(query, (st.session_state.username,))
    rows = cursor.fetchall()
    col_names = [description[0] for description in cursor.description]
    df = pd.DataFrame(rows, columns=col_names)
    conn.close()

    # Display the DataFrame as a table using Streamlit
    st.write(f"{st.session_state.username} Evaluation's history")
    df['date'] = pd.to_datetime(df['date'])
    assessment_dfs = {assessment_type: data for assessment_type, data in df.groupby('assesment_type')}

    # Display and visualize each DataFrame
    for assessment_type, assessment_df in assessment_dfs.items():
        # st.write(f"Data for {assessment_type}")
        # st.dataframe(assessment_df)

        # Create graphs to visualize the progress data using Plotly
        # st.write(f"Progress Data Visualization for {assessment_type}")
        fig = px.line(assessment_df, x='date', y='percentace_level', title=f'History assessment for {assessment_type}')
        st.plotly_chart(fig)

if __name__ == "__main__":
    if 'logged_in' in st.session_state:
        if st.session_state.logged_in:
            # Initialize session state variables
            if 'selected_options' not in st.session_state:
                st.session_state.selected_options = {}
            if 'score' not in st.session_state:
                st.session_state.score = 0
            if 'quiz' not in st.session_state:
                st.session_state.quiz = []
            if 'current_question' not in st.session_state:
                st.session_state.current_question = 0
            if 'start_time' not in st.session_state:
                st.session_state.start_time = time.time()
            #rendering options
            if st.session_state.page == "": 
                render_results_page()
            # elif st.session_state.page == "agile":
            #     if st.session_state.page_section == "calculate_score":
            #         calculate_score()
            #     elif st.session_state.page_section == "agile_assessment":
            #         agile()
            #     else:
            #         agile_intro()
        else:
            st.subheader("Log in to have access to Results section")
    else:
        st.subheader("Log in to have access to Results section")