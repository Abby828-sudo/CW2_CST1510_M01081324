import streamlit as st
import pandas as pd
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import get_conn
from groq import Groq

#personal api key is to be added into the variable
client = Groq(api_key="ADD_API_KEY")

st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
   layout="wide")

#'''locking the page and only allowing account holders to access it ensures that the data is secure 
# and only accessable to authorised users'''
#can't access this page unless user has logged in 
if not st.session_state.get('access_granted',False): #used AI to know how to block page information unless a certain proccess happens in another page
    st.warning("Page is locked ")
    st.stop()
else:
    st.success("You are logged in!")


conn = get_conn()
#gets a connection with the function created in the Cyber_Incidents python file
data = get_all_cyber_incidents(conn)

st.title("Welcome to the Cyber Incidents Dashboard!")
tab_cyber,tab_Cyber_Chat= st.tabs(['Cyber Dashboard','Cybersecurity AI chat'])

with tab_cyber:
    #'''this will allow me to give permission to who can access certain parts of the information displayed in this page
    if not st.session_state.get('all_access',False):
        st.warning('Tab locked')
    else:
        with st.sidebar:
            #user can access different tabs to see different sets of data
            st.header("Navigation")
            sever = st.selectbox('Severity Level', data['severity'].unique())

        data['timestamp'] = pd.to_datetime(data['timestamp'])
        #filters data based on it's severity
        filter_data = data[data['severity'] == sever]

        #creates columns which will be used to display different charts
        colm1 , colm2 = st.columns(2)

        with colm1:
            #bar chart that displays the severity of different categories in the table
            st.subheader(f"Cyber incidents with severity: {sever}")
            st.bar_chart(filter_data['category'].value_counts())


        with colm2:
            #line chart that displays the trends over time of the different categories 
            st.subheader("Category trend over time")
            st.line_chart(filter_data, x = 'timestamp' , y = 'category')

        #table created that will display the filtered data
        st.subheader("Filtered data")
        st.dataframe(filter_data)


#create session state variables used to clear previous AI responses when new requests are made
#'''AI suggestions have been incorporated in this section of code that are not shown in the week 11 labsheet and 
# groq cloud playground. '''
if "cyber_ai_chat" not in st.session_state:
    st.session_state.cyber_ai_chat = False

if st.button("open_ai"):
    st.session_state.cyber_ai_chat = True 
    st.rerun()

#since session state is true, tab becomes available
if st.session_state.cyber_ai_chat:
    with tab_Cyber_Chat:
        c_incident = st.selectbox("What would you like to have analysed:",data['category'].tolist())

        #modifying the system's response style
        if 'messages' not in st.session_state:
            st.session_state.messages = [{"role": "system","content":"You are a cybersecurity analyst.Analyse incidents using MITRE ATT&CK and CVE references"}]

        #clears the previous response when new request is made
        if "last_incident" not in st.session_state:
            st.session_state.last_incident = c_incident
        if c_incident != st.session_state.last_incident:
            st.session_state.last_incident = c_incident
            st.session_state.messages = [{"role": "system","content":"You are a cybersecurity analyst.Analyse incidents using MITRE ATT&CK and CVE references"}]
        
        for messages in st.session_state.messages: #used to hide system's prompt
            if messages["role"] != "system":
                with st.chat_message(messages["role"]):
                    st.write(messages["content"])


       
        prompt = f"""Analyze this cybersecurity incident:
            
        {c_incident}

        provide:
        1. Root cause analysis
        2. Immediate actions (bullet points)
        3. Long term prevention measures
        4. Risk level (Low,Medium,High,Critical) """
        

        #button that opens the AI interface
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
            st.session_state.messages = [{"role": "system","content":"You are a cybersecurity analyst.Analyse incidents using MITRE ATT&CK and CVE references"}]
            st.rerun()

#button that will allow user to go to the next page
if st.button("->"):
    st.switch_page("pages/It_Ticket_Dashboard.py")



