from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.vectorstores import FAISS


def create_chatbot():
    llm = Ollama(model="fine_tuned_model_name")
    retriever = FAISS.load_local("faiss_index")
    return RetrievalQA(llm=llm, retriever=retriever)
