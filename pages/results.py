import streamlit as st
from common import check_login, add_user, render_header, render_main_page
import time
import base64
import pandas as pd
import sqlite3
import plotly.express as px

def header_page():
    with st.container(height=160):
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
            st.markdown("<h4 style='text-align: center;'>Training and Assessment's Results</h4>", unsafe_allow_html=True)
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

def footer_page():
    with st.container(height=160):
        footer_col1, footer_col2 = st.columns([3, 1])
        with footer_col1:
            st.page_link("start.py", label="Home", icon="🏠")
            st.page_link("pages/assessment.py", label="Assessments", icon="📄")
            st.page_link("pages/resources.py", label="Resources", icon="📚")
        with footer_col2:
            st.link_button("Feedback ⭐⭐⭐⭐⭐", "https://forms.gle/pNBmSCZmZXdiR9y4A", help="Send Feedback", type="secondary", disabled=False, use_container_width=False)

def render_results_page():
    header_page()
    
    with st.container(height=400):
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
        #query to get latest evaluations
        q_latest = ''' SELECT DISTINCT e.assesment_type, e.percentace_level, e.date
                        FROM Evaluations e
                        JOIN (
                            SELECT assesment_type, MAX(date) AS latest_date
                            FROM Evaluations
                            GROUP BY assesment_type
                        ) latest ON e.assesment_type = latest.assesment_type AND e.date = latest.latest_date
                        JOIN Users u ON e.user_id = u.user_id
                        WHERE u."user" = ?'''
        cursor.execute(q_latest, (st.session_state.username,))
        rows = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]
        df_latest = pd.DataFrame(rows, columns=col_names)

        # Create a bar graph using Plotly
        fig = px.bar(df_latest, 
            x='assesment_type', y='percentace_level', 
            color='date',
            labels={
                'assessment_type': 'Assessment Type',
                'percentage_level': 'Score'
            }, title='Latest Evaluation Scores by Assessment Type')
        st.plotly_chart(fig)

        # Execute the query to fetch data
        query = f'''SELECT percentace_level, date, assesment_type 
                    FROM Evaluations e 
                    join Users u on u.user_id = e.user_id 
                    WHERE u."user" = ?'''
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
            fig = px.line(assessment_df, x='date', y='percentace_level',
                labels={
                    'assessment_type': 'Assessment Type',
                    'percentage_level': 'Score'
                }, 
                title=f'History assessment for {assessment_type}')
            st.plotly_chart(fig)

    footer_page()

if __name__ == "__main__":
    if 'logged_in' in st.session_state:
        if st.session_state.logged_in:
            render_results_page()
        else:
            st.subheader("Log in to have access to Results section")
    else:
        st.subheader("Log in to have access to Results section")