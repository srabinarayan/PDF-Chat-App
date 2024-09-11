import os
import shutil
import os ,shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
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
class PdfChatApp():
    def __init__(self, embeddings, llm, vectorstore_dir) -> None:
        self.file_path = None
        self.embeddings = embeddings
        self.vectorstores_dir = vectorstore_dir
        self.search_type = "similarity"
        self.top_n = 3
        self.llm = llm
        pass
    def store_files(self,files):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        UPLOAD_FOLDER = os.path.join(current_directory, "Data")
        clear_folder(UPLOAD_FOLDER)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER,exist_ok=True)  
        for file in files:
            file = file.name
            file_name = file.split(os.sep)[-1]
            shutil.copy(file,os.path.join(UPLOAD_FOLDER,file_name))
        self.file_path =  UPLOAD_FOLDER
        print(self.file_path)
        return "File Uploaded Succesfully!!"   
    def data_ingestion(self,file_path):
        # Create and load PDF Loader
        loader = PyPDFLoader(file_path)
        raw_documents = loader.load()
        print(f"Loaded {len(raw_documents)} documents")
        # Split Text from pdf 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 600,chunk_overlap = 50)
        documents = text_splitter.split_documents(raw_documents)
        return documents
    def get_vector_store(self, docs, embeddings, vectorstore_dir):
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(vectorstore_dir)
        return None
    
    def load_retriever(self, embeddings,vectorstore_dir):
        retriever = (
            FAISS
            .load_local(vectorstore_dir,embeddings,allow_dangerous_deserialization=True)
            .as_retriever(search_type = self.search_type, search_kwargs = {"k":self.top_n})
        )
        return retriever
    def get_conversational_chain(self):
        docs = self.data_ingestion(file_path=self.file_path)
        _ = self.get_vector_store(
            docs= docs,
            embeddings = self.embeddings,
            vectorstore_dir = self.vectorstores_dir
        )
        retriever = self.load_retriever(self.embeddings,self.vectorstores_dir)
        # 2. Incorporate the retriever into a question-answering chain.
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Answer the question as detailed as possible from the provided context, make sure to provide all the details" 
            "if the answer is not in provided context just say, answer is not available in the context, don't provide the wrong answer"
            "\n\n"
            "{context}"
        )

        retrieval_qa_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # retrieval_qa_template = PromptTemplate(template = template, input_variables = ["context", "question"])
        document_chain = create_stuff_documents_chain(self.llm, retrieval_qa_template)
        retrieval_chain = create_retrieval_chain(
            retriever=retriever, combine_docs_chain=document_chain
        )
        
        return retrieval_chain
    
    def get_llm_response(self,chain, question):
        return chain.invoke({"input": question})['answer']
    
    def get_llm_response(self,chain, question):
        return chain.invoke({"input": question})['answer']
    def process_files(self,files):
            