import streamlit as st
# from common import check_login, add_user, render_main_page, render_header
import time
import base64

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
        st.markdown(f"<h3 style='text-align: center; color: #539cdc;'>{st.session_state.username}, welcome to Resources</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Here you can find resources to get stronger in the specific area you want to develop</h4>", unsafe_allow_html=True)
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

def render_resources_page():
    header_page()
    st.markdown("<h1 style='text-align: center;'>Resources Page</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>This is the Resources page content.</p>", unsafe_allow_html=True)

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
                render_resources_page()
            # elif st.session_state.page == "agile":
            #     if st.session_state.page_section == "calculate_score":
            #         calculate_score()
            #     elif st.session_state.page_section == "agile_assessment":
            #         agile()
            #     else:
            #         agile_intro()
        else:
            st.subheader("Log in to have access to this section")
    else:
        st.subheader("Log in to have access to this section")