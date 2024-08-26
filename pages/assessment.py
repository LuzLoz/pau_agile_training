from datetime import datetime
import streamlit as st
# from common import check_login, add_user, render_main_page, render_header
import base64
import sqlite3
import time
def get_db_data(table):
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+table+" limit 5;")
    rows = cursor.fetchall()
    conn.close()
    return rows 
    
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
        st.markdown(f"<h3 style='text-align: center; color: #539cdc;'>{st.session_state.username}, welcome to Assessments</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.assesment_type}</h4>", unsafe_allow_html=True)
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

def agile_intro():
    header_page()
    # st.header("Agile")
    st.write("Evaluate your scrum master skills and assess areas for improvement based on the skill matrix for Scrum Master")
    st.write("This self-sssessment will guide you through a series of questions. Each question have 4 options and only ones is the correct answer, with a limited time of 20 minutes")
    if st.button("Start Agile Assessment"):
        st.session_state.page_section = "agile_assessment"
        st.session_state.start_time = time.time()
        st.session_state.selected_options = {}
        st.session_state.current_question = 0
        st.rerun()

def scrum_intro():
    header_page()
    # st.header("Agile")
    st.write("Evaluate your scrum master skills and assess areas for improvement based on the skill matrix for Scrum Master")
    st.write("This self-sssessment will guide you through a series of questions. Each question have 4 options and only ones is the correct answer, with a limited time of 20 minutes")
    if st.button("Start Scrum Assessment"):
        st.session_state.page_section = "scrum_assessment"
        st.session_state.start_time = time.time()
        st.session_state.selected_options = {}
        st.session_state.current_question = 0
        st.rerun()

def agile():
    #header
    header_page()

    # Calculate elapsed time
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 1200 - elapsed_time  # 20 minutes countdown
    # Convert remaining time to minutes and seconds
    minutes, seconds = divmod(int(remaining_time), 60)
    countdown_str = f"{minutes:02d}:{seconds:02d}"
    # Display countdown timer
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"""
            <div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                Question {st.session_state.current_question + 1} of {len(st.session_state.quiz)}
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        countdown_placeholder = st.empty()
        countdown_placeholder.markdown(f"""<div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                 ⏳ Remaining Time: {countdown_str}</div>
            """,
            unsafe_allow_html=True
        )


    #saving quiz in session data
    st.session_state.quiz = get_db_data("AgileAssesment")

    # Check if time is up (e.g., 20 minutes)
    if elapsed_time > 1200:
        st.write("Time is up!")
        st.session_state.page_section = "calculate_score"
        st.rerun()
    # Display quiz data in the left column

    if st.session_state.current_question < len(st.session_state.quiz):
        row = st.session_state.quiz[st.session_state.current_question]

        question_id = row[0]
        question = row[1]
        option_1 = row[2]
        option_2 = row[3]
        option_3 = row[4]
        option_4 = row[5]

        selected_option = st.radio(question,[option_1, option_2, option_3, option_4],index=None,key=question_id)
        st.session_state.selected_options[question_id] = selected_option
        st.write("")

        if st.button("Next"):
            st.session_state.current_question += 1
            st.rerun()
    else:
        st.write("You have completed the assessment!")
        st.session_state.page_section = "calculate_score"
        st.rerun()

def scrum():
    #header
    header_page()

    # Calculate elapsed time
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 1200 - elapsed_time  # 20 minutes countdown
    # Convert remaining time to minutes and seconds
    minutes, seconds = divmod(int(remaining_time), 60)
    countdown_str = f"{minutes:02d}:{seconds:02d}"
    # Display countdown timer
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"""
            <div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                Question {st.session_state.current_question + 1} of {len(st.session_state.quiz)}
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        countdown_placeholder = st.empty()
        countdown_placeholder.markdown(f"""<div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                 ⏳ Remaining Time: {countdown_str}</div>
            """,
            unsafe_allow_html=True
        )


    #saving quiz in session data
    st.session_state.quiz = get_db_data("Scrum")

    # Check if time is up (e.g., 20 minutes)
    if elapsed_time > 1200:
        st.write("Time is up!")
        st.session_state.page_section = "calculate_score"
        st.rerun()
    # Display quiz data in the left column

    if st.session_state.current_question < len(st.session_state.quiz):
        row = st.session_state.quiz[st.session_state.current_question]

        question_id = row[0]
        question = row[1]
        option_1 = row[2]
        option_2 = row[3]
        option_3 = row[4]
        option_4 = row[5]

        selected_option = st.radio(question,[option_1, option_2, option_3, option_4],index=None,key=question_id)
        st.session_state.selected_options[question_id] = selected_option
        st.write("")

        if st.button("Next"):
            st.session_state.current_question += 1
            st.rerun()
    else:
        st.write("You have completed the assessment!")
        st.session_state.page_section = "calculate_score"
        st.rerun()

def calculate_score():
    header_page()
    st.session_state.section = "calculate_score"
    st.subheader("Here the datails of your score")
    rows = st.session_state.quiz
    score = 0
    for row in rows:
        question_id = row[0]
        question = row[1]
        correct_answer = row[6]
        explanation = row[7]
        selected_option = st.session_state.selected_options.get(question_id, None)
        if selected_option == correct_answer:
            score += 1
            st.markdown(f"""<div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                        Question: {question}<br>Selected: {selected_option} ✅ <span style='color: green;'>Correct!</span>
                        </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                        Question: {question}<br>Selected: <span style='color: red;'>{selected_option} ❌ </span><br>Correct Answer: {correct_answer}<br>Explanation: {explanation}
                        </div>""", unsafe_allow_html=True)

    rated_score = int(score / len(rows) * 100)
    st.session_state.score = rated_score
    st.header(f"Your score: {rated_score}")
    st.page_link("pages/results.py", label="See your Results", icon="📊")
    st.page_link("pages/resources.py", label="Go to Resources", icon="📚")

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
        st.session_state.page = "agile"
        st.rerun()
    elif st.button("Scrum"):
        st.session_state.page = "scrum"
        st.rerun()
    elif st.button("Technical Literacy"):
        agile()
    elif st.button("Bussines Literacy"):
        agile()
    elif st.button("Delivery"):
        agile()
    elif st.button("Meeting Mediation & Facilitation"):
        agile()




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
            if 'assesment_type' not in st.session_state:
                st.session_state.assesment_type = ""
            #rendering options
            if st.session_state.page == "": 
                render_assessment_page()
                #AGILE
            elif st.session_state.page == "agile":
                st.session_state.assesment_type = "Agile"
                if st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "agile_assessment":
                    agile()
                else:
                    agile_intro()
                    #SCRUM
            elif st.session_state.page == "scrum":
                st.session_state.assesment_type = "scrum"
                if st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "scrum_assessment":
                    scrum()
                else:
                    scrum_intro()
        else:
            st.subheader("Log in to have access to Assessment section")
    else:
        st.subheader("Log in to have access to Assessment section")
    