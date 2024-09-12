 # LLM-based PDF Question Answering System

This project allows users to upload multiple PDFs and ask questions related to the content in the documents. It supports both open-source and paid language models (LLMs) and provides flexibility in adjusting the model's temperature for response control. 

## Features

- **Multiple PDF Uploads**: Users can upload one or more PDF files.
- **Interactive Q&A**: Ask questions about the content in the uploaded PDFs, and get responses powered by LLMs.
- **Model Flexibility**: Choose between different open-source and paid LLM models.
- **Adjustable Model Temperature**: Control the randomness of the model's responses by setting the temperature.

## How It Works

1. **Upload PDFs**: The user can upload multiple PDFs that contain the information they want to ask questions about.
2. **Ask Questions**: Once the PDFs are uploaded, the user can input a question. The system processes the documents and answers based on the content.
3. **LLM Integration**: The project integrates with different models, allowing you to select which model to use (open-source or paid).
4. **Model Temperature**: Adjust the temperature of the selected model to control how deterministic or creative the model's responses are.

## Getting Started

Follow these steps to set up and run the project:

### Prerequisites

1. **Python**: Make sure Python is installed on your system (Python 3.8 or higher).
2. **Project Setup**: 
   ```bash
   1. conda create -n venv python
   2. conda activate venv
   3. pip install -r requirements.txt
   4. streamlit run streamlit_app.py 
   
### Usage
1. **Upload File**: Upload pdf documents.
2. **Choose a Model**: You can select either open-source or paid models depending on your preference.
3. **Set Temperature**: Adjust the temperature to control the randomness of the model's responses. Higher temperatures lead to more random responses, while lower values make the responses more deterministic.
4. **Start Asking Questions**: Once your PDFs are uploaded, you can interactively ask questions about the content.