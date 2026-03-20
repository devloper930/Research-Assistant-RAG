# processing.py
import os, re
from glob import glob
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import Config

def clean_text(text: str) -> str:
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def _load_pdf(path):
    loader = PyPDFLoader(path)
    pages  = loader.load_and_split()
    docs   = []
    for p in pages:
        txt = clean_text(p.page_content)
        if len(txt) < 20:
            continue
        p.page_content = txt
        p.metadata.update(source=os.path.basename(path))
        docs.append(p)
    return docs

def process_documents():
    pdfs = glob(Config.PDF_GLOB)
    docs = []
    with ThreadPoolExecutor() as ex:
        for subdocs in ex.map(_load_pdf, pdfs):
            docs.extend(subdocs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)

@lru_cache(maxsize=1)
def _get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )

def load_or_create_index():
    emb = _get_embeddings()
    if os.path.isdir(Config.INDEX_DIR):
        print("📂 Loading existing FAISS index...")
        return FAISS.load_local(
            Config.INDEX_DIR,
            emb,
            allow_dangerous_deserialization=True  # << add this
        )

    print("📁 Creating new FAISS index...")
    chunks = process_documents()
    index = FAISS.from_documents(chunks, emb)
    index.save_local(Config.INDEX_DIR)
    return index
