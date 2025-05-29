import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()

def get_retriever():
    embedding = HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDING_MODEL"))
    db = Chroma(persist_directory=os.getenv("CHROMA_DB_DIR"), embedding_function=embedding)
    return db.as_retriever(search_kwargs={"k": 4})
