from datetime import datetime
import streamlit as st
import math
import base64
import sqlite3
import time
from datetime import datetime
def get_db_data(table):
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+table+" LIMIT 20;")
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

def assessment_intro(assesment_type):
    header_page()
    st.write("Evaluate your scrum master skills and assess areas for improvement based on the skill matrix for Scrum Master")
    st.write("This self-sssessment will guide you through a series of questions. Each question have 4 options and only ones is the correct answer, with a limited time of 20 minutes")
    if st.button("Start "+assesment_type.replace("_"," ")+" Assessment"):
        st.session_state.page_section = assesment_type.lower()+"_assessment"
        print(st.session_state.page_section)
        st.session_state.start_time = time.time()
        st.session_state.selected_options = {}
        st.session_state.current_question = 0
        st.rerun()

def assessment(table_name):
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
    st.session_state.quiz = get_db_data(table_name)

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
        st.session_state.page_section = "evaluate_answers"
        st.session_state.current_answer_index = 0
        st.rerun()

def calculate_score():
    header_page()
    st.session_state.section = "calculate_score"
    st.subheader("Here the datails of your score")

    rows = st.session_state.quiz
    score = 0
    right_difficulty = {1:0, 2:0, 3:0, 4:0}
    wrong_difficulty = {1:0, 2:0, 3:0, 4:0}
    for row in rows:
        question_id = row[0]
        question = row[1]
        correct_answer = row[6]
        explanation = row[7]
        question_level = row[8]
        selected_option = st.session_state.selected_options.get(question_id, None)
        if selected_option == correct_answer:
            right_difficulty[question_level] += 1
            st.markdown(f"""<div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                        Question: {question}<br>Selected: {selected_option} ✅ <span style='color: green;'>Correct!</span>
                        </div>""", unsafe_allow_html=True)
        else:
            wrong_difficulty[question_level] += 1
            st.markdown(f"""<div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                        Question: {question}<br>Selected: <span style='color: red;'>{selected_option} ❌ </span><br>Correct Answer: {correct_answer}<br>Explanation: {explanation}
                        </div>""", unsafe_allow_html=True)

    score = scoring_function(right_difficulty,wrong_difficulty)

    st.session_state.score = score
    st.header(f"Your score: {score}")
    level = 'PL1 : Beginner'
    if score <= 60 :
        level = 'PL1 : Beginner'
    elif score > 60 and score <= 80 :
        level = 'PL2 : Practicioner'
    elif score > 80 and score <= 95 :
        level = 'PL3 : Proficient'
    elif score > 95 :
        level = 'PL4 : Expert'
    st.subheader(f"Due to your score you are considered a  {level}")
    save_score()
    st.page_link("start.py", label="Home", icon="🏠")
    st.page_link("pages/results.py", label="See your Results", icon="📊")
    st.page_link("pages/resources.py", label="Go to Resources", icon="📚")

def evaluate_answers():
    header_page()
    # Initialize session state for current answer index
    if 'current_answer_index' not in st.session_state:
        st.session_state.current_answer_index = 0
        st.session_state.score = 0

    # Get the current answer index
    current_index = st.session_state.current_answer_index

    # Get the selected options and quiz data from session state
    selected_options = st.session_state.selected_options
    rows = st.session_state.quiz

    # Display the current answer and its details
    if rows and selected_options:
        question_id = list(selected_options.keys())[current_index]
        selected_option = selected_options[question_id]
        question_data = next((row for row in rows if row[0] == question_id), None)

        if question_data:
            question = question_data[1]
            correct_answer = question_data[6]
            explanation = question_data[7]

            st.subheader(f"Evaluation: Question {current_index + 1}/{len(selected_options)}")
            st.markdown(f"**Question:** {question}")
            if selected_option == correct_answer:
                st.markdown(f"**Selected Answer:** {selected_option} ✅ ")
            else:
                st.markdown(f"**Selected Answer:** {selected_option} ❌")

            st.markdown(f"**Correct Answer:** {correct_answer}")
            st.markdown(f"**Explanation:** {explanation}")

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Previous", key="prev"):
                    if current_index > 0:
                        st.session_state.current_answer_index -= 1
                        st.rerun()
            with col2:
                st.write(f"Answer {current_index + 1} of {len(selected_options)}")
            with col3:
                if st.button("Next", key="next"):
                    if current_index < len(selected_options) - 1:
                        st.session_state.current_answer_index += 1
                        st.rerun()
                    if current_index == len(selected_options) - 1:
                        st.session_state.page_section = "calculate_score"
                        st.rerun()
    else:
        st.write("No answers available.")
        st.session_state.page_section = "calculate_score"
        st.rerun()

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
        st.session_state.page = "Technical_Literacy"
        st.rerun()
    elif st.button("Business Literacy"):
        st.session_state.page = "Business_Literacy"
        st.rerun()
    elif st.button("Delivery"):
        st.session_state.page = "Delivery"
        st.rerun()
    elif st.button("Meeting Mediation & Facilitation"):
        st.session_state.page = "Meeting_Mediation_&_Facilitation"
        st.rerun()

