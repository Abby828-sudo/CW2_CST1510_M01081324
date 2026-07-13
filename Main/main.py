import streamlit as st
import string
from app_model.hashing import generate_hash,is_valid_hash
from app_model.db import get_conn
from app_model.users import add_user,get_user

conn = get_conn()

# make website icon
st.set_page_config(
  page_title="Home",
  page_icon="🏠",
 layout="wide")


st.title("Welcome to the Home page!🏠")

# set session state of page to lock it until user is logged in
if 'logged_in' not in st.session_state:
  st.session_state['logged_in'] = False

#set session state for user access
if 'access_granted' not in st.session_state:
   st.session_state['access_granted'] = False
if 'all_access' not in st.session_state:
   st.session_state['all_access'] = False


# making tabs to register and login a user
tab_login,tab_register = st.tabs(["Login ","Register"])




# design the register tab
#'''user enters their registration details which are stored in the project_data database'''
with tab_register:
    register_user = st.text_input("New Username")
    register_num = st.text_input("Phone number",type='default') #allows users to put phone number with {+} symbol
    check =  get_user(conn,register_user) # will be used to check the database if username already exists
    register_pass = st.text_input("New Password",type='password')
    conf_register_pass = st.text_input("Confirm password",type='password') # user must confirm password for password to be hashed
    role = st.selectbox("Role",options=("Select an option","admin","user"),key="r_role") # role must be admin or user.
    #For security purposes to ensure users don't access certain information that only the admin can.
    #'''This is used for a validation check to ensure the password created matches the criteria made by the programmer'''
    #will be used to check if the password is valid
    symbol_c = sum(1 for letter in register_pass if letter in string.punctuation) # used AI to learn how to use the "string" module
    digit_c = sum(1 for letter in register_pass if letter.isdigit())# used AI to learn how to use the "string" module
    if st.button("Register",key="r_button"):
        #check that all fields are filled
        if not register_user or not register_num or not register_pass or not conf_register_pass or not role:
            st.warning("Fill in all the fields")
        #check if username already exists
        elif check is not None:
            st.warning("Username already exists, enter a valid one.")
        #check that password is 7 or more characters
        elif len(register_pass) < 7:
            st.warning("Paaword must be 7 or more characters")
        #check that new and confirmed password are the same
        elif register_pass != conf_register_pass:
            st.error("Password does not match!")
        #check that role has been selected
        elif role != 'admin' and role != 'user':
            st.warning("Role must be selected")
        #check that password has at least 2 digits and 3 symbols
        elif symbol_c < 3 or digit_c < 2:
            st.warning("Password must have at least 2 digits and 3 symbols")
        elif not register_num.startswith("+") or not register_num[1:].isdigit(): #Ai was used to produce code for this check
            st.error("Phone number must only have numbers and {+} symbol!")
        elif len(register_num[1:]) != 8: #Ai was used to produce code for this check
            st.warning("Phone number must be 8 digits")
        else:
            hash_password = generate_hash(register_pass)
            #adding user to the database - project_data.db
            add_user(conn,register_user,phone_num=register_num,password_hash=hash_password,roles=role)
            st.success("Registration complete! Login to access dashboard.")
            #keeping the user logged out until they log in, in the login tab
            st.session_state['logged_in'] = False

with tab_login:
    login_user = st.text_input("Username", key=('login_user'))
    login_pass = st.text_input("Password",type='password', key='login_pass')
    if st.button("Log In",key='l_button'):
        #check that all fields are filled
        if not login_user or not login_pass:
            st.warning("Fill in all the fields")
        else:
            #'''it's safer to make a variable and assign the function to it,
            # to check if username exists than to check the function directly'''
            uname  = get_user(conn,login_user) # used to check that username is valid.
            #check that username matches registered one in the database
            if uname is None: #used AI to solve errors involving this validation check
                st.error("Invalid username or password!")
            else:
                #assign function to the variables to search for user's details in the user table
                user_name,user_hash,role1 = uname
                #check that password is correct
                if is_valid_hash(login_pass,user_hash):
                    st.session_state['logged_in'] = True
                    st.success("Login successful!")
                    if role1.strip().lower() == 'admin':
                        st.session_state['access_granted'] = True
                        st.session_state['all_access'] = True
                        st.switch_page('pages/Cyber_Incidents_Dashboard.py') #automatic switch to the next page
                    else:
                        st.session_state['access_granted'] = True
                        st.session_state['all_access'] = False
                        st.switch_page('pages/Cyber_Incidents_Dashboard.py') #automatic switch to the next page
                else:
                    st.session_state['logged_in'] =False
                    st.warning("Incorrect password! Try again.")

    #allows user to change their password if forgotten
    if st.button("Forgot password",key='f_button'):
        st.session_state["show_page"] = True #unlocks the change password page
        st.success("reset page unlocked")
        st.switch_page('pages/Change_password.py') #automatic switch to the page



































































