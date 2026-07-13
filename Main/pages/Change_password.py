import streamlit as st
import string
from app_model.hashing import generate_hash
from app_model.db import get_conn 
from app_model.users import update_user,get_user_by_phone_num


conn = get_conn()

#can't access this page unless the button (Forgot password) in the home page is pressed
#used AI to know how to block page information unless a certain proccess happens in another page
if not st.session_state.get("show_page",False):
    st.warning("Page is locked ")
    st.stop()
else:
    st.session_state["show_page"] = True

st.title('Reset password')

#set the session state of the page
#used AI to make up these two lines of code
if 'changed_password' not in st.session_state:
    st.session_state['changed_password'] = False

#create tab to change the user's password
tab_new_pass = st.tabs(["New password"])[0] #used AI to find a way to display only one tab without an error occurring

with tab_new_pass:
    #'''using a phone number or email is safer to use to change a password rather than using a username.
    #This ensures that no one can change another user's password without their knowledge which makes unauthorised access harder to achieve.'''
    phone_n = st.text_input("Phone Number") #phone number will be used to change the password
    new_pasw = st.text_input("New password",type='password')
    conf_pasw = st.text_input("Confirm password",type='password')
    
    #'''This is used for a validation check to ensure the password created matches the criteria made by the programmer'''
    #will be used to check if the password is valid
    symbol_c = sum(1 for letter in new_pasw if letter in string.punctuation)# used AI to learn how to use the "string" module
    digit_c = sum(1 for letter in new_pasw if letter.isdigit())# used AI to learn how to use the "string" module
    
    if st.button("Confirm"):
        #all fields must be filled
        if not phone_n or not new_pasw or not conf_pasw:
            st.warning("Fill in all the fields")
        #password must be 7 or more characters long
        elif len(new_pasw) < 7:
            st.warning("Password must be 7 characters or more")
        #check that password has at least 2 digits and 3 symbols
        elif symbol_c < 3 or digit_c < 2:
            st.warning("Password must have at least 2 digits and 3 symbols")
        #new and confirm password must be the same
        elif new_pasw != conf_pasw:
            st.error("Password does not match!")
        #check to see if phone number is registered
        #used AI to fix errors that came with trying to use a phone number to update user information
        elif not get_user_by_phone_num(conn,phone_n): 
            st.warning("Phone number not found")
        else: 
            hashed_password = generate_hash(new_pasw)
            update_user(conn,phone_n,hashed_password) #update the user's password 
            st.session_state['changed_password'] = True
            st.session_state['logged_in'] = False #user must log in to access the other pages
        
        
            st.success("Changed password successfully! Login to access dashboard.")
            #lock the page after the password has been changed
            st.session_state["show_page"] = False
            #automatic page switch so that the user can log in
            st.switch_page('main.py')
        

