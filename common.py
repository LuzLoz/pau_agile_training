import streamlit as st
import sqlite3
import datetime
import base64

def render_header():
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
    header_col1, header_col2, header_col3 = st.columns([1, 1, 3])
    
    with header_col1:
         # Read and encode the image to base64
        with open("static/logo.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        
        # Custom HTML for the image with click event
        st.markdown(f"""
            <style>
            .logo-image {{
                width: 100px;
                height: 100px;
                cursor: pointer;
            }}
            </style>
            <img src="data:image/png;base64,{encoded_image}" class="logo-image" onclick="window.location.href='/?page=main'" />
            """, unsafe_allow_html=True)
    
    with header_col2:
        st.subheader(f'Welcome, {st.session_state.username}!')

    with header_col3:
        button_col1, button_col2, button_col3 = st.columns(3)
        with button_col1:
            if st.button('Assessment'):
                st.query_params["page"] = "assessment"
        with button_col2:
            if st.button('Resources'):
                st.query_params["page"] = "resources"
        with button_col3:
            if st.button('Results'):
                st.query_params["page"] = "results"

def render_main_page():
    render_header()

    st.markdown("<h1 style='text-align: center;'>Welcome to SCRUM Master Skills!", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Measure and Improve Your Scrum Master Skills", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>This Web site is dedicated to helping you measure and improve your hard skills as Scrum Master. Here, you will find a measurement tool and a wide range of resources to enhance your knowledge and expertise in this role.", unsafe_allow_html=True)

# Function to check login credentials
def check_login(username, password):
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to add a new user
def add_user(username, password):
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (user, password, incription_date) VALUES (?, ?, ?)', (username, password, datetime.date.today()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Function to fetch quiz questions and options
def fetch_quiz(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM AgileAssesment')
    questions = cursor.fetchall()
    
    quiz = []
    for question in questions:
        cursor.execute('SELECT * FROM options WHERE question_id = ?', (question[0],))
        options = cursor.fetchall()
        quiz.append((question, options))
    
    conn.close()
    return quiz

# Function to calculate results
def calculate_results(quiz, user_responses):
    correct_answers = 0
    total_questions = len(quiz)
    
    for question, options in quiz:
        correct_option = next(option for option in options if option[3])  # Assuming is_correct is the 4th column
        if user_responses.get(f'question_{question[0]}') == correct_option[0]:
            correct_answers += 1
    
    return correct_answers, total_questions

