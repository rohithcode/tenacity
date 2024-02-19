import streamlit as st
from streamlit_option_menu import option_menu
from views.demo import load_demo
from views.hear import load_hear
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login(fields={'Form name': 'Login','Username': 'Username','Password': 'Password','Login': 'Login'})
if authentication_status:
    st.sidebar.info(f'Welcome *{name}* :sunglasses:')
    with st.sidebar:
            selected = option_menu(menu_title="Options",options= ["Help Me Win", 'Hear Me Out'], 
                 menu_icon="cast", default_index=0)
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    if selected=="Help Me Win":
        load_demo()
    if selected=="Hear Me Out":
        load_hear()
    if selected == "Logout":
        authentication_status=False
            
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')


    

