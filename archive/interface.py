import gradio as gr
def create_interface():
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
    return demo,upload_button,text_input,submit_button