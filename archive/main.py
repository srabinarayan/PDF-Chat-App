import os
import shutil
import gradio as gr
import os ,shutil
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from code import PdfChatApp
from interface import create_interface
# import streamlit as st
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(temperature=0.1, verbose=True)
embeddings = OpenAIEmbeddings()
pdfchatapp = PdfChatApp(embeddings,llm,"PDF-Chat App/vectordb")
# generator_chain = pdfchatapp.get_conversational_chain()
# query = "What is MobileNet architrecture ?"

def get_response(message, history):
    return message
demo,upload_button,text_input,submit_button = create_interface()
with demo:
    output = gr.Textbox(label="Status")
    print(f"Starting File Path: {pdfchatapp.file_path}")
    upload_button.upload(pdfchatapp.store_files, inputs=[upload_button], outputs=[output])
    pass
demo.launch()