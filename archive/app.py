import os
import shutil
import gradio as gr
import os ,shutil
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        # Remove all the files in the directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
def upload_file(files):
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(current_directory, "RAW_DATA")
    clear_folder(UPLOAD_FOLDER)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER,exist_ok=True)  
    for file in files:
        file = file.name
        file_name = file.split(os.sep)[-1]
        shutil.copy(file,os.path.join(UPLOAD_FOLDER,file_name))    
    gr.Info("File Uploaded!!")    
    return None
def get_response(message, history):
    return message
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=0.33):
            openai = gr.Button('Open-AI')
        with gr.Column(scale=0.33):
            gemma = gr.Button('Gemini')
        with gr.Column(scale=0.33):
            llama = gr.Button('LLAMA')    
    ##############
    # FIRST ROW:
    ##############
    with gr.Row() as row_one:
        
        with gr.Column() as chatbot_output:
            # chatbot = gr.ChatInterface(fn=get_response,
            #                            title="PDF - Chat APP", 
            #                         #    chatbot= gr.Chatbot(
            #                         #        label = None, 
            #                         #        value= [[None,"Hello, I'm your virtual assistant, here to guide you with processing loan applications and provide suitable recommendations."]]
            #                         #     ),
            #                             fill_height=True, 
            #                             retry_btn = "↻ Retry",
            #                             undo_btn = None,
            #                             submit_btn = "🢁"
            # )
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                bubble_full_width=False,
                height=500,
            )
    ##############
    # SECOND ROW:
    ##############
    with gr.Row():
        with gr.Column(scale=0.80):
                text_input = gr.Textbox(
                    show_label=False,
                    placeholder="Type here to ask your PDF",
                container=False)
        # input_txt = gr.Textbox(
        #     lines=4,
        #     scale=8,
        #     placeholder="Enter text and press enter, or upload PDF files",
        #     container=False,
        # ) 
        with gr.Column(scale=0.20):
            submit_button = gr.Button('Send')
    ##############
    # Third ROW:
    ##############
    with gr.Row() as row_third: 
        upload_button = gr.UploadButton("Click to Upload a File", file_types=["file"], file_count="multiple")
    # upload_button.upload(upload_file, upload_button, file_output)

demo.launch()