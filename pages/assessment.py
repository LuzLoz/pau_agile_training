import streamlit as st
from common import check_login, add_user, render_main_page, render_header
import base64
import sqlite3
import time
def get_db_data(table):
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+table+";")
    rows = cursor.fetchall()
    conn.close()
    return rows 
    
def agile_intro():
    st.header("Agile")
    st.write("Evaluate your scrum master skills and assess areas for improvement based on the skill matrix for Scrum Master")
    st.write("This self-sssessment will guide you through a series of questions. It contains 20 questions with 4 options and only ones is the correct answer, with a limited time of 20 minutes")
    if st.button("Start Agile Assessment"):
        st.session_state.page_section = "assessment_agile"
        agile()

def agile():
    st.session_state.page_section = "agile"
    #header
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
        st.markdown(f"<h3 style='text-align: center; color: #539cdc;'>{st.session_state.username}, welcome to Assessments</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Agile</h4>", unsafe_allow_html=True)
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


    # Initialize session state for selected options and score
    if 'selected_options' not in st.session_state:
        st.session_state.selected_options = {}
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    # Timer
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    elapsed_time = time.time() - st.session_state.start_time
    st.write(f"Time elapsed: {int(elapsed_time)} seconds")

    rows = get_db_data("AgileAssesment")

    # Check if time is up (e.g., 20 minutes)
    if elapsed_time > 1200:
        st.write("Time is up!")
        calculate_score(rows)
        return
    
    st.write("Agile Assessment Data:")
    for row in rows:
        question_id = row[0]
        question = row[1]
        option_1 = row[2]
        option_2 = row[3]
        option_3 = row[4]
        option_4 = row[5]
        answer = row[6]
        explanation = row[7]
        selected_option = st.radio(question,[option_1, option_2, option_3, option_4],index=None,key=question_id)
        st.session_state.selected_options[question_id] = selected_option
        st.write("")

    if st.button("Calculate"):
        calculate_score(rows)

def calculate_score(rows):
    score = 0
    for row in rows:
        question_id = row[0]
        correct_answer = row[6]
        selected_option = st.session_state.selected_options.get(question_id, None)
        if selected_option == correct_answer:
            score += 1
    st.session_state.score = score
    st.write(f"Your score: {score}")

def render_assessment_page():
    #header
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
        st.markdown(f"<h3 style='text-align: center; color: #539cdc;'>{st.session_state.username}, welcome to Assessments</h3>", unsafe_allow_html=True)

    #page content
    st.markdown("<h4 style='text-align: center;'>Which hard skill do you want to asses today?</h4>", unsafe_allow_html=True)
    # hard skills list
    st.markdown('<div style="text-align: center;" class="button-container">', unsafe_allow_html=True)
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #246cab;
            width: 300px;
            height: 50px;
            margin: 5px;
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

    if st.button("Agile"):
        agile()
    elif st.button("Scrum"):
        agile()
    elif st.button("Technical Literacy"):
        agile()
    elif st.button("Bussines Literacy"):
        agile()
    elif st.button("Delivery"):
        agile()
    elif st.button("Meeting Mediation & Facilitation"):
        agile()




if __name__ == "__main__":
    if st.session_state.logged_in:
        st.session_state.start_time = time.time()
        if 'page_section' not in st.session_state: 
            render_assessment_page()
        elif st.session_state.page_section == "agile":
            agile()
    else:
        st.subheader("Log in to have access to this section")
    