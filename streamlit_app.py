import os
import time
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from pdfchatapp.main import PdfChatApp, clear_folder
from streamlit_chat import message
from dotenv import load_dotenv
load_dotenv()
pdf_folder = "Data"
response_time = 0
clicked_button_name = None
temp_update = False
# st.set_page_config("Chat PDF")
# Main page content
st.header("Chat with PDF")
sidebar_container = st.sidebar.container()
rag_pipeline_container = st.container()
response_container = st.container()
input_container = st.container()

def initialise_llms(temprature=0,llm_name= "OpenAI"):
    if llm_name == "OpenAI":
        return ChatOpenAI(temperature=temprature, verbose=True),OpenAIEmbeddings()
    elif llm_name == "Gemini":
        return ChatGroq(temperature=temprature,model_name="gemma2-9b-it"),OpenAIEmbeddings() 
    elif llm_name == "Gemma":
        return ChatGroq(temperature=temprature,model_name="gemma2-9b-it"),OpenAIEmbeddings() 
    elif llm_name == "Llama":
        return ChatGroq(temperature=temprature,model_name="Llama3-8b-8192"),OpenAIEmbeddings()


if (
    "user_prompt_history" not in st.session_state
    and "chat_answers_history" not in st.session_state
    and "chat_history" not in st.session_state
    and "app" not in st.session_state
    and "llm_name" not in st.session_state
    ):
    
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answers_history"] = []
    st.session_state["chat_history"] = []
    st.session_state["app"] = None
    st.session_state["llm_name"] = None
def on_btn_click():
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answers_history"] = []
    st.session_state["chat_history"] = []  
    
with sidebar_container:
    # Block 1: File Uploader component
    with st.sidebar.container():
        st.subheader("File Uploader")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"): 
            os.makedirs(pdf_folder, exist_ok=True)
            clear_folder(pdf_folder)
            for uploaded_file in pdf_docs:
                file_path = os.path.join(pdf_folder, uploaded_file.name)
                # Save the uploaded file to the local path
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())       
            st.success("File Uploaded Successfully!")            

    # Add a horizontal line for separation
    st.sidebar.markdown("---")

    # Block 2: Slider component
    with st.sidebar.container():
        st.subheader("Temprature Slider")
        slider_value = st.slider(
            "Choose a value between 0 to 1",
            min_value=0.0,  # Minimum value
            max_value=1.0,  # Maximum value
            value=0.0,      # Default value
            step=0.1        # Step size
        )
        st.write(f"Selected value: {slider_value}")
        if slider_value != 0:
            temp_update = True
    # Add another horizontal line for separation
    st.sidebar.markdown("---")




with rag_pipeline_container:
    # Row 1: Three equal-width buttons
    col1, col2, col3,col4 = st.columns([0.25,0.25,0.25,0.25])  # Create three equal columns

    # Initialize an empty container to display the clicked button name
    button_placeholder = st.empty()
    

    with col1:
        if st.button("OpenAI",use_container_width  = True):
            st.session_state["llm_name"]  = "OpenAI"
    with col2:
        if st.button("Gemini",use_container_width  = True):
            st.session_state["llm_name"]  = "Gemini"
            st.success("Yet to integrate Gemini model. Currently using Gemma Model")        
    with col3:
        if st.button("Gemma",use_container_width  = True):
            st.session_state["llm_name"]  = "Gemma"
    with col4:
        if st.button("Llama",use_container_width  = True):
            st.session_state["llm_name"]  = "Llama"
            
    
    if temp_update or st.session_state["llm_name"]: 
        if st.session_state.get("llm_name", None) is None:
            st.session_state["llm_name"]  = "OpenAI"
        llm, embeddings  = initialise_llms(temprature=slider_value,llm_name=st.session_state.get("llm_name", None))
        st.write(f"Selected LLM: {st.session_state.get("llm_name", None)}")
        st.write(f"Model temprature: {slider_value}")
        st.write(f"Model Version: {llm.model_name}")
        st.write(f"Embedding version: {embeddings.model}")
        start_time=time.process_time()
        with st.spinner("Building RAG Database..."):
            vectorstore_dir = "vectordb"
            if not os.path.exists(vectorstore_dir):
                os.makedirs(vectorstore_dir,exist_ok=True)
            clear_folder(vectorstore_dir)
            
            if os.path.exists(pdf_folder) and len(os.listdir(pdf_folder))>0: 
                st.session_state["app"] = PdfChatApp(
                file_path = pdf_folder, 
                embeddings = embeddings, 
                llm = llm, vectorstore_dir = vectorstore_dir
                ) 
                _ = st.session_state["app"].create_vectordb()
                # st.session_state["retrival_chain"] = pdfchatapp.get_conversational_chain()   
                st.success("Succesfully Setup the RAG Pipeline.")
            else:
                print("Pass") 
        st.write(f"Time Taken : {round(time.process_time()-start_time,2)} seconds") 
        temp_update = False       
               
                               
with input_container:
    # Row 3: Text input and Send button in two columns
    col1, col2 = st.columns([0.9, 0.1])  # Create two columns (3:1 ratio for width)
    with col1:
        user_message = st.text_input(label= "Enter your message",label_visibility = "collapsed",placeholder="Type your message here...")   
    with col2:
        submit_button = st.button("Send",use_container_width  = True)
    if submit_button or user_message:
        start=time.process_time()
        generated_response= st.session_state["app"].get_llm_response(
            query = user_message ,chat_history = st.session_state["chat_history"])
        response_time = time.process_time()-start
        st.session_state["user_prompt_history"].append(user_message)
        st.session_state["chat_answers_history"].append(generated_response["result"])
        st.session_state["chat_history"].append(("human",user_message))
        st.session_state["chat_history"].append(("ai",generated_response["result"]))
   
        
if st.session_state["chat_answers_history"]:
    with response_container:
        count = 0
        # count_ = 0
        for generated_response, user_query in zip(st.session_state["chat_answers_history"],st.session_state["user_prompt_history"]):
            count +=  1
            # print(generated_response, user_query)
            message(user_query, is_user=True, key=f"{count}_user")
            message(generated_response,key=f"{count}") 
        st.write(f"Response time : {round(response_time,2)} seconds")   
        st.button("Clear message", on_click=on_btn_click)    