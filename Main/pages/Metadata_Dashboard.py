import streamlit as st
import pandas as pd
from app_model.metadatas import get_all_datasets_metadata
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
#connection to the table created in the Metadata python file
data = get_all_datasets_metadata(conn)

st.title("Welcome to the Datasets Metadata Dashboard!")
tab_Data,tab_Data_Chat= st.tabs(['Dataset Dashboard','Dataset AI chat'])


with tab_Data:
    #'''this will allow me to give permission to who can access certain parts of the information displayed in this page
    if not st.session_state.get('all_access',False):
        st.warning('Tab locked')
    else:
        with st.sidebar:
            #allows user to see different tabs with differents sets of data
            st.header("Navigation")
            upload = st.selectbox('Uploads', data['uploaded_by'].unique())

        data['upload_date'] = pd.to_datetime(data['upload_date'])
        #filters data based on the time it was uploaded
        filter_data = data[data['uploaded_by'] == upload]

        #will be used to create charts
        colm1 ,colm2 = st.columns(2)

        with colm1:
            #shows the number of datasets uploaded by a certain admin
            st.subheader(f"Number of datasets uploaded by: {upload}")
            st.bar_chart(filter_data['name'].value_counts())

        with colm2:
            #rows that the names of data occupy 
            st.subheader("Dataset names against their size")
            st.line_chart(filter_data, x = 'name' , y = 'rows')

        #table that displays the filtered data
        st.subheader("Filtered data")
        st.dataframe(filter_data)

#create session state variables used to clear previous AI responses when new requests are made
#'''AI suggestions have been incorporated in this section of code that are not shown in the week 11 labsheet and 
# groq cloud playground. '''
if "Metadata_ai_chat" not in st.session_state:
    st.session_state.Metadata_ai_chat = False

if st.button("open_ai"):
    st.session_state.Metadata_ai_chat = True 
    st.rerun()

#session state used unlock the AI tab 
if st.session_state.Metadata_ai_chat: 
    with tab_Data_Chat:
        dataset = st.selectbox("What would you like to have analysed:",data['name'].tolist())

        #modifying the system's response style 
        if 'messages' not in st.session_state:
            st.session_state.messages = [{"role": "system","content":"You are a data science expert.Help with dataset analysis"}]

        #clears the previous response when new request is made
        if "last_dataset" not in st.session_state:
            st.session_state.last_dataset = dataset
        if dataset != st.session_state.last_dataset:
            st.session_state.last_dataset = dataset
            st.session_state.messages = [{"role": "system","content":"You are a data science expert.Help with dataset analysis"}]
        
        for messages in st.session_state.messages: #used to hide system's prompt
            if messages["role"] != "system":
                with st.chat_message(messages["role"]):
                    st.write(messages["content"])


        prompt = f"""Analyze this Dataset:
            
        {dataset}

        provide:
        1. Deep analysis
        2. Visualisation types (bullet points)
        3. Statistic methods
        4. Machine learning """
        
        #button that opens the AI chat
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
            st.session_state.messages = [{"role": "system","content":"You are a data science expert.Help with dataset analysis"}]
            st.rerun()

#allows user to go to the previous page
if st.button("<-"):
    st.switch_page("pages/It_Ticket_Dashboard.py")

