import streamlit as st
import sqlite3
import datetime
import base64


def render_header():
    st.markdown("""
    <style>
    .link-button>button {
        background-color: #246cab;
    }
    .link-button>button:hover {
        background-color: #539cdc;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    with st.container(height=160):
        header_col1, header_col2, header_col3 = st.columns([1, 1, 1])
        
        with header_col1:
            # Read and encode the image to base64
            with open("images/logo.png", "rb") as image_file:
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
                <img src="data:image/png;base64,{encoded_image}" class="logo-image" onclick="window.location.href='/'" />
                """, unsafe_allow_html=True)
        
        with header_col2:
            st.subheader(f'Welcome, {st.session_state.username}!')

def render_main_page():
    render_header()
    with st.container(height=400):
        st.markdown("<h2 style='text-align: center;'>This is Scrum Master Skills", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>A Space where you can Assess & Improve ", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>This Web site is dedicated to helping you measure and improve your hard skills as Scrum Master. Here, you will find a measurement tool and a wide range of resources to enhance your knowledge and expertise in this role.", unsafe_allow_html=True)

        # st.page_link("start.py", label="Home", icon="🏠")
        st.page_link("pages/assessment.py", label="Assessments", icon="📄")
        st.page_link("pages/resources.py", label="Resources", icon="📚")
        st.page_link("pages/results.py", label="Results", icon="📊")

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
        # Check if the user already exists
        cursor.execute('SELECT 1 FROM users WHERE user = ?', (username,))
        if cursor.fetchone() is not None:
            return False  # User already exists
            
        cursor.execute('INSERT INTO users (user, password, inscription_data, "level") VALUES (?, ?, ?, ?)', (username, password, datetime.date.today(),0))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
