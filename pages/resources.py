import streamlit as st
# from common import check_login, add_user, render_main_page, render_header
import time
import base64

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

def footer_page():
    with st.container(height=160):
        footer_col1, footer_col2 = st.columns([3, 1])
        with footer_col1:
            st.page_link("start.py", label="Home", icon="🏠")
            st.page_link("pages/assessment.py", label="Assessments", icon="📄")
            st.page_link("pages/results.py", label="Results", icon="📊")
        with footer_col2:
            st.link_button("Feedback ⭐⭐⭐⭐⭐", "https://forms.gle/pNBmSCZmZXdiR9y4A", help="Send Feedback", type="secondary", disabled=False, use_container_width=False)

def render_resources_page():
    header_page()

    with st.container(height=400):
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
        # page content HERE
    footer_page()

    
if __name__ == "__main__":
    if 'logged_in' in st.session_state:
        if st.session_state.logged_in:
            render_resources_page()
        else:
            st.subheader("Log in to have access to this section")
    else:
        st.subheader("Log in to have access to this section")