def save_score():
    user = st.session_state.username
    score = st.session_state.score
    date = today_date = datetime.today().strftime('%Y-%m-%d')
    assesment_type = st.session_state.assesment_type
    # Connect to the SQLite database
    conn = sqlite3.connect('data/agile_training.db')
    cursor = conn.cursor()
    # Get the user_id from the users table
    cursor.execute('SELECT user_id FROM Users WHERE user = ?', (user,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
        # Insert the values into the Evaluations table
        cursor.execute('INSERT INTO Evaluations (user_id, percentace_level, date, assesment_type) VALUES (?, ?, ?, ?)', (user_id, score, date, assesment_type))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def rasch_probability(theta, b_i):
    # Rasch Model: P(X = 1 | theta, b_i) = e^(theta - b_i) / (1 + e^(theta - b_i))
    return math.exp(theta - b_i) / (1 + math.exp(theta - b_i))

def select_item_based_on_rasch(theta, items):
    best_item = None
    highest_prob = -1
    for item in items:
        item_id, question, difficulty = item
        prob = rasch_probability(theta, difficulty)  # Calculate the probability
        # Select the item with the highest probability of being answered correctly
        if prob > highest_prob:
            highest_prob = prob
            best_item = item
            
    return best_item

def scoring_function(right, wrong):
    # right = {1: 4, 2: 1, 3: 0, 4: 0}
    # wrong = {1: 12, 2: 3, 3: 0, 4: 0}
    # Calculate the total possible score
    final_score = 0
    right = sum(key * value for key, value in right.items())
    wrong = sum(key * value for key, value in wrong.items())
    total_possible_score = right + wrong
    final_score = math.ceil((right/total_possible_score) * 100)

    return final_score


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
                if st.session_state.page_section == "evaluate_answers":
                    evaluate_answers()
                elif st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "agile_assessment":
                    assessment("AgileAssesment")
                else:
                    assessment_intro("Agile")
            #SCRUM
            elif st.session_state.page == "scrum":
                st.session_state.assesment_type = "scrum"
                if st.session_state.page_section == "evaluate_answers":
                    evaluate_answers()
                elif st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "scrum_assessment":
                    assessment("Scrum")
                else:
                    assessment_intro("Scrum")
            #Business Literacy
            elif st.session_state.page == "Business_Literacy":
                st.session_state.assesment_type = "Business_Literacy"
                if st.session_state.page_section == "evaluate_answers":
                    evaluate_answers()
                elif st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "business_literacy_assessment":
                    assessment("BusinessLiteracy")
                else:
                    assessment_intro("Business_Literacy")
            #Technical Literacy
            elif st.session_state.page == "Technical_Literacy":
                st.session_state.assesment_type = "Technical_Literacy"
                if st.session_state.page_section == "evaluate_answers":
                    evaluate_answers()
                elif st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "technical_literacy_assessment":
                    assessment("TechnicalLiteracy")
                else:
                    assessment_intro("Technical_Literacy")
            #Delivery
            elif st.session_state.page == "Delivery":
                st.session_state.assesment_type = "Delivery"
                if st.session_state.page_section == "evaluate_answers":
                    evaluate_answers()
                elif st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "delivery_assessment":
                    assessment("Delivery")
                else:
                    assessment_intro("Delivery")
            #Meeting Mediation & Facilitation
            elif st.session_state.page == "Meeting_Mediation_&_Facilitation":
                st.session_state.assesment_type = "Meeting_Mediation_&_Facilitation"
                if st.session_state.page_section == "evaluate_answers":
                    evaluate_answers()
                elif st.session_state.page_section == "calculate_score":
                    calculate_score()
                elif st.session_state.page_section == "meeting_mediation_&_facilitation_assessment":
                    assessment("MeetingMediationAndFacilitation")
                else:
                    assessment_intro("Meeting_Mediation_&_Facilitation")
        else:
            st.subheader("Log in to have access to Assessment section")
    else:
        st.subheader("Log in to have access to Assessment section")
    