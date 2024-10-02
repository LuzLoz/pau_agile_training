import streamlit as st
from common import check_login, add_user, render_main_page
st.set_page_config(initial_sidebar_state="collapsed") 
# Login form
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
# Initialize session state for sign up visibility
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False


if not st.session_state.show_signup and not st.session_state.logged_in:
    st.title('Agile Assessment')
    st.image('images/logo.png', width=200)
    st.subheader('Login')
    username = st.text_input('Username',key='login_username')
    password = st.text_input('Password', type='password', key='login_password')
    if st.button('Login',key='login'):
        user = check_login(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = ""
            st.session_state.page_section = ""
            st.success('Login successful!')
            st.rerun()
        else:
            st.error('Invalid username or password')
    # Add a link to toggle the sign up section
    if st.button('if you dont have an account you can Sign Up here', key='show_signup_link'):
        st.session_state.show_signup = True
        st.rerun()
# Only show the Sign Up section if the link is clicked
elif st.session_state.show_signup:
    st.title('Agile Assessment')
    st.image('images/logo.png', width=200)
    st.subheader('Sign Up')
    new_username = st.text_input('New Username',key='singup_username')
    new_password = st.text_input('New Password', type='password', key='singup_password')
    if st.button('Sign Up',key='singup'):
        if add_user(new_username, new_password):
            st.session_state.logged_in = True
            st.session_state.username = new_username
            st.session_state.page = ""
            st.session_state.page_section = ""
            st.session_state.show_signup = False
            render_main_page()
            st.rerun()
        else:
            st.subheader('Username already exists. Please choose a different username.')
else:
    # main page
    st.session_state.page = ""
    st.session_state.page_section = ""
    render_main_page()