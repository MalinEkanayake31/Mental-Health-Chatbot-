import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDING_MODEL"))
data_path = "./backend/data/verified_docs"
docs = []

for file in os.listdir(data_path):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(data_path, file))
        docs.extend(loader.load())

db = Chroma.from_documents(docs, embedding=embedding, persist_directory=os.getenv("CHROMA_DB_DIR"))
db.persist()
print("✅ Embeddings created and saved.")
