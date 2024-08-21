import streamlit as st
from common import check_login, add_user, render_main_page
from assessment import render_assessment_page
from resources import render_resources_page
from results import render_results_page



# Login form
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title('Agile Assessment')
    st.image('static/logo.png', width=200)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            user = check_login(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success('Login successful!')
            else:
                st.error('Invalid username or password')

    with col2:
        st.subheader('Sign Up')
        new_username = st.text_input('New Username')
        new_password = st.text_input('New Password', type='password')
        if st.button('Sign Up'):
            if add_user(new_username, new_password):
                st.success('User created successfully! Please log in.')
            else:
                st.error('Username already exists. Please choose a different username.')
else:
    # main page
    
    
    query_params = st.query_params
    if "page" in st.query_params:
        if st.query_params["page"] == "assessment":
            render_assessment_page()
        elif st.query_params["page"] == "resources":
            render_resources_page()
        elif st.query_params["page"] == "results":
            render_results_page()
    else:
        render_main_page()