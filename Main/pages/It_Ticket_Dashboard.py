import streamlit as st
import pandas as pd
from app_model.it_tickets import get_all_it_tickets
from app_model.db import get_conn
from groq import Groq
st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
   layout="wide")

#personal api key is to be added into the variable
client = Groq(api_key="ADD_API_KEY")
#'''locking the page and only allowing account holders to access it ensures that the data is secure 
# and only accessable to authorised users'''
#can't access this page unless user has logged in 
if not st.session_state.get('access_granted',False): #used AI to know how to block page information unless a certain proccess happens in another page
    st.warning("Page is locked ")
    st.stop()
else:
    st.success("You are logged in!") #access to the page has been permitted 



conn = get_conn()
data = get_all_it_tickets(conn)


st.title("Welcome to the It Tickets Dashboard!")
tab_ticket,tab_ticket_Chat= st.tabs(['Ticket Dashboard','It Ticket AI chat'])

with tab_ticket:
    #'''this will allow me to give permission to who can access certain parts of the information displayed in this page
    if not st.session_state.get('all_access',False):
        st.warning('Tab locked')
    else:
        with st.sidebar:
            #user can access different tabs to see different sets of data
            st.header("Navigation")
            desc = st.selectbox('Assigned', data['assigned_to'].unique())

        data['created_at'] = pd.to_datetime(data['created_at'])
        filter_data = data[data['assigned_to'] == desc] #filtered data according to the time it was created 

        #used to create 2 charts
        colm1 , colm2 = st.columns(2)

        with colm1:
            #displays a bar chat with information about the status of the ticket problem-solving progress
            st.subheader(f"It tickets assigned to: {desc}")
            st.bar_chart(filter_data['status'].value_counts())


        with colm2:
            #line chart that displays the priority of ticket problems and the status of the process of fixing the problems
            st.subheader("Status of It Tickets")
            st.line_chart(filter_data, x = 'priority' , y = 'status')

        #table to display the filtered data
        st.subheader("Filtered data")
        st.dataframe(filter_data)


#create session state variables used to clear previous AI responses when new requests are made
#'''AI suggestions have been incorporated in this section of code that are not shown in the week 11 labsheet and 
# groq cloud playground. '''
if "ticket_ai_chat" not in st.session_state:
    st.session_state.ticket_ai_chat = False

#button to open AI chat
if st.button("open_ai"):
    st.session_state.ticket_ai_chat = True 
    st.rerun()

#since session state is true, tab becomes available
if st.session_state.ticket_ai_chat:
    with tab_ticket_Chat:
        ticket = st.selectbox("What would you like to have analysed:",data['priority'].tolist())

        #modifying the system's response style
        if 'messages' not in st.session_state:
            st.session_state.messages = [{"role": "system","content":"You are an IT operations lead. Prioritise support."}]


        #clears the previous response when new request is made
        if "last_ticket" not in st.session_state:
            st.session_state.last_ticket = ticket
        if ticket != st.session_state.last_ticket:
            st.session_state.last_ticket = ticket
            st.session_state.messages = [{"role": "system","content":"You are an IT operations lead. Prioritise support."}]

        for messages in st.session_state.messages: #used to hide system's prompt
            if messages["role"] != "system":
                with st.chat_message(messages["role"]):
                    st.write(messages["content"])
        
        prompt = f"""Analyze this ticket problem:
            
        {ticket}

        provide:
        1. Support tickets by impact and urgency
        2. Suggest troubleshooting steps
        3. Infrastructure best practices """
        if st.button("Analyze"):
            #creates an interaction with the machine where 'user' is the role of the user
            st.session_state.messages.append({"role": "user","content":prompt})
            st.chat_message("user").write(prompt)

           #version of the machine being used
            chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages = st.session_state.messages)

            #'assistant' is the role of the machine
            reply = (chat_completion.choices[0].message.content)
            st.session_state.messages.append({"role": "assistant","content":reply})
            st.chat_message("assistant").write(reply)
        

        #clears the AI chat 
        if st.button("Clear chat"):
            st.session_state.messages = [{"role": "system","content":"You are an IT operations lead. Prioritise support."}]
            st.rerun()

#allows user to go to the next page
if st.button("->"):                                     
    st.switch_page("pages/Metadata_Dashboard.py")

#button that allows user to go to the previous page
if st.button("<-"):
    st.switch_page("pages/Cyber_Incidents_Dashboard.py")

