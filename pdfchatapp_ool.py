import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langchain.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.prompts import PromptTemplate

from langchain_core.prompts import ChatPromptTemplate


class PdfChatApp():
    def __init__(self,file_path: str, embeddings, llm, vectorstore_dir) -> None:
        self.file_path = file_path
        self.embeddings = embeddings
        self.vectorstores_dir = vectorstore_dir
        self.search_type = "similarity"
        self.top_n = 3
        self.llm = llm
        pass
    def data_ingestion(self,file_path):
        # Create and load PDF Loader
        loader = PyPDFDirectoryLoader(file_path)
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
    def create_vectordb(self):
        docs = self.data_ingestion(file_path=self.file_path)
        _ = self.get_vector_store(
            docs= docs,
            embeddings = self.embeddings,
            vectorstore_dir = self.vectorstores_dir
        )
        
    def get_conversational_chain(self):
        retriever = self.load_retriever(self.embeddings,self.vectorstores_dir)
        # 2. Incorporate the retriever into a question-answering chain.
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Answer the question as detailed as possible from the provided context, make sure to provide all the details" 
            "if the answer is not in provided context just say, answer is not available in the context, don't provide the wrong answer"
            "\n\n"
            "{context}"
        )
        retrieval_qa_template = hub.pull("langchain-ai/retrieval-qa-chat")
        # retrieval_qa_template = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", system_prompt),
        #         ("human", "{input}"),
        #     ]
        # )

        # retrieval_qa_template = PromptTemplate(template = template, input_variables = ["context", "question"])
        document_chain = create_stuff_documents_chain(self.llm, retrieval_qa_template)
        rephrase_document = hub.pull("langchain-ai/chat-langchain-rephrase")
        history_aware_retriever = create_history_aware_retriever(
            llm=self.llm, retriever=retriever, prompt=rephrase_document
        )
        retrieval_chain = create_retrieval_chain(
            retriever=history_aware_retriever, combine_docs_chain=document_chain
        )
        
        return retrieval_chain
    def get_llm_response(self, query: str, chat_history: list[dict[str, any]] = []):
        
        retrieval_chain = self.get_conversational_chain()
        result = retrieval_chain.invoke(
            input={"input": query, "chat_history": chat_history}
        )
        new_result = {
            "query": result["input"],
            "result": result["answer"],
            "source_documents": result["context"],
        }
        return new_result
    
# def get_llm_response(chain, question):
#     return chain.invoke({"input": question})['answer']
        
        
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